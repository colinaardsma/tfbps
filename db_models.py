"""Models Module"""
import sys
from google.appengine.ext import db
# sys.path.insert(0, '//Users/colinaardsma/google_appengine')
#define columns of database objects
import caching
import time
import queries
# import hashing

class BatterDB(db.Model):
    """The Batter Database Model"""
    # Descriptive Properties
    name = db.StringProperty(required=True)
    normalized_first_name = db.StringProperty
    last_name = db.StringProperty
    team = db.StringProperty(required=True)
    pos = db.StringProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    category = db.StringProperty(required=True)
    # Raw Stat Properties
    atbats = db.IntegerProperty(required=True)
    runs = db.IntegerProperty(required=True)
    hrs = db.IntegerProperty(required=True)
    rbis = db.IntegerProperty(required=True)
    sbs = db.IntegerProperty(required=True)
    avg = db.FloatProperty(required=True)
    ops = db.FloatProperty(required=True)
    # Initial zScore Properties
    zScoreR = db.FloatProperty
    zScoreHr = db.FloatProperty
    zScoreRbi = db.FloatProperty
    zScoreSb = db.FloatProperty
    zScoreAvg = db.FloatProperty
    zScoreOps = db.FloatProperty
    # Weighted (Multiplied by AB) Properties
    weightedR = db.FloatProperty
    weightedHr = db.FloatProperty
    weightedRbi = db.FloatProperty
    weightedSb = db.FloatProperty
    weightedAvg = db.FloatProperty
    weightedOps = db.FloatProperty
    # Weighted and RezScored Properties
    weightedZscoreR = db.FloatProperty
    weightedZscoreHr = db.FloatProperty
    weightedZscoreRbi = db.FloatProperty
    weightedZscoreSb = db.FloatProperty
    weightedZscoreAvg = db.FloatProperty
    weightedZscoreOps = db.FloatProperty
    # Values
    fvaaz = db.FloatProperty
    dollarValue = db.FloatProperty
    keeper = db.FloatProperty
    # FA Status
    isFA = db.BooleanProperty

class PitcherDB(db.Model):
    """The Pitcher Database Model"""
    # Descriptive Properties
    name = db.StringProperty(required=True)
    normalized_first_name = db.StringProperty
    last_name = db.StringProperty
    team = db.StringProperty(required=True)
    pos = db.StringProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    category = db.StringProperty(required=True)
    # Raw Stat Properties
    ips = db.IntegerProperty(required=True)
    wins = db.IntegerProperty(required=True)
    saves = db.IntegerProperty(required=True)
    strikeOuts = db.IntegerProperty(required=True)
    era = db.FloatProperty(required=True)
    whip = db.FloatProperty(required=True)
    # Initial zScore Properties
    zScoreW = db.FloatProperty
    zScoreSv = db.FloatProperty
    zScoreK = db.FloatProperty
    zScoreEra = db.FloatProperty
    zScoreWhip = db.FloatProperty
    # Weighted (Multiplied by IP) Properties
    weightedW = db.FloatProperty
    weightedSv = db.FloatProperty
    weightedK = db.FloatProperty
    weightedEra = db.FloatProperty
    weightedWhip = db.FloatProperty
    # Weighted and RezScored Properties
    weightedZscoreW = db.FloatProperty
    weightedZscoreSv = db.FloatProperty
    weightedZscoreK = db.FloatProperty
    weightedZscoreEra = db.FloatProperty
    weightedZscoreWhip = db.FloatProperty
    # Values
    fvaaz = db.FloatProperty
    dollarValue = db.FloatProperty
    keeper = db.FloatProperty
    # FA Status
    isFA = db.BooleanProperty

# TODO: delete this?
# def pull_batters(player):
#     player = BatterDB(name=name, team=team, pos=pos, ab=ab, r=r, hr=hr, rbi=rbi, sb=sb, avg=avg, obp=obp, h=h, double=double, triple=triple, bb=bb, k=k, slg=slg, ops=ops, category=category)
#     player.put()

class User(db.Model):
    """The User database model"""
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    authorization = db.StringProperty(required=True)
    yahooGuid = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty()
    last_accessed = db.DateTimeProperty(auto_now=True)
    location = db.GeoPtProperty()
    access_token = db.StringProperty()
    token_expiration = db.DateTimeProperty()
    refresh_token = db.StringProperty()

def store_user(username, user_id, password, email, location = None, yahooGuid = None, authorization = "basic"):
    user = User(username=username, password=password, email=email, location=location,
                yahooGuid=yahooGuid, authorization=authorization, access_token=None,
                token_expiration=None, refresh_token=None)
    db.put(user)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache
    update_user_memcache(user, user_id)

def update_user(user, user_id, username=None, hashed_password=None, email=None,
                authorization=None, yahooGuid=None, last_accessed=None,
                location=None, access_token=None, token_expiration=None,
                refresh_token=None):
    user = queries.get_user_by_name(user.username)
    if username:
        user.username = username
    if hashed_password:
        # password = hashing.make_pw_hash(username, password) # hash password for storage in db
        user.password = hashed_password
    if email:
        user.email = email
    if authorization:
        user.authorization = authorization
    if yahooGuid:
        user.yahooGuid = yahooGuid
    if last_accessed:
        user.last_accessed = last_accessed
    if location:
        user.location = location
    if access_token:
        user.access_token = access_token
    if token_expiration:
        user.token_expiration = token_expiration
    if refresh_token:
        user.refresh_token = refresh_token
    db.put(user)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache
    update_user_memcache(user, user_id)

def update_user_memcache(user, user_id):
    caching.cached_user_by_name(user.username, True)
    caching.cached_check_username(user.username, True)
    caching.cached_get_user_by_id(user_id, True)
    caching.cached_get_users(True)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache
