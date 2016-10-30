import os, webapp2, math, re, json, datetime #import stock python methods
import jinja2 #need to install jinja2 (not stock)
import htmlParsing, dbmodels, gqlqueries, caching, jsonData, validuser, hashing, dbmodification, rssparsing, zscore #import python files I've made
from dbmodels import Users
import time

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

    def __init__(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        c = self.request.cookies.get('user') #pull cookie value
        uid = ""
        if c:
            uid = hashing.check_secure_val(c)

        self.user = uid and caching.cached_get_user_by_id(uid)
        self.auth = self.user and caching.cached_get_authorization(self.user.username)

        if not self.user and self.request.path in auth_paths:
            self.redirect('/login')

    # check user authorization vs authorization lists
    def get_auth(self, auth):
        if auth != "admin" and self.request.path in admin_auth_paths:
            self.redirect('/login')
        elif (auth != "admin" and auth != "power_user") and self.request.path in power_user_auth_paths:
            self.redirect('/login')
        elif (auth != "admin" and auth != "power_user" and auth != "commissioner") and self.request.path in commissioner_auth_paths:
            self.redirect('/login')
        elif (auth != "admin" and auth != "power_user" and auth != "commissioner" and auth != "basic") and self.request.path in basic_auth_paths:
            self.redirect('/login')
        else:
            self.request.path

class MainHandler(Handler):
    def render_main(self):
        #pull username
        if self.user:
            user = self.user.username # get username from user object
            self.get_auth(self.auth) # check to see if authorized to view page
        else:
            user = ""

        fakeBbArticle = rssparsing.get_fakebb_rss_content(0)
        yahooArticle = rssparsing.get_yahoo_rss_content(0)

        # self.render("home.html", user=user, fakeBbArticle=fakeBbArticle, yahooArticle=yahooArticle)
        self.write(zscore.get_batter_z_score(caching.cached_get_fpprojb()))

    def get(self):
        self.render_main()

class Registration(Handler):
    def render_reg(self, username="", email="", usernameError="", passwordError="", passVerifyError="", emailError=""):
        #pull username
        if self.user:
            user = self.user.username # get username from user object
            self.get_auth(self.auth) # check to see if authorized to view page
        else:
            user = ""

        self.render("registration.html", username=username, email=email, usernameError=usernameError, passwordError=passwordError, passVerifyError=passVerifyError, emailError=emailError, user=user)

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
            authorization = "basic"
            user = Users(username=username, password=password, email=email, authorization=authorization) #create new blog object named post
            user.put() #store post in database
            user_id = user.key().id()
            self.response.headers.add_header('Set-Cookie', 'user=%s' % hashing.make_secure_val(user_id)) #hash user id for use in cookie

            time.sleep(.2) #ewait 2/10 of a second while post is entered into db

            #update cache
            caching.cached_user_by_name(username, True)
            caching.cached_check_username(username, True)
            caching.cached_get_users(True)

            self.redirect('/welcome')
        else:
            self.render_reg(username, email, usernameError, passwordError, passVerifyError, emailError)

class Login(Handler):
    def render_login(self, username="", error=""):
        #pull username
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

class FPProjBatter(Handler):
    def render_spreadsheet(self):
        #pull username
        if self.user:
            user = self.user.username # get username from user object
            self.get_auth(self.auth) # check to see if authorized to view page
        else:
            user = ""

        cat = "batter"
        players = caching.cached_get_fpprojb()
        dataDate = datetime.datetime(1980, 1, 1)
        for p in players:
            if p.last_modified > dataDate:
                dataDate = p.last_modified

        self.render("spreadsheet.html", players=players, cat=cat, dataDate=dataDate, user=user)

    def get(self):
        self.render_spreadsheet()

class FPProjPitcher(Handler):
    def render_spreadsheet(self, cat=""):
        #pull username
        if self.user:
            user = self.user.username # get username from user object
            self.get_auth(self.auth) # check to see if authorized to view page
        else:
            user = ""

        cat = "pitcher"
        players = caching.cached_get_fpprojp()
        dataDate = datetime.datetime(1980, 1, 1)
        for p in players:
            if p.last_modified > dataDate:
                dataDate = p.last_modified

        self.render("spreadsheet.html", players=players, cat=cat, dataDate=dataDate, user=user)

    def get(self):
        self.render_spreadsheet()

class FPBDataPull(Handler):
    def render_pull(self):
        if self.auth == "admin": #restrict access to admins only
            #this will only work for fantasypros.com
            URL = "http://www.fantasypros.com/mlb/projections/hitters.php" #currently does not work with https
            htmlParsing.fpprojbdatapull(URL)
            self.redirect("/fpprojb")
        else:
            self.redirect("/login")

    def get(self):
        self.render_pull()

class FPPDataPull(Handler):
    def render_pull(self):
        if self.auth == "admin": #restrict access to admins only
            #this will only work for fantasypros.com
            URL = "http://www.fantasypros.com/mlb/projections/pitchers.php" #currently does not work with https
            htmlParsing.fpprojpdatapull(URL)
            self.redirect("/fpprojp")
        else:
            self.redirect("/login")

    def get(self):
        self.render_pull()

class Flush(Handler):
    def get(self, key=""):
        caching.flush(key)
        # self.write(key)
        self.redirect("/admin")

class admin(Handler):
    def render_admin(self, userConfirmation=""):
        #pull username
        if self.user:
            user = self.user.username # get username from user object
            self.get_auth(self.auth) # check to see if authorized to view page
        else:
            user = ""

        #pull list of all users
        users = caching.cached_get_users()

        self.render("admin.html", user=user, users=users, userConfirmation=userConfirmation)

    def get(self, userConfirmation=""):
        self.render_admin(userConfirmation=userConfirmation)

    def post(self):
        username = self.request.get("username")
        authorization = self.request.get("authorization")
        userConfirmation = username, authorization

        #set authorization
        dbmodification.set_authorization(username, authorization)

        # time.sleep(.1) #ewait 1/10 of a second while post is entered into db

        #update cache
        caching.cached_user_by_name(username, True)
        caching.cached_check_username(username, True)
        caching.cached_get_users(True)
        caching.cached_get_authorization(username, True)

        self.render_admin(userConfirmation=userConfirmation)

class jsonHandler(Handler):
    def render_json(self, data=""):
        jData = jsonData.jsonData(data)

        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8' #set content-type to json and charset to UTF-8
        self.write(jData) #write json data to page

    def get(self, data=""):
        self.render_json(data)

#routing
app = webapp2.WSGIApplication([
    ('/', MainHandler),

    #user handling
    ('/registration', Registration),
    ('/login', Login),
    ('/logout', Logout),
    ('/welcome', Welcome),

    #stat viewing
    ('/fpprojb', FPProjBatter),
    ('/fpprojp', FPProjPitcher),
    # ('/fp', FP),

    #stat retrieval
    ('/fpprojbdatapull', FPBDataPull),
    ('/fpprojpdatapull', FPPDataPull),

    #memcache flushing
    webapp2.Route('/flush<key:[a-z0-9-_]+projb>', Flush), #batter projections
    webapp2.Route('/flush<key:[a-z0-9-_]+projp>', Flush), #pitcher projections
    # webapp2.Route('/flush<key:[a-z0-9-_]+rosb>', Flush), #batter rest of season
    # webapp2.Route('/flush<key:[a-z0-9-_]+rosp>', Flush), #pitcher rest of season

    #below flushes user memcache, is this necessary?
    # webapp2.Route('/flush<key:[a-z0-9-_]+getUser>', Flush), #user objects
    # webapp2.Route('/flush<key:[a-z0-9-_]+checkUsername>', Flush), #usernames
    # webapp2.Route('/flush<key:users>', Flush), #all user data


    #admin page
    ('/admin', admin),

    #json export
    webapp2.Route('/<data:[a-z0-9-_]+projb>.json', jsonHandler),
    webapp2.Route('/<data:[a-z0-9-_]+projp>.json', jsonHandler)
    # webapp2.Route('/<data:[a-z0-9-_]+rosb>.json', jsonHandler),
    # webapp2.Route('/<data:[a-z0-9-_]+rosp>.json', jsonHandler)

], debug=True)

#authorization paths
basic_auth_paths = [ #must be logged in as basic user to access these links
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

commissioner_auth_paths = [ #must be logged in as power_user to access these links
    '/test'
]

power_user_auth_paths = [ #must be logged in as power_user to access these links
    '/fpprojbdatapull',
    '/fpprojbdatapull/',
    '/fpprojpdatapull',
    '/fpprojpdatapull/'
]

admin_auth_paths = [ #must be logged in as admin to access these links
    '/admin',
    '/admin/'
]

auth_paths = basic_auth_paths + commissioner_auth_paths + power_user_auth_paths + admin_auth_paths
