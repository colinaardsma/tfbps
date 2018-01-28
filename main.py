import os
import ast
import time
import datetime
import logging
import json
import webapp2
import api_connector
import jinja2
from operator import itemgetter
import socket
import cgi
import urllib2
import hashing
import caching
import html_parser
import validuser
import db_models
import queries
import yql_queries
import cgi
import pprint
import sgp_calc
import heapq

# setup jinja2
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),
                            'templates') # set template_dir to main.py dir(current dir)/templates
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True) # set jinja2's working directory to template_dir

PROD_REDIRECT_PATH = "/get_token"
LOCALHOST_REDIRECT_PATH = "/localhost_token"
GUID_REDIRECT_PATH = LOCALHOST_REDIRECT_PATH

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
        self.username = ""
        if self.user:
            self.username = self.user.username

    def get_user(self):
        user_cookie = self.request.cookies.get('user') # pull cookie value

        self.user_id = ""
        if user_cookie:
            self.user_id = hashing.check_secure_val(user_cookie)

        self.user = self.user_id and caching.cached_get_user_by_id(self.user_id)
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

    def store_user(self, username, password, email, location, guid=None):
        db_models.store_user(username, password, email, location, guid)

        user = caching.cached_user_by_name(username)
        user_id = user.key().id()
        self.response.headers.add_header('Set-Cookie', 'user=%s' %
                                         hashing.make_secure_val(user_id)) # hash user id for use in cookie
        # self.redirect('/welcome')

    def set_cookie(self, user_id):
        self.response.headers.add_header('Set-Cookie', 'user=%s' %
                                         hashing.make_secure_val(user_id)) # hash user id for use in cookie

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
        # if datetime.datetime.now() > datetime.datetime(2017,10,1):
        #     self.render("offseason.html", username=self.username)
        # else:
        self.render_batting_projections()

class PitchingProjections(Handler):
    def render_pitching_projections(self):
        import team_tools_db
        players = team_tools_db.pitcher_projections()
        self.render("spreadsheet.html", players=players, cat="pitcher", username=self.username)

    def get(self):
        # if datetime.datetime.now() > datetime.datetime(2017,10,1):
        #     self.render("offseason.html", username=self.username)
        # else:
        self.render_pitching_projections()

class TeamToolsHTML(Handler):
    def render_fa_rater(self, league_no="", team_name="", player_name="", team_a={},
                        team_a_name="", team_a_players=[], team_b={}, team_b_name="",
                        team_b_players=[], trade_result={}, all_keepers_key="",
                        redirect=""):
        # fa rater
        if league_no != "" and team_name != "":
            import team_tools_html
            top_fa = team_tools_html.fa_finder(league_no, team_name)
            team_name = top_fa['Team Name']
            # print top_fa
        else:
            top_fa = None
        # single player lookup
        if player_name != "":
            import team_tools_html
            single_player = team_tools_html.single_player_rater(player_name)
        else:
            single_player = None
        # trade analyzer
        if league_no != "" and team_a_name != "" and team_b_name != "":
            team_a = html_parser.get_single_yahoo_team(league_no, team_a_name)
            team_b = html_parser.get_single_yahoo_team(league_no, team_b_name)
            league_no = league_no
        elif league_no != "" and team_a and team_b and team_a_players and team_b_players:
            import team_tools_html
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
            import team_tools_html
            projected_standings = team_tools_html.final_standing_projection(league_no)
        else:
            projected_standings = None

        # keepers
        if all_keepers_key == "":
            keepers = None
        else:
            import team_tools_html
            keepers = team_tools_html.get_keepers(all_keepers_key, self.user, self.user_id,
                                                  redirect)

        self.render("team_tools_html.html", top_fa=top_fa, single_player=single_player,
                    projected_standings=projected_standings, team_name=team_name,
                    league_no=league_no, team_a=team_a, team_b=team_b, trade_result=trade_result,
                    username=self.username, all_keepers_key=all_keepers_key, keepers=keepers)

    def get(self):
        # if datetime.datetime.now() > datetime.datetime(2017,10,1):
        #     self.render("offseason.html", username=self.username)
        # else:
        redirect = "/team_tools_html"
        self.render_fa_rater(redirect=redirect)

    def post(self):
        redirect = "/team_tools_html"
        league_no = self.request.get("league_no")
        team_name = self.request.get("team_name")
        player_name = self.request.get("player_name")
        team_a = self.request.get("team_a")
        team_a_name = self.request.get("team_a_name")
        team_a_players = self.request.POST.getall("team_a_players")
        team_b = self.request.get("team_b")
        team_b_name = self.request.get("team_b_name")
        team_b_players = self.request.POST.getall("team_b_players")
        all_keepers_key = self.request.get("all_keepers_key")
        self.render_fa_rater(league_no=league_no, team_name=team_name, player_name=player_name,
                             team_a=team_a, team_a_name=team_a_name, team_a_players=team_a_players,
                             team_b=team_b, team_b_name=team_b_name, team_b_players=team_b_players,
                             all_keepers_key=all_keepers_key, redirect=redirect)

class TeamToolsDB(Handler):
    def render_team_tools_db(self, league_no="", team_name="", player_name="", update="",
                             fa_league_key="", proj_league_key="", all_keepers_key="",
                             proj_keepers_key="", current_leagues=None, redirect=""):
        # update projections
        if update == "":
            elapsed = None
        # else:
        #     start = time.time()
        #     team_tools_db.pull_batters()
        #     team_tools_db.pull_pitchers()
        #     # team_tools_db.pull_players()
        #     end = time.time()
        #     elapsed = end - start
        # # fa rater
        # # if league_no == "" or team_name == "":
        if fa_league_key == "":
            top_fa = None
        else:
            import team_tools_db
            top_fa = team_tools_db.fa_finder(fa_league_key, self.user, self.user_id, redirect)
            team_name = top_fa['Team Name']
        # single player lookup
        if player_name == "":
            single_player = None
        else:
            import team_tools_db
            start = time.time()
            single_player = team_tools_db.single_player_rater(player_name)
            end = time.time()
            elapsed = end - start
            logging.info("\r\n***************\r\nBatter Creation in %f seconds", elapsed)

        # final stanings projection
        # if league_no == "" or (league_no != "" and team_name != ""):
        if proj_league_key == "":
            projected_standings = None
        else:
            import team_tools_db
            projected_standings = team_tools_db.final_standing_projection(proj_league_key,
                                                                          self.user, self.user_id,
                                                                          redirect)

        # keepers
        if all_keepers_key == "":
            all_keepers = None
        else:
            import team_tools_db
            all_keepers = team_tools_db.get_keeper_costs(all_keepers_key, self.user, self.user_id,
                                                         redirect)

        if proj_keepers_key == "":
            proj_keepers = None
        else:
            import team_tools_db
            proj_keepers = team_tools_db.get_projected_keepers(proj_keepers_key, self.user,
                                                               self.user_id, redirect)

        self.render("team_tools_db.html", top_fa=top_fa, single_player=single_player,
                    projected_standings=projected_standings, team_name=team_name, elapsed=elapsed,
                    username=self.username, fa_league_key=fa_league_key,
                    proj_league_key=proj_league_key, all_keepers_key=all_keepers_key,
                    proj_keepers_key=proj_keepers_key, current_leagues=current_leagues,
                    all_keepers=all_keepers, proj_keepers=proj_keepers)

    def get(self):
        # if datetime.datetime.now() > datetime.datetime(2017,10,1):
        #     self.render("offseason.html", username=self.username)
        # else:
        redirect = "/team_tools_db"
        league_list = None
        current_leagues = None
        if self.user:
            league_list = yql_queries.get_leagues(self.user, self.user_id, redirect)
            current_leagues = yql_queries.get_current_leagues(league_list)

        self.render_team_tools_db(current_leagues=current_leagues, redirect=redirect)

    def post(self):
        redirect = "/team_tools_db"
        league_no = self.request.get("league_no")
        team_name = self.request.get("team_name")
        player_name = self.request.get("player_name")
        update = self.request.get("update")
        fa_league_key = self.request.get("fa_league_key")
        proj_league_key = self.request.get("proj_league_key")
        proj_keepers_key = self.request.get("proj_keepers_key")
        all_keepers_key = self.request.get("all_keepers_key")
        self.render_team_tools_db(league_no=league_no, team_name=team_name, redirect=redirect,
                                  player_name=player_name, update=update, fa_league_key=fa_league_key,
                                  proj_league_key=proj_league_key, proj_keepers_key=proj_keepers_key,
                                  all_keepers_key=all_keepers_key)

class UpdateProjections(Handler):
    def render_update_projections(self, elapsed=""):
        self.render

    def get(self):
        start = time.time()
        import team_tools_db
        # team_tools_db.pull_batters(batting_csv)
        # team_tools_db.pull_pitchers(pitching_csv)
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
        yahoo_guid_json = yql_queries.get_guid(oauth_token)

        yahoo_guid_dict = json.loads(yahoo_guid_json)
        guid = yahoo_guid_dict['guid']['value']

        db_models.update_user(user=self.user, user_id=self.user_id, yahooGuid=guid)
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
        yahoo_guid_json = yql_queries.get_guid(oauth_token)
        yahoo_guid_dict = json.loads(yahoo_guid_json)
        guid = yahoo_guid_dict['guid']['value']

        self.redirect(str("http://localhost:8080?code=" + code))

    def get(self):
        code = self.request.get('code')
        self.render_query_redirect(code=code)

    # def post(self):
    #     code = self.request.get('code')
    #     self.render_query_redirect(code=code)

class TokenLocalhost(Handler):
    def render_guid_locahost(self, code):
        self.redirect(str('http://localhost:8080/get_token?code=' + code))

    def get(self):
        code = self.request.get('code')
        self.render_guid_locahost(code=code)

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
        username = self.request.get("username").lower()
        password = self.request.get("password")
        pass_verify = self.request.get("pass_verify")
        email = self.request.get("email")
        link_yahoo = self.request.get("link_yahoo")
        # link_yahoo = True if self.request.get("link_yahoo") == "on" else False

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
            ip_address = self.request.remote_addr
            url = "https://ipinfo.io/" + ip_address + "/json"
            request = urllib2.Request(url)
            content = urllib2.urlopen(request)
            ip_address_json = content.read()
            ip_address_dict = json.loads(ip_address_json)
            location = None
            if 'loc' in ip_address_dict:
                location = ip_address_dict['loc']

            self.store_user(username, password, email, location)
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
        username = self.request.get("username").lower()
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
            self.response.headers.add_header('Set-Cookie', 'user=%s' %
                                             hashing.make_secure_val(user_id)) # hash user id for use in cookie
            self.redirect('/welcome')

class Logout(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie',
                                         'user=""; expires=Thu, 01-Jan-1970 00:00:10 GMT') #clear cookie
        self.redirect('/registration')

class Welcome(Handler):
    def render_welcome(self):
        self.redirect('/')

    def get(self):
        self.render_welcome()

class TestPage(Handler):
    def render_welcome(self):
        self.redirect('/')

    def get(self):
        print ":::::::::::::::::::::::"
        league_key = "370.l.5091"
        redirect = "/get_leagues"
        # auction_results = yql_queries.get_auction_results(league_key, self.user, self.user_id, redirect)
        # print auction_results
        # rosters = yql_queries.get_current_rosters(league_key, self.user, self.user_id, redirect)
        # print rosters
        # transactions = yql_queries.get_league_transactions(league_key, self.user, self.user_id, redirect)
        # print transactions
        # keepers = yql_queries.get_keepers(league_key, self.user, self.user_id, redirect)
        # pprint.pprint(keepers)
        # import team_tools_db
        # proj_keepers = team_tools_db.get_projected_keepers(league_key, self.user, self.user_id, redirect)
        # pprint.pprint(proj_keepers)
        settings = yql_queries.get_league_settings(league_key, self.user, self.user_id, redirect)
        pprint.pprint(settings)
        # leagues = yql_queries.get_leagues(self.user, self.user_id, redirect)
        # pprint.pprint(leagues)

        # for league in league_list:

        # api_connector.check_token_expiration(self.user, self.user_id, "/get_leagues")
        # current_year_query_path = "/users;use_login=1/games;game_keys=mlb/leagues"
        # current_year_query_json = api_connector.yql_query(current_year_query_path,
        #                                                   self.user.access_token)
        # current_year_dict = json.loads(current_year_query_json)
        # current_year_league_key = current_year_dict['fantasy_content']['users']['0']['user'][1]['games']['0']['game'][1]['leagues']['0']['league'][0]['league_key']
        # print "%%%%%%%%%%%%%%%%%%%%%%%%"
        # print current_year_league_key
        # league_settings_dict = yql_queries.get_league_settings(current_year_league_key, self.user.access_token)
        # print league_settings_dict

        # one_year_prior_league_key = yql_queries.get_prev_year_league(current_year_dict)
        # one_year_prior_query_path = "/leagues;league_keys=" + one_year_prior_league_key
        # one_year_prior_json = api_connector.yql_query(one_year_prior_query_path,
        #                                               self.user.access_token)
        # print one_year_prior_json
        # one_year_prior_dict = json.loads(one_year_prior_json)

        # two_years_prior_league_key = yql_queries.get_prev_year_league(one_year_prior_dict)
        # two_years_prior_query_path = "/leagues;league_keys=" + two_years_prior_league_key
        # two_years_prior_json = api_connector.yql_query(two_years_prior_query_path,
        #                                                self.user.access_token)
        # print two_years_prior_json
        # two_years_prior_dict = json.loads(two_years_prior_json)


class User(Handler):
    def render_user(self, elapsed=None, link_yahoo=None):
        self.render("user.html", username=self.username, user=self.user,
                    link_yahoo=link_yahoo, elapsed=elapsed)

    def get(self):
        link_yahoo = api_connector.request_auth(GUID_REDIRECT_PATH)
        self.render_user(link_yahoo=link_yahoo)

    def post(self):
        start = time.time()
        import team_tools_db
        batting_csv = self.request.POST["batting_csv"]
        pitching_csv = self.request.POST["pitching_csv"]
        league = caching.cached_get_leagues_by_league_key(self.user.main_league)
        if isinstance(batting_csv, cgi.FieldStorage):
            team_tools_db.pull_batters(self.user, self.user_id, league, batting_csv)
        if isinstance(pitching_csv, cgi.FieldStorage):
            team_tools_db.pull_pitchers(self.user, self.user_id, league, pitching_csv)
        end = time.time()
        elapsed = end - start
        link_yahoo = api_connector.request_auth(GUID_REDIRECT_PATH)
        self.render_user(elapsed=elapsed, link_yahoo=link_yahoo)

class CodeAuth(Handler):
    def render_code_handler(self, code):
        self.redirect(api_connector.get_token(code, GUID_REDIRECT_PATH))

    def get(self):
        code = self.request.get("code")
        self.render_code_handler(code)

class GetToken(Handler):
    def render_code_handler(self, code):
        token_json = api_connector.get_token(code, GUID_REDIRECT_PATH)
        token_dict = json.loads(token_json)
        yahoo_guid = token_dict['xoauth_yahoo_guid']
        access_token = token_dict['access_token']
        refresh_token = token_dict['refresh_token']
        token_expiration = (datetime.datetime.now() +
                            datetime.timedelta(seconds=token_dict['expires_in']))
        db_models.update_user(self.user, self.user_id, yahooGuid=yahoo_guid,
                              access_token=access_token, refresh_token=refresh_token,
                              token_expiration=token_expiration)
        redirect = "/user"

        self.user = self.user_id and caching.cached_get_user_by_id(self.user_id)
        self.auth = self.user and caching.cached_get_authorization(self.user.username)

        get_leagues(self.user, self.user_id, redirect)
        self.redirect(redirect)

    def get(self):
        code = self.request.get("code")
        self.render_code_handler(code)

class RefreshToken(Handler):
    def get(self):
        api_connector.check_token_expiration(self.user, self.user_id, "/user")

class GetLeagues(Handler):
    def get(self):
        get_leagues(self.user, self.user_id, "/user")
        self.redirect("/user")

def get_leagues(user, user_id, redirect):
    leagues = yql_queries.get_leagues(user, user_id, redirect)
    db_leagues = caching.cached_get_all_leagues()
    user_leagues = caching.cached_get_all_user_leagues_by_user(user)
    batters = caching.cached_get_all_batters()
    batter_fvaaz_list = []
    for batter in batters:
        batter_fvaaz_list.append(batter.fvaaz)
    pitchers = caching.cached_get_all_batters()
    pitcher_fvaaz_list = []
    for pitcher in pitchers:
        pitcher_fvaaz_list.append(pitcher.fvaaz)
    main_league = None
    for league in leagues:
        db_league = [db_lg for db_lg in db_leagues if db_lg.league_key == league['league_key']]
        if not db_league:
            settings = yql_queries.get_league_settings(league['league_key'], user,
                                                       user_id, redirect)
            standings = yql_queries.get_league_standings(league['league_key'], user,
                                                         user_id, redirect)
            results = yql_queries.get_auction_results(league['league_key'], user,
                                                      user_id, redirect)
            sgp = sgp_calc.get_sgp(standings)
            avg_sgp = 0.00
            ops_sgp = 0.00
            drafted_batters_over_one_dollar = (results['total_batters_drafted']
                                               - results['one_dollar_batters'])
            drafted_pitchers_over_one_dollar = (results['total_pitchers_drafted']
                                                - results['one_dollar_pitchers'])

            batter_fvaaz_over_one_dollar = heapq.nlargest(drafted_batters_over_one_dollar,
                                                          batter_fvaaz_list)
            pitcher_fvaaz_over_one_dollar = heapq.nlargest(drafted_pitchers_over_one_dollar,
                                                           pitcher_fvaaz_list)
            total_batter_fvaaz_over_one_dollar = sum(batter_fvaaz_over_one_dollar)
            total_pitcher_fvaaz_over_one_dollar = sum(pitcher_fvaaz_over_one_dollar)

            batter_budget_over_one_dollar = (results['money_spent_on_batters']
                                             - results['one_dollar_batters'])
            pitcher_budget_over_one_dollar = (results['money_spent_on_pitchers']
                                              - results['one_dollar_pitchers'])

            batter_dollar_per_fvaaz = (batter_budget_over_one_dollar
                                       / total_batter_fvaaz_over_one_dollar)
            pitcher_dollar_per_fvaaz = (pitcher_budget_over_one_dollar
                                        / total_pitcher_fvaaz_over_one_dollar)

            b_player_pool_mult = 2.375
            p_player_pool_mult = 4.45

            if 'AVG' in sgp:
                avg_sgp = sgp['AVG']
            if 'OPS' in sgp:
                ops_sgp = sgp['OPS']
            db_models.store_league(settings['Name'], settings['League Key'],
                                   settings['Max Teams'], settings['Max Innings Pitched'],
                                   settings['Batting POS'], settings['Pitching POS'],
                                   settings['Bench POS'], settings['DL POS'],
                                   settings['NA POS'], settings['Prev Year Key'],
                                   settings['Season'], sgp['R'], sgp['HR'], sgp['RBI'],
                                   sgp['SB'], ops_sgp, avg_sgp, sgp['W'], sgp['SV'],
                                   sgp['K'], sgp['ERA'], sgp['WHIP'],
                                   results['total_batters_drafted'],
                                   results['total_pitchers_drafted'],
                                   results['one_dollar_batters'],
                                   results['one_dollar_pitchers'], results['total_money_spent'],
                                   results['money_spent_on_batters'],
                                   results['money_spent_on_pitchers'], results['batter_budget_pct'],
                                   results['pitcher_budget_pct'],
                                   batter_dollar_per_fvaaz, pitcher_dollar_per_fvaaz,
                                   b_player_pool_mult, p_player_pool_mult)
            new_league = db_models.calc_three_year_avgs(settings['League Key'])
            db_models.store_user_league(user, new_league)
        else:
            db_user_league = [usr_lg for usr_lg in user_leagues
                              if usr_lg.league_key == db_lg.league_key
                              for db_lg in db_leagues]
            if not db_user_league:
                db_models.store_user_league(user, db_league[0])
        main_league = league
    db_models.update_user(user, user_id, main_league=main_league['league_key'])

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
    ('/localhost_token/?', TokenLocalhost),
    ('/test_page/?', TestPage),
    ('/code_auth/?', CodeAuth),
    ('/get_token/?', GetToken),
    ('/refresh_token/?', RefreshToken),
    ('/get_leagues/?', GetLeagues),

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
