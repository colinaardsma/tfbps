import gqlqueries
from dbmodels import Users, fantProProjB, fantProProjP #import classes from python file named dbmodels
from google.appengine.api import memcache

# def cached_posts(limit=None, offset=0, user="", update=False):
#     key = str(limit) + str(offset) + str(user)
#     blogs = memcache.get(key)
#     if blogs is None or update:
#         blogs = gqlqueries.get_posts(limit, offset, user)
#         memcache.set(key, blogs)
#     return blogs

def cached_get_fpb(update=False):
    key = "fullfpb"
    sheet = memcache.get(key)
    if sheet is None or update:
        sheet = gqlqueries.get_fpb()
        memcache.set(key, sheet)
    return sheet

def cached_get_fpp(update=False):
    key = "fullfpp"
    sheet = memcache.get(key)
    if sheet is None or update:
        sheet = gqlqueries.get_fpp()
        memcache.set(key, sheet)
    return sheet

def cached_user_by_name(usr, update=False):
    key = str(usr) + "getUser"
    user = memcache.get(key)
    if user is None or update:
        user = gqlqueries.get_user_by_name(usr)
        memcache.set(key, user)
    return user

def cached_check_username(username, update=False):
    key = str(username) + "checkUsername"
    name = memcache.get(key)
    if name is None or update:
        name = gqlqueries.check_username(username)
        memcache.set(key, name)
    return name
