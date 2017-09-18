import gqlqueries
import queries
import re
from dbmodels import Users, FPProjB, FPProjP #import classes from python file named dbmodels
from google.appengine.api import memcache

# stat retrieval methods
def get_cached_batter(update=False):
    key = "batter" # create key
    sheet = memcache.get(key) # search memcache for data at key, set data to sheet
    if sheet is None or update: # if nothing in memcache (or if update is called) run gql query and set memcache
        sheet = gqlqueries.get_fpprojb()
        memcache.set(key, sheet)
    return sheet

def get_cached_pitcher(update=False):
    key = "pitcher" # create key
    sheet = memcache.get(key) # search memcache for data at key, set data to sheet
    if sheet is None or update: # if nothing in memcache (or if update is called) run gql query and set memcache
        sheet = gqlqueries.get_fpprojp()
        memcache.set(key, sheet)
    return sheet





# stat retrieval methods
def cached_get_fpprojb(update=False):
    key = "fpprojb" # create key
    sheet = memcache.get(key) # search memcache for data at key, set data to sheet
    if sheet is None or update: # if nothing in memcache (or if update is called) run gql query and set memcache
        sheet = gqlqueries.get_fpprojb()
        memcache.set(key, sheet)
    return sheet

def cached_get_fpprojp(update=False):
    key = "fpprojp" # create key
    sheet = memcache.get(key) # search memcache for data at key, set data to sheet
    if sheet is None or update: # if nothing in memcache (or if update is called) run gql query and set memcache
        sheet = gqlqueries.get_fpprojp()
        memcache.set(key, sheet)
    return sheet

# user methods
def cached_user_by_name(username, update=False): # get user object
    key = str(username) + "getUbyN"
    user = memcache.get(key)
    if user is None or update:
        user = queries.get_user_by_name(username)
        memcache.set(key, user)
    return user

def cached_get_user_by_id(user_id, update=False): # get user object
    key = str(user_id) + "getUbyUID"
    user = memcache.get(key)
    if user is None or update:
        user = queries.get_user_by_id(user_id)
        memcache.set(key, user)
    return user

def cached_check_username(username, update=False): #check username
    key = str(username) + "checkUsername"
    name = memcache.get(key)
    if name is None or update:
        name = queries.check_username(username)
        memcache.set(key, name)
    return name

def cached_get_users(update=False):
    key = "users"
    users = memcache.get(key)
    if users is None or update:
        users = gqlqueries.get_users()
        memcache.set(key, users)
    return users

def cached_get_authorization(username, update=False):
    key = str(username) + "authorization"
    auth = memcache.get(key)
    if auth is None or update:
        auth = queries.get_authorization(username)
        memcache.set(key, auth)
    return auth

# post methods
def cached_posts(limit=None, offset=0, user="", author ="", update=False):
    key = "%s,%d,%s" % (limit, offset, author)
    blogs = memcache.get(key)
    if blogs is None or update:
        blogs = gqlqueries.get_posts(limit, offset, user)
        memcache.set(key, blogs)
    return blogs

#memcache flushing
def flush(key=None):
    #below deletes user memcache, is this necessary?
    # if key and key == "users":
    #     userkey = re.compile(r"^[a-zA-Z0-9_-]+getUser$")
    #     matching_keys = filter(userkey.match, memcache)
    #     for mk in matching_keys:
    #         memcache.delete(mk)
    if key:
        memcache.delete(key)
        return
    memcache.flush_all()
    return
