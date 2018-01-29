"""Models Module"""
import sys
sys.path.insert(0, '//Users/colinaardsma/google_appengine')
from google.appengine.ext import ndb
#define columns of database objects

class Users(ndb.Model):
    """The user model"""
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    authorization = ndb.StringProperty(required=False)

class Batter(ndb.Model):
    """The Batter Model"""
    # Descriptive Properties
    name = ndb.StringProperty(required=True)
    team = ndb.StringProperty(required=True)
    pos = ndb.StringProperty(required=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    category = ndb.StringProperty(required=True)
    # Raw Stat Properties
    atbats = ndb.IntegerProperty(required=True)
    runs = ndb.IntegerProperty(required=True)
    hrs = ndb.IntegerProperty(required=True)
    rbis = ndb.IntegerProperty(required=True)
    sbs = ndb.IntegerProperty(required=True)
    avg = ndb.FloatProperty(required=True)
    ops = ndb.FloatProperty(required=True)
    # Initial zScore Properties
    zScoreR = ndb.FloatProperty()
    zScoreHr = ndb.FloatProperty()
    zScoreRbi = ndb.FloatProperty()
    zScoreSb = ndb.FloatProperty()
    zScoreAvg = ndb.FloatProperty()
    zScoreOps = ndb.FloatProperty()
    # Weighted (Multiplied by AB) Properties
    weightedR = ndb.FloatProperty()
    weightedHr = ndb.FloatProperty()
    weightedRbi = ndb.FloatProperty()
    weightedSb = ndb.FloatProperty()
    weightedAvg = ndb.FloatProperty()
    weightedOps = ndb.FloatProperty()
    # Weighted and RezScored Properties
    weightedZscoreR = ndb.FloatProperty()
    weightedZscoreHr = ndb.FloatProperty()
    weightedZscoreRbi = ndb.FloatProperty()
    weightedZscoreSb = ndb.FloatProperty()
    weightedZscoreAvg = ndb.FloatProperty()
    weightedZscoreOps = ndb.FloatProperty()

class Pitcher(ndb.Model):
    """The Pitcher Model"""
    # Descriptive Properties
    name = ndb.StringProperty(required=True)
    team = ndb.StringProperty(required=True)
    pos = ndb.StringProperty(required=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    category = ndb.StringProperty(required=True)
    # Raw Stat Properties
    ips = ndb.IntegerProperty(required=True)
    wins = ndb.IntegerProperty(required=True)
    saves = ndb.IntegerProperty(required=True)
    strikeOuts = ndb.IntegerProperty(required=True)
    era = ndb.FloatProperty(required=True)
    whip = ndb.FloatProperty(required=True)
    # Initial zScore Properties
    zScoreW = ndb.FloatProperty()
    zScoreSv = ndb.FloatProperty()
    zScoreK = ndb.FloatProperty()
    zScoreEra = ndb.FloatProperty()
    zScoreWhip = ndb.FloatProperty()
    # Weighted (Multiplied by IP) Properties
    weightedW = ndb.FloatProperty()
    weightedSv = ndb.FloatProperty()
    weightedK = ndb.FloatProperty()
    weightedEra = ndb.FloatProperty()
    weightedWhip = ndb.FloatProperty()
    # Weighted and RezScored Properties
    weightedZscoreW = ndb.FloatProperty()
    weightedZscoreSv = ndb.FloatProperty()
    weightedZscoreK = ndb.FloatProperty()
    weightedZscoreEra = ndb.FloatProperty()
    weightedZscoreWhip = ndb.FloatProperty()

#define columns of database objects
class FPProjB(ndb.Model):
    """The batter model"""
    name = ndb.StringProperty(required=True)
    team = ndb.StringProperty(required=True)
    pos = ndb.StringProperty(required=True)
#how to do multiple positions?
    ab = ndb.IntegerProperty(required=True)
    r = ndb.IntegerProperty(required=True)
    hr = ndb.IntegerProperty(required=True)
    rbi = ndb.IntegerProperty(required=True)
    sb = ndb.IntegerProperty(required=True)
    avg = ndb.FloatProperty(required=True)
    obp = ndb.FloatProperty(required=True)
    h = ndb.IntegerProperty(required=True)
    double = ndb.IntegerProperty(required=True)
    triple = ndb.IntegerProperty(required=True)
    bb = ndb.IntegerProperty(required=True)
    k = ndb.IntegerProperty(required=True)
    slg = ndb.FloatProperty(required=True)
    ops = ndb.FloatProperty(required=True)
    sgp = ndb.FloatProperty(required=False) #change to true later
    zr = ndb.FloatProperty(required=False)
    zhr = ndb.FloatProperty(required=False)
    zrbi = ndb.FloatProperty(required=False)
    zsb = ndb.FloatProperty(required=False)
    zops = ndb.FloatProperty(required=False)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    category = ndb.StringProperty(required=True)

#define columns of database objects
class FPProjP(ndb.Model):
    """# This is the Pitcher Model"""
    name = ndb.StringProperty(required=True)
    team = ndb.StringProperty(required=True)
    pos = ndb.StringProperty(required=True)
    #how to do multiple positions?
    ip = ndb.FloatProperty(required=True)
    k = ndb.IntegerProperty(required=True)
    w = ndb.IntegerProperty(required=True)
    sv = ndb.IntegerProperty(required=True)
    era = ndb.FloatProperty(required=True)
    whip = ndb.FloatProperty(required=True)
    er = ndb.IntegerProperty(required=True)
    h = ndb.IntegerProperty(required=True)
    bb = ndb.IntegerProperty(required=True)
    hr = ndb.IntegerProperty(required=True)
    g = ndb.IntegerProperty(required=True)
    gs = ndb.IntegerProperty(required=True)
    l = ndb.IntegerProperty(required=True)
    cg = ndb.IntegerProperty(required=True)
    sgp = ndb.FloatProperty(required=False) #change to true later
    z_score = ndb.FloatProperty(required=False) #change to true later
    last_modified = ndb.DateTimeProperty(auto_now=True)
    category = ndb.StringProperty(required=True)

#define columns of database objects
class Blog(ndb.Model):
    title = ndb.StringProperty(required=True)
    body = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    author = ndb.KeyProperty(kind=Users, required=True)
    coords = ndb.GeoPtProperty(required=False) #store coordinates of user based on URL, not required as it may not always be available
