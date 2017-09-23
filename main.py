import os
import ast
import time
import datetime
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
"""TESTING"""
GUID_REDIRECT_PATH = "/guid_localhost"
QUERY_REDIRECT_PATH = "/query_localhost"
"""PRODUCTION"""
# GUID_REDIRECT_PATH = "/quid_redirect"
# QUERY_REDIRECT_PATH = "/query_redirect"

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
        self.get_user()
        self.username = None
        if self.user:
            self.username = self.user.username
    
    def get_user(self):
        user_cookie = self.request.cookies.get('user') # pull cookie value

        user_id = ""
        if user_cookie:
            user_id = hashing.check_secure_val(user_cookie)

        self.user = user_id and caching.cached_get_user_by_id(user_id)
        self.auth = self.user and caching.cached_get_authorization(self.user.username)

        # pull username
        if self.user:
            # username = self.user.username # get username from user object
            self.get_auth(self.auth) # check to see if authorized to view page
        elif not self.user and self.request.path in auth_paths:
            self.redirect('/login')
        # else:
        #     username = ""
        # return username

    def update_user(self, user, username=None, password=None, email=None,
                    authorization=None, yahooGuid=None, last_accessed=None,
                    location=None, access_token=None, token_expiration=None,
                    refresh_token=None):
        user = queries.get_user_by_name(user.username)
        if username:
            user.username = username
        if password:
            password = hashing.make_pw_hash(username, password) # hash password for storage in db
            user.password = password
        if email:
            user.email = email
        if authorization:
            user.authorization = authorization
        if yahooGuid:
            user.yahooGuid = yahooGuid
        if last_accessed:
            user.last_accessed = last_accessed
        if location:
            user.location = location
        if access_token:
            user.access_token = access_token
        if token_expiration:
            user.token_expiration = token_expiration
        if refresh_token:
            user.refresh_token = refresh_token
        db_models.update_user(user)


    def store_user(self, username, password, email, guid=None):
        db_models.store_user(username, password, email, guid)

        time.sleep(1) # wait 1 second while post is entered into db and memcache
        user = caching.cached_user_by_name(username)
        user_id = user.key().id()
        self.response.headers.add_header('Set-Cookie', 'user=%s' %
                                         hashing.make_secure_val(user_id)) # hash user id for use in cookie
        # self.redirect('/welcome')

    # check user authorization vs authorization lists
    def get_auth(self, auth):
        if auth != "admin" and self.request.path in admin_auth_paths:
            self.redirect('/login')
        elif ((auth != "admin" and auth != "power_user") and
              self.request.path in power_user_auth_paths):
            self.redirect('/login')
        elif ((auth != "admin" and auth != "power_user" and auth != "commissioner") and
              self.request.path in commissioner_auth_paths):
            self.redirect('/login')
        elif ((auth != "admin" and auth != "power_user" and auth != "commissioner" and
               auth != "basic") and self.request.path in basic_auth_paths):
            self.redirect('/login')
        else:
            self.request.path

class MainHandler(Handler):
    def render_main(self):
        # fakeBbArticle = rssparsing.get_fakebb_rss_content(0)
        # yahooArticle = rssparsing.get_yahoo_rss_content(0)

        self.render("home.html", username=self.username)
        # self.render("home.html", user=user, fakeBbArticle=fakeBbArticle,
        #             yahooArticle=yahooArticle)
        # self.write(rssparsing.get_fakebb_rss_content(0))

    def get(self):
        self.render_main()

class BattingProjections(Handler):
    def render_batting_projections(self):
        import team_tools_db
        players = team_tools_db.batter_projections()
        self.render("spreadsheet.html", players=players, cat="batter", username=self.username)

    def get(self):
        self.render_batting_projections()

class PitchingProjections(Handler):
    def render_pitching_projections(self):
        import team_tools_db
        players = team_tools_db.pitcher_projections()
        self.render("spreadsheet.html", players=players, cat="pitcher", username=self.username)

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
                    league_no=league_no, team_a=team_a, team_b=team_b, trade_result=trade_result,
                    username=self.username)

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
                    projected_standings=projected_standings, team_name=team_name, elapsed=elapsed,
                    username=self.username)

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
        self.redirect(api_connector.request_auth(GUID_REDIRECT_PATH))

class GuidRedirect(Handler):
    def render_guid_redirect(self, code):
        oauth_token = api_connector.get_token(code, GUID_REDIRECT_PATH)
        oauth_token_dict = json.loads(oauth_token)
        guid = oauth_token_dict['xoauth_yahoo_guid']
        yahoo_guid_json = api_connector.get_guid(oauth_token)

        yahoo_guid_dict = json.loads(yahoo_guid_json)
        guid = yahoo_guid_dict['guid']['value']

        self.update_user(user=self.user, yahooGuid=guid)
        self.redirect("/")

    def get(self):
        code = self.request.get('code')
        self.render_guid_redirect(code=code)

    def post(self):
        code = self.request.get('code')
        self.render_guid_redirect(code=code)

class QueryRedirect(Handler):
    def render_query_redirect(self, code):
        oauth_token = api_connector.get_token(code, GUID_REDIRECT_PATH)
        yahoo_guid_json = api_connector.get_guid(oauth_token)
        yahoo_guid_dict = json.loads(yahoo_guid_json)
        guid = yahoo_guid_dict['guid']['value']

        self.redirect(str("http://localhost:8080?code=" + code))

    def get(self):
        code = self.request.get('code')
        self.render_query_redirect(code=code)

    # def post(self):
    #     code = self.request.get('code')
    #     self.render_query_redirect(code=code)

class GuidLocalhost(Handler):
    def render_guid_locahost(self, code):
        self.redirect(str('http://localhost:8080/guid_redirect?code=' + code))

    def get(self):
        code = self.request.get('code')
        self.render_guid_locahost(code=code)

class QueryLocalhost(Handler):
    def render_guery_locahost(self, code):
        self.redirect(str('http://localhost:8080/query_redirect?code=' + code))

    def get(self):
        code = self.request.get('code')
        self.render_guery_locahost(code=code)

class Registration(Handler):
    def render_registration(self, username="", email="", username_error="",
                            password_error="", pass_verify_error="", email_error="",
                            link_yahoo=""):
        self.render("registration.html", username=username, email=email,
                    username_error=username_error, password_error=password_error,
                    pass_verify_error=pass_verify_error, email_error=email_error,
                    link_yahoo=link_yahoo)

    def get(self):
        self.render_registration()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        pass_verify = self.request.get("pass_verify")
        email = self.request.get("email")
        link_yahoo = True if self.request.get("link_yahoo") == "on" else False

        error = False
        # check password
        if not password: # check if password is blank
            password_error = "Password cannot be empty"
            error = True
        elif not validuser.valid_password(password): # check if password is valid
            password_error = "Invalid Password"
            error = True
        else:
            password_error = ""
        # check password verification
        if not pass_verify: # check if password verification is blank
            pass_verify_error = "Password Verification cannot be empty"
            error = True
        elif password != pass_verify: # check if password matches password verification
            pass_verify_error = "Passwords do not match"
            error = True
        else:
            pass_verify_error = ""
        # check username
        if not username: # check if username is blank
            username_error = "Username cannot be empty"
            error = True
        elif not validuser.valid_username(username): # check if username if valid
            username_error = "Invalid Username"
            error = True
        elif caching.cached_check_username(username): # check if username is unique
            username_error = "That username is taken"
            error = True
        else:
            username_error = ""
        # check email
        if not email: # check if email is blank
            email_error = ""
        elif not validuser.valid_email(email): # check if email is valid
            email_error = "Invalid Email"
            error = True
        else:
            email_error = ""
        # see if any errors returned
        if not error:
            username = username
            password = hashing.make_pw_hash(username, password) # hash password for storage in db

            self.store_user(username, password, email)
            if link_yahoo:
                self.redirect(api_connector.request_auth(GUID_REDIRECT_PATH))

        else:
            self.render_registration(username, email, username_error, password_error,
                                     pass_verify_error, email_error, link_yahoo)

class Login(Handler):
    def render_login(self, username="", error=""):
        self.render("login.html", username=self.username, error=error)

    def get(self):
        self.render_login()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        if not caching.cached_check_username(username):
            error = "Invalid login"
        else:
            user_id = caching.cached_check_username(username)
            user = caching.cached_get_user_by_id(user_id)
            pword = user.password
            salt = pword.split("|")[1]
            if username == user.username:
                if hashing.make_pw_hash(username, password, salt) == pword:
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
        self.redirect('/')

    def get(self):
        self.render_welcome()

class GetLeagues(Handler):
    def get(self):
        yql_query(path, oauth_token)
        self.redirect(api_connector.request_auth(GUID_REDIRECT_PATH))

class User(Handler):
    def render_user(self, link_yahoo=None, refresh_token=None):
        self.render("user.html", username=self.username, link_yahoo=link_yahoo, refresh_token=refresh_token)

    def get(self):
        link_yahoo = api_connector.request_auth(GUID_REDIRECT_PATH)
        user = self.user
        print "$$$$$$$$$$$$$$$$$"
        print user.username
        print user.refresh_token
        # refresh_token = api_connector.check_token_expiration(user, "/user")
        refresh_token = user.yahooGuid
        self.render_user(link_yahoo, refresh_token)

class CodeAuth(Handler):
    def render_code_handler(self, code):
        # print "Code: " + code
        # print "Redirect: " + GUID_REDIRECT_PATH
        self.redirect(api_connector.get_token(code, GUID_REDIRECT_PATH))

    def get(self):
        code = self.request.get("code")
        self.render_code_handler(code)
# TODO: fix
class GetToken(Handler):
    def render_code_handler(self, code):
        # print "Code: " + code
        # print "Redirect: " + GUID_REDIRECT_PATH
        token_json = api_connector.get_token(code, GUID_REDIRECT_PATH)
        token_dict = json.loads(token_json)
        yahoo_guid = token_dict['xoauth_yahoo_guid']
        access_token = token_dict['access_token']
        refresh_token = token_dict['refresh_token']
        token_expiration = (datetime.datetime.now() +
                            datetime.timedelta(seconds=token_dict['expires_in']))
        self.update_user(self.user, yahooGuid=yahoo_guid, access_token=access_token,
                         refresh_token=refresh_token, token_expiration=token_expiration)
        self.redirect("/user")

    def get(self):
        code = self.request.get("code")
        self.render_code_handler(code)
# TODO: fix
class RefreshToken(Handler):
    def render_code_handler(self):
        # print "Code: " + code
        # print "Redirect: " + GUID_REDIRECT_PATH
        # token_json = api_connector.get_token(code, GUID_REDIRECT_PATH)
        # print token_json
        # token_dict = json.loads(token_json)
        # print token_dict
        # self.redirect()
        self.redirect(api_connector.check_token_expiration(self.user, "/user"))

    def get(self):
        self.render_code_handler()

# routing
app = webapp2.WSGIApplication([
    ('/', MainHandler),

    # user handling
    ('/registration/?', Registration),
    ('/login/?', Login),
    ('/logout/?', Logout),
    ('/welcome/?', Welcome),
    ('/user/?', User),

    # yahoo api
    ('/oauth/?', Oauth),
    ('/guid_redirect/?', GuidRedirect),
    ('/query_redirect/?', QueryRedirect),
    ('/localhost_guid/?', GuidLocalhost),
    ('/localhost_query/?', QueryLocalhost),
    ('/get_leagues/?', GetLeagues),
    ('/code_auth/?', CodeAuth),
    ('/get_token/?', GetToken),
    ('/refresh_token/?', RefreshToken),
    

    # projections
    ('/batting_projections/?', BattingProjections),
    ('/pitching_projections/?', PitchingProjections),

    # team tools
    ('/team_tools_html/?', TeamToolsHTML),
    ('/team_tools_db/?', TeamToolsDB),
    ('/update_projections/?', UpdateProjections)
    ], debug=True)

# authorization paths
basic_auth_paths = [ # must be logged in as basic user to access these links
    '/fpprojb',
    '/fpprojb/',
    '/fpprojp',
    '/fpprojp/'
    # '/new_post',
    # '/new_post/',
    # '/modify_post',
    # '/modify_post/',
    # '/post/<post_id:\d+>/edit',
    # '/post/<post_id:\d+>/delete'
]

commissioner_auth_paths = [ # must be logged in as power_user to access these links
    '/test'
]

power_user_auth_paths = [ # must be logged in as power_user to access these links
    '/fpprojbdatapull',
    '/fpprojbdatapull/',
    '/fpprojpdatapull',
    '/fpprojpdatapull/'
]

admin_auth_paths = [ # must be logged in as admin to access these links
    '/admin',
    '/admin/'
]

auth_paths = basic_auth_paths + commissioner_auth_paths + power_user_auth_paths + admin_auth_paths
