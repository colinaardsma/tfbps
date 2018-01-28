import gqlqueries
import queries
import re
from dbmodels import Users, FPProjB, FPProjP #import classes from python file named dbmodels
from google.appengine.api import memcache

# stat retrieval methods
def cached_get_all_batters(update=False):
    key = "allBatters"
    batters = memcache.get(key)
    if batters is None or update:
        batters = queries.get_batters()
        memcache.set(key, batters)
    return batters

def cached_get_all_pitchers(update=False):
    key = "allPitchers"
    pitchers = memcache.get(key)
    if pitchers is None or update:
        pitchers = queries.get_pitchers()
        memcache.set(key, pitchers)
    return pitchers

# user methods
def cached_user_by_name(username, update=False): # get user object
    key = str(username).lower() + "_getUbyN"
    user = memcache.get(key)
    if user is None or update:
        user = queries.get_user_by_name(username)
        memcache.set(key, user)
    return user

def cached_get_user_by_id(user_id, update=False): # get user object
    key = str(user_id) + "_getUbyUID"
    user = memcache.get(key)
    if user is None or update:
        user = queries.get_user_by_id(user_id)
        memcache.set(key, user)
    return user

def cached_check_username(username, update=False): #check username
    key = str(username).lower() + "_checkUsername"
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
    key = str(username).lower() + "_authorization"
    auth = memcache.get(key)
    if auth is None or update:
        auth = queries.get_authorization(username)
        memcache.set(key, auth)
    return auth

#league methods
def cached_get_leagues_by_league_key(league_key, update=False):
    key = str(league_key) + "_leagueByLeagueKey"
    league = memcache.get(key)
    if league is None or update:
        league = queries.get_leagues_by_league_key(str(league_key))
        memcache.set(key, league)
    return league

def cached_get_all_leagues(update=False):
    key = "allLeagues"
    leagues = memcache.get(key)
    if leagues is None or update:
        leagues = queries.get_all_leagues()
        memcache.set(key, leagues)
    return leagues

#user_league methods
def cached_get_all_user_leagues_by_user(user, update=False):
    key = user.yahooGuid + "_userLeague"
    user_league = memcache.get(key)
    if user_league is None or update:
        user_league = queries.get_all_user_leagues_by_user(user)
        memcache.set(key, user_league)
    return user_league

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
