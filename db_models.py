"""Models Module"""
import sys
from google.appengine.ext import db
# sys.path.insert(0, '//Users/colinaardsma/google_appengine')
#define columns of database objects

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
    yahooGuid = db.StringProperty
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty
    last_accessed = db.DateTimeProperty(auto_now=True)
    location = db.GeoPtProperty

 
