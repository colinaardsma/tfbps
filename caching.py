import gqlqueries
from dbmodels import Users, fantProProjB, fantProProjP #import classes from python file named dbmodels
from google.appengine.api import memcache

#post methods
# def cached_posts(limit=None, offset=0, user="", update=False):
#     key = str(limit) + str(offset) + str(user)
#     blogs = memcache.get(key)
#     if blogs is None or update:
#         blogs = gqlqueries.get_posts(limit, offset, user)
#         memcache.set(key, blogs)
#     return blogs

#data retrieval methods
def cached_get_fpb(update=False):
    key = "fullfpb" #create key
    sheet = memcache.get(key) #search memcache for data at key, set data to sheet
    if sheet is None or update: #if nothing in memcache (or if update is called) run gql query and set memcache
        sheet = gqlqueries.get_fpb()
        memcache.set(key, sheet)
    return sheet

def cached_get_fpp(update=False):
    key = "fullfpp" #create key
    sheet = memcache.get(key) #search memcache for data at key, set data to sheet
    if sheet is None or update: #if nothing in memcache (or if update is called) run gql query and set memcache
        sheet = gqlqueries.get_fpp()
        memcache.set(key, sheet)
    return sheet

#user validation methods
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
