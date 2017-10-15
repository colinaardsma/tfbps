"""Models Module"""
import sys
sys.path.insert(0, '//Users/colinaardsma/google_appengine')
from google.appengine.ext import db
#define columns of database objects

class Users(db.Model):
    """The user model"""
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    authorization = db.StringProperty(required=False)

class Batter(db.Model):
    """The Batter Model"""
    # Descriptive Properties
    name = db.StringProperty(required=True)
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

class Pitcher(db.Model):
    """The Pitcher Model"""
    # Descriptive Properties
    name = db.StringProperty(required=True)
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

#define columns of database objects
class FPProjB(db.Model):
    """The batter model"""

    name = db.StringProperty(required=True)
    team = db.StringProperty(required=True)
    pos = db.StringProperty(required=True)
#how to do multiple positions?
    ab = db.IntegerProperty(required=True)
    r = db.IntegerProperty(required=True)
    hr = db.IntegerProperty(required=True)
    rbi = db.IntegerProperty(required=True)
    sb = db.IntegerProperty(required=True)
    avg = db.FloatProperty(required=True)
    obp = db.FloatProperty(required=True)
    h = db.IntegerProperty(required=True)
    double = db.IntegerProperty(required=True)
    triple = db.IntegerProperty(required=True)
    bb = db.IntegerProperty(required=True)
    k = db.IntegerProperty(required=True)
    slg = db.FloatProperty(required=True)
    ops = db.FloatProperty(required=True)
    sgp = db.FloatProperty(required=False) #change to true later
    zr = db.FloatProperty(required=False)
    zhr = db.FloatProperty(required=False)
    zrbi = db.FloatProperty(required=False)
    zsb = db.FloatProperty(required=False)
    zops = db.FloatProperty(required=False)
    last_modified = db.DateTimeProperty(auto_now = True)
    category = db.StringProperty(required=True)

#define columns of database objects
class FPProjP(db.Model):
    """# This is the Pitcher Model"""

    name = db.StringProperty(required=True)
    team = db.StringProperty(required=True)
    pos = db.StringProperty(required=True)
#how to do multiple positions?
    ip = db.FloatProperty(required=True)
    k = db.IntegerProperty(required=True)
    w = db.IntegerProperty(required=True)
    sv = db.IntegerProperty(required=True)
    era = db.FloatProperty(required=True)
    whip = db.FloatProperty(required=True)
    er = db.IntegerProperty(required=True)
    h = db.IntegerProperty(required=True)
    bb = db.IntegerProperty(required=True)
    hr = db.IntegerProperty(required=True)
    g = db.IntegerProperty(required=True)
    gs = db.IntegerProperty(required=True)
    l = db.IntegerProperty(required=True)
    cg = db.IntegerProperty(required=True)
    sgp = db.FloatProperty(required=False) #change to true later
    z_score = db.FloatProperty(required=False) #change to true later
    last_modified = db.DateTimeProperty(auto_now=True)
    category = db.StringProperty(required=True)

#define columns of database objects
class Blog(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    author = db.ReferenceProperty(Users, required=True)
    coords = db.GeoPtProperty(required=False) #store coordinates of user based on URL, not required as it may not always be available
