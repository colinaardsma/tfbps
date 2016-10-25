import os, webapp2, math, re, json, datetime #import stock python methods
import jinja2 #need to install jinja2 (not stock)
import htmlParsing, dbmodels, gqlqueries, caching, jsonData, validuser, hashing #import python files I've made
from dbmodels import Users
# import time

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

    def initialize(self, *a, **kw):
        """
            A filter to restrict access to certain pages when not logged in.
            If the request path is in the global auth_paths list, then the user
            must be signed in to access the path/resource.
        """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        c = self.request.cookies.get('user') #pull cookie value
        uid = ""
        if c:
            uid = hashing.check_secure_val(c)

        self.user = uid and Users.get_by_id(int(uid))

        if not self.user and self.request.path in auth_paths:
            self.redirect('/login')

class MainHandler(Handler):
    def render_spreadsheet(self):
        self.render("home.html")

    def get(self):
        self.render_spreadsheet()

class Registration(Handler):
    def render_reg(self, username="", email="", usernameError="", passwordError="", passVerifyError="", emailError=""):
        self.render("registration.html", username=username, email=email, usernameError=usernameError, passwordError=passwordError, passVerifyError=passVerifyError, emailError=emailError)

    def get(self):
        self.render_reg()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        passVerify = self.request.get("passVerify")
        email = self.request.get("email")
        error = False

        #check password
        if not password: #check if password is blank
            passwordError = "Password cannot be empty"
            error = True
        elif not validuser.valid_password(password): #check if password is valid
            passwordError = "Invalid Password"
            error = True
        else:
            passwordError = ""
        #check password verification
        if not passVerify: #check if password verification is blank
            passVerifyError = "Password Verification cannot be empty"
            error = True
        elif password != passVerify: #check if password matches password verification
            passVerifyError = "Passwords do not match"
            error = True
        else:
            passVerifyError = ""
        #check username
        if not username: #check if username is blank
            usernameError = "Username cannot be empty"
            error = True
        elif not validuser.valid_username(username): #check if username if valid
            usernameError = "Invalid Username"
            error = True
        elif caching.cached_check_username(username): #check if username is unique
            usernameError = "That username is taken"
            error = True
        else:
            usernameError = ""
        #check email
        if not email: #check if email is blank
            emailError = ""
        elif not validuser.valid_email(email): #check if email is valid
            emailError = "Invalid Email"
            error = True
        else:
            emailError = ""
        #see if any errors returned
        if error == False:
            username = username
            password = hashing.make_pw_hash(username, password) #hash password for storage in db
            user = Users(username=username, password=password, email=email) #create new blog object named post
            user.put() #store post in database
            user_id = user.key().id()
            self.response.headers.add_header('Set-Cookie', 'user=%s' % hashing.make_secure_val(user_id)) #hash user id for use in cookie
            caching.cached_user_by_name(username, True) #direct cached_posts to update cache
            caching.cached_check_username(username, True) #direct cached_posts to update cache
            self.redirect('/welcome')
        else:
            self.render_reg(username, email, usernameError, passwordError, passVerifyError, emailError)

class Login(Handler):
    def render_login(self, username="", error=""):
        self.render("login.html", username=username, error=error)

    def get(self):
        self.render_login()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        if not caching.cached_check_username(username):
            error = "Invalid login"
        else:
            user_id = caching.cached_check_username(username)
            user_id = int(user_id)
            u = Users.get_by_id(user_id)
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
            self.response.headers.add_header('Set-Cookie', 'user=%s' % hashing.make_secure_val(user_id)) #hash user id for use in cookie
            self.redirect('/welcome')

class Logout(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user=""; expires=Thu, 01-Jan-1970 00:00:10 GMT') #clear cookie
        self.redirect('/registration')

class Welcome(Handler):
    def render_welcome(self):
        c = self.request.cookies.get('user') #pull cookie value
        usr = hashing.get_user_from_cookie(c)

        self.redirect('/')

    def get(self):
        self.render_welcome()


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

    #user handling
    ('/registration', Registration),
    ('/login', Login),
    ('/logout', Logout),
    ('/welcome', Welcome),

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

auth_paths = [ #must be logged in to access these links
    '/admin',
    '/admin/',
    '/fpbdatapull',
    '/fpbdatapull/',
    '/fppdatapull',
    '/fppdatapull/'
    # '/new_post',
    # '/new_post/',
    # '/modify_post',
    # '/modify_post/',
    # '/post/<post_id:\d+>/edit',
    # '/post/<post_id:\d+>/delete'
]
