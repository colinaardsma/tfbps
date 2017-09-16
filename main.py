import os
import ast
import time
import logging
import json
import webapp2
import api_connector
import jinja2
import hashing
import caching
import html_parser
import validuser
import db_models
import queries

# setup jinja2
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),
                            'templates') # set template_dir to main.py dir(current dir)/templates
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True) # set jinja2's working directory to template_dir

# define some functions that will be used by all pages
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        # simplifies self.response.out.write to self.write
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        # creates the string that will render html using jinja2 with html template named template
        # and parameters named params
        template = JINJA_ENV.get_template(template)
        return template.render(params)

    def render(self, template, **kw):
        # writes the html string created in render_str to the page
        self.write(self.render_str(template, **kw))

    def __init__(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        cookies = self.request.cookies.get('user') # pull cookie value
        uid = ""
        if cookies:
            uid = hashing.check_secure_val(cookies)

        self.user = uid and caching.cached_get_user_by_id(uid)
        self.auth = self.user and caching.cached_get_authorization(self.user.username)

        # if not self.user and self.request.path in auth_paths:
        # if not self.user:
        #     self.redirect('/login')

    # # check user authorization vs authorization lists
    # def get_auth(self, auth):
    #     if auth != "admin" and self.request.path in admin_auth_paths:
    #         self.redirect('/login')
    #     elif ((auth != "admin" and auth != "power_user") and
    #           self.request.path in power_user_auth_paths):
    #         self.redirect('/login')
    #     elif ((auth != "admin" and auth != "power_user" and auth != "commissioner") and
    #           self.request.path in commissioner_auth_paths):
    #         self.redirect('/login')
    #     elif ((auth != "admin" and auth != "power_user" and auth != "commissioner" and
    #            auth != "basic") and self.request.path in basic_auth_paths):
    #         self.redirect('/login')
    #     else:
    #         self.request.path

class MainHandler(Handler):
    def render_main(self):
        # pull username
        if self.user:
            user = self.user.username # get username from user object
            # self.get_auth(self.auth) # check to see if authorized to view page
        else:
            user = ""

        # fakeBbArticle = rssparsing.get_fakebb_rss_content(0)
        # yahooArticle = rssparsing.get_yahoo_rss_content(0)

        self.render("home.html", user=user)
        # self.render("home.html", user=user, fakeBbArticle=fakeBbArticle,
        #             yahooArticle=yahooArticle)
        # self.write(rssparsing.get_fakebb_rss_content(0))

    def get(self):
        self.render_main()

class BattingProjections(Handler):
    def render_batting_projections(self):
        import team_tools_db
        players = team_tools_db.batter_projections()
        self.render("spreadsheet.html", players=players, cat="batter")

    def get(self):
        self.render_batting_projections()

class PitchingProjections(Handler):
    def render_pitching_projections(self):
        import team_tools_db
        players = team_tools_db.pitcher_projections()
        self.render("spreadsheet.html", players=players, cat="pitcher")

    def get(self):
        self.render_pitching_projections()

class TeamToolsHTML(Handler):
    def render_fa_rater(self, league_no="", team_name="", player_name="", team_a={},
                        team_a_name="", team_a_players=[], team_b={}, team_b_name="",
                        team_b_players=[], trade_result={}):
        import team_tools_html
        # fa rater
        if league_no != "" and team_name != "":
            top_fa = team_tools_html.fa_finder(league_no, team_name)
            team_name = top_fa['Team Name']
        else:
            top_fa = None
        # single player lookup
        if player_name != "":
            single_player = team_tools_html.single_player_rater(player_name)
        else:
            single_player = None
        # trade analyzer
        if league_no != "" and team_a_name != "" and team_b_name != "":
            team_a = html_parser.get_single_yahoo_team(league_no, team_a_name)
            team_b = html_parser.get_single_yahoo_team(league_no, team_b_name)
            league_no = league_no
        elif league_no != "" and team_a and team_b and team_a_players and team_b_players:
            team_a = ast.literal_eval(team_a)
            team_b = ast.literal_eval(team_b)
            trade_result = team_tools_html.trade_analyzer(league_no, team_a, team_a_players,
                                                          team_b, team_b_players)
        else:
            team_a = None
            team_b = None
            trade_result = None
        # final standings projection
        if league_no == "" or (league_no != "" and team_name != "") or (team_a and team_b):
            projected_standings = None
        # final stanings projection
        if league_no != "" and team_name == "" and not (team_a or team_b):
            projected_standings = team_tools_html.final_standing_projection(league_no)
        else:
            projected_standings = None

        self.render("team_tools_html.html", top_fa=top_fa, single_player=single_player,
                    projected_standings=projected_standings, team_name=team_name,
                    league_no=league_no, team_a=team_a, team_b=team_b, trade_result=trade_result)

    def get(self):
        self.render_fa_rater()

    def post(self):
        league_no = self.request.get("league_no")
        team_name = self.request.get("team_name")
        player_name = self.request.get("player_name")
        team_a = self.request.get("team_a")
        team_a_name = self.request.get("team_a_name")
        team_a_players = self.request.POST.getall("team_a_players")
        team_b = self.request.get("team_b")
        team_b_name = self.request.get("team_b_name")
        team_b_players = self.request.POST.getall("team_b_players")
        self.render_fa_rater(league_no=league_no, team_name=team_name, player_name=player_name,
                             team_a=team_a, team_a_name=team_a_name, team_a_players=team_a_players,
                             team_b=team_b, team_b_name=team_b_name, team_b_players=team_b_players)

class TeamToolsDB(Handler):
    def render_fa_rater(self, league_no="", team_name="", player_name="", update=""):
        import team_tools_db
        # update projections
        if update == "":
            elapsed = None
        else:
            start = time.time()
            team_tools_db.pull_batters()
            team_tools_db.pull_pitchers()
            # team_tools_db.pull_players()
            end = time.time()
            elapsed = end - start
        # fa rater
        if league_no == "" or team_name == "":
            top_fa = None
        else:
            top_fa = team_tools_db.fa_finder(league_no, team_name)
            team_name = top_fa['Team Name']
        # single player lookup
        if player_name == "":
            single_player = None
        else:
            start = time.time()
            single_player = team_tools_db.single_player_rater(player_name)
            end = time.time()
            elapsed = end - start
            logging.info("\r\n***************\r\nBatter Creation in %f seconds", elapsed)

        # final stanings projection
        if league_no == "" or (league_no != "" and team_name != ""):
            projected_standings = None
        else:
            projected_standings = team_tools_db.final_standing_projection(league_no)

        self.render("team_tools_db.html", top_fa=top_fa, single_player=single_player,
                    projected_standings=projected_standings, team_name=team_name, elapsed=elapsed)

    def get(self):
        self.render_fa_rater()

    def post(self):
        league_no = self.request.get("league_no")
        team_name = self.request.get("team_name")
        player_name = self.request.get("player_name")
        update = self.request.get("update")
        self.render_fa_rater(league_no=league_no, team_name=team_name,
                             player_name=player_name, update=update)

class UpdateProjections(Handler):
    def render_update_projections(self, elapsed=""):
        self.render

    def get(self):
        start = time.time()
        import team_tools_db
        team_tools_db.pull_batters()
        team_tools_db.pull_pitchers()
        end = time.time()
        elapsed = end - start
        self.redirect("/team_tools_db")

class Oauth(Handler):
    def get(self):
        self.redirect(api_connector.request_auth())

class Redirect(Handler):
    def render_redirect(self, code):
        oauth_token = api_connector.get_token(code)
        yahoo_guid_json = api_connector.get_guid(oauth_token)
        yahoo_guid_dict = json.loads(yahoo_guid_json)
        guid = yahoo_guid_dict['guid']['value']

        self.redirect(str("http://localhost:8080?code=" + code))

    def get(self):
        code = self.request.get('code')
        self.render_redirect(code=code)

    def post(self):
        code = self.request.get('code')
        self.render_redirect(code=code)

class LocalhostRedirect(Handler):
    def render_locahostredirect(self, code):
        self.redirect(str('http://localhost:8080/redirect?code=' + code))

    def get(self):
        code = self.request.get('code')
        self.render_locahostredirect(code=code)

class Registration(Handler):
    def render_registration(self, username="", email="", usernameError="",
                            passwordError="", passVerifyError="", emailError=""):
        # pull username
        if self.user:
            user = self.user.username # get username from user object
            # self.get_auth(self.auth) # check to see if authorized to view page
        else:
            user = ""

        self.render("registration.html", username=username, email=email,
                    usernameError=usernameError, passwordError=passwordError,
                    passVerifyError=passVerifyError, emailError=emailError, user=user)

    def get(self):
        self.render_registration()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        passVerify = self.request.get("passVerify")
        email = self.request.get("email")
        error = False

        # check password
        if not password: # check if password is blank
            passwordError = "Password cannot be empty"
            error = True
        elif not validuser.valid_password(password): # check if password is valid
            passwordError = "Invalid Password"
            error = True
        else:
            passwordError = ""
        # check password verification
        if not passVerify: # check if password verification is blank
            passVerifyError = "Password Verification cannot be empty"
            error = True
        elif password != passVerify: # check if password matches password verification
            passVerifyError = "Passwords do not match"
            error = True
        else:
            passVerifyError = ""
        # check username
        if not username: # check if username is blank
            usernameError = "Username cannot be empty"
            error = True
        elif not validuser.valid_username(username): # check if username if valid
            usernameError = "Invalid Username"
            error = True
        elif caching.cached_check_username(username): # check if username is unique
            usernameError = "That username is taken"
            error = True
        else:
            usernameError = ""
        # check email
        if not email: # check if email is blank
            emailError = ""
        elif not validuser.valid_email(email): # check if email is valid
            emailError = "Invalid Email"
            error = True
        else:
            emailError = ""
        # see if any errors returned
        if error == False:
            username = username
            password = hashing.make_pw_hash(username, password) # hash password for storage in db
            authorization = "basic"
            db_models.store_user(username, password, email, authorization)
            # update cache
            caching.cached_check_username(username, True)
            caching.cached_user_by_name(username, True)
            caching.cached_get_users(True)
            
            time.sleep(1) # wait 2/10 of a second while post is entered into db
            user = caching.cached_user_by_name(username)
            user_id = user.key().id()
            self.response.headers.add_header('Set-Cookie', 'user=%s' %
                                             hashing.make_secure_val(user_id)) # hash user id for use in cookie



            self.redirect('/welcome')
        else:
            self.render_registration(username, email, usernameError,
                                     passwordError, passVerifyError,
                                     emailError)

class Login(Handler):
    def render_login(self, username="", error=""):
        # pull username
        if self.user:
            user = self.user.username # get username from user object
            self.get_auth(self.auth) # check to see if authorized to view page
        else:
            user = ""

        self.render("login.html", username=username, error=error, user=user)

    def get(self):
        self.render_login()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        if not caching.cached_check_username(username):
            error = "Invalid login"
        else:
            user_id = caching.cached_check_username(username)
            u = caching.cached_get_user_by_id(user_id)
            p = u.password
            salt = p.split("|")[1]
            if username == u.username:
                if hashing.make_pw_hash(username, password, salt) == p:
                    error = ""
                else:
                    error = "invalid login - pass"

        if error:
            self.render_login(username, error)
        else:
            self.response.headers.add_header('Set-Cookie', 'user=%s' % hashing.make_secure_val(user_id)) # hash user id for use in cookie
            self.redirect('/welcome')

class Logout(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user=""; expires=Thu, 01-Jan-1970 00:00:10 GMT') #clear cookie
        self.redirect('/registration')

class Welcome(Handler):
    def render_welcome(self):
        c = self.request.cookies.get('user') # pull cookie value
        usr = hashing.get_user_from_cookie(c)

        self.redirect('/')

    def get(self):
        self.render_welcome()

# routing
app = webapp2.WSGIApplication([
    ('/', MainHandler),

    # user handling
    ('/registration/?', Registration),
    ('/login/?', Login),
    ('/logout/?', Logout),
    ('/welcome/?', Welcome),

    # yahoo api
    ('/oauth/?', Oauth),
    ('/redirect/?', Redirect),
    ('/localhostredirect/?', LocalhostRedirect),

    # projections
    ('/batting_projections/?', BattingProjections),
    ('/pitching_projections/?', PitchingProjections),
    
    # team tools
    ('/team_tools_html/?', TeamToolsHTML),
    ('/team_tools_db/?', TeamToolsDB),
    ('/update_projections/?', UpdateProjections)
    ], debug=True)
    