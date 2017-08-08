import os
import webapp2
import api_connector
import jinja2
import hashing
import caching
import time
import logging
import html_parser

# setup jinja2
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),
                            'templates') # set template_dir to main.py dir(current dir)/templates
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True) # set jinja2's working directory to template_dir

# define some functions that will be used by all pages
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw): # simplifies self.response.out.write to self.write
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params): # creates the string that will render html using jinja2 with html template named template and parameters named params
        t = JINJA_ENV.get_template(template)
        return t.render(params)

    def render(self, template, **kw): # writes the html string created in render_str to the page
        self.write(self.render_str(template, **kw))

    def __init__(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        c = self.request.cookies.get('user') # pull cookie value
        uid = ""
        if c:
            uid = hashing.check_secure_val(c)

        self.user = uid and caching.cached_get_user_by_id(uid)
        self.auth = self.user and caching.cached_get_authorization(self.user.username)

        # if not self.user and self.request.path in auth_paths:
        # if not self.user:
        #     self.redirect('/login')

    # # check user authorization vs authorization lists
    # def get_auth(self, auth):
    #     if auth != "admin" and self.request.path in admin_auth_paths:
    #         self.redirect('/login')
    #     elif (auth != "admin" and auth != "power_user") and self.request.path in power_user_auth_paths:
    #         self.redirect('/login')
    #     elif (auth != "admin" and auth != "power_user" and auth != "commissioner") and self.request.path in commissioner_auth_paths:
    #         self.redirect('/login')
    #     elif (auth != "admin" and auth != "power_user" and auth != "commissioner" and auth != "basic") and self.request.path in basic_auth_paths:
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
        # self.render("home.html", user=user, fakeBbArticle=fakeBbArticle, yahooArticle=yahooArticle)
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
        if league_no == "" or team_name == "":
            top_fa = None
        else:
            top_fa = team_tools_html.fa_finder(league_no, team_name)
            team_name = top_fa['Team Name']
        # single player lookup
        if player_name == "":
            single_player = None
        else:
            single_player = team_tools_html.single_player_rater(player_name)
        # trade analyzer
        if (league_no == "" and team_a == "" and not team_a_players and team_b == ""
                and not team_b_players):
            team_a = None
            team_b = None
            trade_result = None
        elif league_no != "" and team_a_name != "" and team_b_name != "":
            team_a = html_parser.get_single_yahoo_team(league_no, team_a_name)
            team_b = html_parser.get_single_yahoo_team(league_no, team_b_name)
            trade_result = None
        elif league_no != "" and team_a and team_b and team_a_players and team_b_players:
            trade_result = team_tools_html.trade_analyzer(league_no, team_a, team_a_players,
                                                          team_b, team_b_players)
        # final stanings projection
        if league_no == "" or (league_no != "" and team_name != "") or (team_a and team_b):
            projected_standings = None
        else:
            projected_standings = team_tools_html.final_standing_projection(league_no)

        self.render("team_tools_html.html", top_fa=top_fa, single_player=single_player,
                    projected_standings=projected_standings, team_name=team_name,
                    team_a=team_a, team_b=team_b, trade_result=trade_result)

    def get(self):
        self.render_fa_rater()

    def post(self):
        league_no = self.request.get("league_no")
        team_name = self.request.get("team_name")
        player_name = self.request.get("player_name")
        team_a = self.request.get("team_a")
        team_a_name = self.request.get("team_a_name")
        team_a_players = self.request.get("team_a_players")
        team_b = self.request.get("team_b")
        team_b_name = self.request.get("team_b_name")
        team_b_players = self.request.get("team_b_players")
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
    def render_redirect(self):
        self.render("home/html")

    def get(self):
        self.render_redirect()

# routing
app = webapp2.WSGIApplication([
    ('/', MainHandler),

    # user handling
    ('/oauth/?', Oauth),
    ('/redirect/?', Redirect),
    ('/batting_projections/?', BattingProjections),
    ('/pitching_projections/?', PitchingProjections),
    ('/team_tools_html/?', TeamToolsHTML),
    ('/team_tools_db/?', TeamToolsDB),
    ('/update_projections/?', UpdateProjections)
    ], debug=True)
    