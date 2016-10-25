import os, webapp2, math, re, json, datetime #import stock python methods
import jinja2 #need to install jinja2 (not stock)
import htmlParsing, dbmodels, gqlqueries, caching, jsonData #import python files I've made
# import time
# from jsonData import jsonData

#setup jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates') #set template_dir to main.py dir(current dir)/templates
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True) #set jinja2's working directory to template_dir

#define some functions that will be used by all pages
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw): #simplifies self.response.out.write to self.write
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params): #creates the string that will render html using jinja2 with html template named template and parameters named params
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw): #writes the html string created in render_str to the page
        self.write(self.render_str(template, **kw))

    # def initialize(self, *a, **kw):
    #     """
    #         A filter to restrict access to certain pages when not logged in.
    #         If the request path is in the global auth_paths list, then the user
    #         must be signed in to access the path/resource.
    #     """
    #     webapp2.RequestHandler.initialize(self, *a, **kw)
    #     c = self.request.cookies.get('user') #pull cookie value
    #     uid = ""
    #     if c:
    #         uid = hashing.check_secure_val(c)
    #
    #     self.user = uid and Users.get_by_id(int(uid))
    #
    #     if not self.user and self.request.path in auth_paths:
    #         self.redirect('/login')

class MainHandler(Handler):
    def render_spreadsheet(self):
        self.render("home.html")

    def get(self):
        self.render_spreadsheet()

class FPBatter(Handler):
    def render_spreadsheet(self):
        cat = "batter"
        players = caching.cached_get_fpb()
        dataDate = datetime.datetime(1980, 1, 1)
        for p in players:
            if p.last_modified > dataDate:
                dataDate = p.last_modified

        self.render("spreadsheet.html", players=players, cat=cat, dataDate=dataDate)

    def get(self):
        self.render_spreadsheet()

class FPPitcher(Handler):
    def render_spreadsheet(self, cat=""):
        cat = "pitcher"
        players = caching.cached_get_fpp()
        dataDate = datetime.datetime(1980, 1, 1)
        for p in players:
            if p.last_modified > dataDate:
                dataDate = p.last_modified

        self.render("spreadsheet.html", players=players, cat=cat, dataDate=dataDate)

    def get(self):
        self.render_spreadsheet()

class FPBDataPull(Handler):
    def render_pull(self):
        #this will only work for fantasypros.com
        URL = "http://www.fantasypros.com/mlb/projections/hitters.php" #currently does not work with https
        htmlParsing.fpbDataPull(URL)
        self.redirect("/fpbatter")

    def get(self):
        self.render_pull()

class FPPDataPull(Handler):
    def render_pull(self):
        #this will only work for fantasypros.com
        URL = "http://www.fantasypros.com/mlb/projections/pitchers.php" #currently does not work with https
        htmlParsing.fppDataPull(URL)
        self.redirect("/fppitcher")

    def get(self):
        self.render_pull()

class admin(Handler):
    def render_admin(self):
        self.render("admin.html")

    def get(self):
        self.render_admin()

class jsonHandler(Handler):
    def render_json(self, data=""):
        # jData = []
        data = data
        jData = jsonData.jsonData(data)

        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8' #set content-type to json and charset to UTF-8
        self.write(jData) #write json data to page

    def get(self, data=""):
        self.render_json(data)

app = webapp2.WSGIApplication([
    ('/', MainHandler),

    #data viewing
    ('/fpbatter', FPBatter),
    ('/fppitcher', FPPitcher),
    # ('/fp', FP),

    #data retrieval
    ('/fpbdatapull', FPBDataPull),
    ('/fppdatapull', FPPDataPull),

    #admin page
    ('/admin', admin),

    #json export
    webapp2.Route('/<data:[a-z0-9-_]+batter>.json', jsonHandler),
    webapp2.Route('/<data:[a-z0-9-_]+pitcher>.json', jsonHandler)

], debug=True)
