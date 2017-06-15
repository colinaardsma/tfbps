import webapp2
import api_connector
import jinja2
import hashing
import os
import caching
import webbrowser
import fa_vs_team

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

class FaRater(Handler):
    def render_fa_rater(self, league_no="", team_name="", player_name=""):
        if league_no == "" or team_name == "":
            top_fa = None
        else:
            top_fa = fa_vs_team.fa_vs_team(league_no, team_name)
            top_fa = top_fa.replace("\n", "<br />")
        if player_name == "":
            single_player = None
        else:
            single_player = fa_vs_team.single_player_rater(player_name)
        self.render("fa_rater.html", top_fa=top_fa, single_player=single_player)

    def get(self):
        self.render_fa_rater()

    def post(self):
        league_no = self.request.get("league_no")
        team_name = self.request.get("team_name")
        player_name = self.request.get("player_name")
        self.render_fa_rater(league_no=league_no, team_name=team_name, player_name=player_name)

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
    ('/fa_rater/?', FaRater)
    ], debug=True)
    