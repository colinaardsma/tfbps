from dbmodels import Users, FPProjB, FPProjP, Blog #import Users and Blog classes from python file named dbmodels
from google.appengine.ext import ndb
import logging

# User Queries
def get_user_by_name(usr):
    logging.error("get_user_by_name QUERY")
    """ Get a user object from the db, based on their username """
    # user = ndb.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % usr) #using %s in SQL queries is BAD, never do this
    user = Users.query().filter(Users.username == usr) # .query() = "SELECT *"; .filter("username", usr) = "username = usr"
    if user:
        return user.get()

def get_user_by_id(uid):
    logging.error("get_user_by_uid QUERY")
    """ Get a user object from the db, based on their username """
    user = Users.get_by_id(int(uid))
    if user:
        return user

def check_username(username):
    # n = ndb.GqlQuery("SELECT * FROM Users ORDER BY username") #pull db of userinfo and order by username
    name = Users.query().order(Users.username) # .query() = "SELECT *"; .order("username") = "ORDER BY username"
    for n in name:
        if n.username == username:
            return n.key().id()

def get_users():
    users = Users.query().order(Users.username) # .query() = "SELECT *"; .order("username") = "ORDER BY username"
    u = list(users)
    return u

def get_authorization(username):
    user = Users.query().filter(Users.username == username)
    if user:
        u = user.get()
        return u.authorization

# Statistic Queries
def get_fpprojb():
    logging.error("get_fpb QUERY")
    sheet = FPProjB.query().order(-FPProjB.sgp) # .query() = "SELECT *"; .order("-sgp") = "ORDER BY sgp DESC"
    # players = query.fetch()
    players = list(sheet)
    return players

def get_fpprojp():
    logging.error("get_fpp QUERY")
    sheet = FPProjP.query().order(-FPProjP.sgp) # .query() = "SELECT *"; .order("-sgp") = "ORDER BY sgp DESC"
    # players = query.fetch()
    players = list(sheet)
    return players

# blog
def get_posts(limit=None, offset=0, user=""):
    logging.error("get_posts limit=%s, offset=%d, user=%s QUERY" % (limit, offset, user))
    if user:
        query = Blog.query().filter(Blog.author == user).order(-Blog.created) # .query() = "SELECT *"; .filter("author", user) = "author = user"; .order("-created") = "ORDER BY created DESC"
    else:
        query = Blog.query().order(-Blog.created) # .query() = "SELECT *"; .order("-created") = "ORDER BY created DESC"
    posts = query.fetch(limit=limit, offset=offset) # .fetch(limit=limt, offset=offset) = "LIMIT limit OFFSET offset"
    posts = list(posts)
    return posts
    # return ndb.GqlQuery("SELECT * FROM Blog ORDER BY created DESC") #table is named Blog because class is named Blog (the class creates the table)
