from dbmodels import Users, fantProProjB, fantProProjP #import Users and Blog classes from python file named dbmodels
from google.appengine.ext import db
import logging


# def get_posts(limit=None, offset=0, user=""):
#     logging.error("get_posts QUERY")
#     if user:
#         query = Blog.all().filter("author", user).order("-created") # .all() = "SELECT *"; .filter("author", user) = "author = user"; .order("-created") = "ORDER BY created DESC"
#     else:
#         query = Blog.all().order("-created") # .all() = "SELECT *"; .order("-created") = "ORDER BY created DESC"
#     posts = query.fetch(limit=limit, offset=offset) # .fetch(limit=limt, offset=offset) = "LIMIT limit OFFSET offset"
#     posts = list(posts)
#     return posts
#     # return db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC") #table is named Blog because class is named Blog (the class creates the table)
#
# def get_user_by_name(usr):
#     logging.error("get_user_by_name QUERY")
#     """ Get a user object from the db, based on their username """
#     # user = db.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % usr) #using %s in SQL queries is BAD, never do this
#     user = Users.all().filter("username", usr) # .all() = "SELECT *"; .filter("username", usr) = "username = usr"
#     if user:
#         return user.get()
#
# def check_username(username):
#     # n = db.GqlQuery("SELECT * FROM Users ORDER BY username") #pull db of userinfo and order by username
#     n = Users.all().order("username") # .all() = "SELECT *"; .order("username") = "ORDER BY username"
#     for name in n:
#         if name.username == username:
#             return name.key().id()

def get_fpb():
    logging.error("get_fpb QUERY")
    query = fantProProjB.all().order("-sgp") # .all() = "SELECT *"; .order("-sgp") = "ORDER BY sgp DESC"
    # players = query.fetch()
    players = list(query)
    return players

def get_fpp():
    logging.error("get_fpp QUERY")
    query = fantProProjP.all().order("-sgp") # .all() = "SELECT *"; .order("-sgp") = "ORDER BY sgp DESC"
    # players = query.fetch()
    players = list(query)
    return players
