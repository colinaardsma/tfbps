"""Player models"""
# next 3 lines are for running locally
import sys
sys.path.append('/usr/local/google_appengine/')
sys.path.append('/usr/local/google_appengine/lib/yaml/lib/')
from google.appengine.ext import db
import normalizer
# sys.path.insert(0, '//Users/colinaardsma/google_appengine')
#define columns of database objects

class BatterHTML(object):
    """The Batter HTML Model"""
    # Descriptive Properties
    name = ""
    normalized_first_name = ""
    last_name = ""
    team = ""
    pos = ""
    # last_modified =
    category = ""
    # Raw Stat Properties
    atbats = 0.0
    runs = 0.0
    hrs = 0.0
    rbis = 0.0
    sbs = 0.0
    avg = 0.000
    ops = 0.000
    # Initial zScore Properties
    zScoreR = 0.000
    zScoreHr = 0.000
    zScoreRbi = 0.000
    zScoreSb = 0.000
    zScoreAvg = 0.000
    zScoreOps = 0.000
    # Weighted (Multiplied by AB) Properties
    weightedR = 0.000
    weightedHr = 0.000
    weightedRbi = 0.000
    weightedSb = 0.000
    weightedAvg = 0.000
    weightedOps = 0.000
    # Weighted and RezScored Properties
    weightedZscoreR = 0.000
    weightedZscoreHr = 0.000
    weightedZscoreRbi = 0.000
    weightedZscoreSb = 0.000
    weightedZscoreAvg = 0.000
    weightedZscoreOps = 0.000
    # Values
    fvaaz = 0.00
    dollarValue = 0.00
    keeper = 0.00
    # FA Status
    isFA = False

    def __init__(self, name, team, pos, category, atbats=0.0, runs=0.0, hrs=0.0, rbis=0.0,
                 sbs=0.0, avg=0.000, ops=0.000):
        # Descriptive Properties
        self.name = str(name)
        norm_name = normalizer.name_normalizer(name)
        self.normalized_first_name = str(norm_name['First'])
        self.last_name = str(norm_name['Last'])
        self.team = str(normalizer.team_normalizer(str(team)))
        self.pos = str(pos).split(",")
        # self.last_modified = last_modified
        self.category = str(category)
        # Raw Stat Properties
        self.atbats = float(atbats if atbats != None else 0.0)
        self.runs = float(runs if runs != None else 0.0)
        self.hrs = float(hrs if hrs != None else 0.0)
        self.rbis = float(rbis if rbis != None else 0.0)
        self.sbs = float(sbs if sbs != None else 0.0)
        self.avg = float(avg if avg != None else 0.0)
        self.ops = float(ops if ops != None else 0.0)

class PitcherHTML(object):
    """The Pitcher HTML Model"""
    # Descriptive Properties
    name = ""
    normalized_first_name = ""
    last_name = ""
    team = ""
    pos = ""
    is_sp = False
    # last_modified =
    category = ""
    # Raw Stat Properties
    ips = 0.0
    wins = 0.0
    svs = 0.0
    sos = 0.0
    era = 0.0
    whip = 0.000
    kip = 0.000
    # Initial zScore Properties
    zScoreW = 0.000
    zScoreSv = 0.000
    zScoreK = 0.000
    zScoreEra = 0.000
    zScoreWhip = 0.000
    # Weighted (Multiplied by AB) Properties
    weightedW = 0.000
    weightedSv = 0.000
    weightedK = 0.000
    weightedEra = 0.000
    weightedWhip = 0.000
    # Weighted and RezScored Properties
    weightedZscoreW = 0.000
    weightedZscoreSv = 0.000
    weightedZscoreK = 0.000
    weightedZscoreEra = 0.000
    weightedZscoreWhip = 0.000
    # Values
    fvaaz = 0.00
    dollarValue = 0.00
    keeper = 0.00
    # FA Status
    isFA = False

    def __init__(self, name, team, pos, category, ips=0.0, wins=0.0, svs=0.0, sos=0.0,
                 era=0.00, whip=0.00):
        # Descriptive Properties
        self.name = str(name)
        norm_name = normalizer.name_normalizer(name)
        self.normalized_first_name = str(norm_name['First'])
        self.last_name = str(norm_name['Last'])
        self.team = str(normalizer.team_normalizer(team))
        self.pos = str(pos).split(",")
        # self.last_modified = last_modified
        self.category = str(category)
        # Raw Stat Properties
        self.ips = float(ips if ips != None else 0.0)
        self.wins = float(wins if wins != None else 0.0)
        self.svs = float(svs if svs != None else 0.0)
        self.sos = float(sos if sos != None else 0.0)
        self.era = float(era if era != None else 0.0)
        self.whip = float(whip if whip != None else 0.0)
        self.kip = float(sos) / float(ips) if sos != None and ips != None else 0.0
        # SP Status
        self.is_sp = (False if 'SP' not in str(pos) or int(svs) > 0 or
                      float(wins) / float(ips) < 0.05 else True)

class BatterDB(db.Model):
    """The Batter Database Model"""
    # Descriptive Properties
    name = db.StringProperty(required=True)
    normalized_first_name = db.StringProperty()
    last_name = db.StringProperty()
    team = db.StringProperty(required=True)
    pos = db.StringListProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    category = db.StringProperty(required=True)
    # Raw Stat Properties
    atbats = db.FloatProperty(required=True)
    runs = db.FloatProperty(required=True)
    hrs = db.FloatProperty(required=True)
    rbis = db.FloatProperty(required=True)
    sbs = db.FloatProperty(required=True)
    avg = db.FloatProperty(required=True)
    ops = db.FloatProperty(required=True)
    # Initial zScore Properties
    zScoreR = db.FloatProperty()
    zScoreHr = db.FloatProperty()
    zScoreRbi = db.FloatProperty()
    zScoreSb = db.FloatProperty()
    zScoreAvg = db.FloatProperty()
    zScoreOps = db.FloatProperty()
    # Weighted (Multiplied by AB) Properties
    weightedR = db.FloatProperty()
    weightedHr = db.FloatProperty()
    weightedRbi = db.FloatProperty()
    weightedSb = db.FloatProperty()
    weightedAvg = db.FloatProperty()
    weightedOps = db.FloatProperty()
    # Weighted and RezScored Properties
    weightedZscoreR = db.FloatProperty()
    weightedZscoreHr = db.FloatProperty()
    weightedZscoreRbi = db.FloatProperty()
    weightedZscoreSb = db.FloatProperty()
    weightedZscoreAvg = db.FloatProperty()
    weightedZscoreOps = db.FloatProperty()
    # Values
    fvaaz = db.FloatProperty()
    dollarValue = db.FloatProperty()
    keeper = db.FloatProperty()
    # FA Status
    isFA = db.BooleanProperty()

class PitcherDB(db.Model):
    """The Pitcher Database Model"""
    # Descriptive Properties
    name = db.StringProperty(required=True)
    normalized_first_name = db.StringProperty()
    last_name = db.StringProperty()
    team = db.StringProperty(required=True)
    pos = db.StringListProperty(required=True)
    is_sp = db.BooleanProperty()
    last_modified = db.DateTimeProperty(auto_now=True)
    category = db.StringProperty(required=True)
    # Raw Stat Properties
    ips = db.FloatProperty(required=True)
    wins = db.FloatProperty(required=True)
    svs = db.FloatProperty(required=True)
    sos = db.FloatProperty(required=True)
    era = db.FloatProperty(required=True)
    whip = db.FloatProperty(required=True)
    kip = db.FloatProperty()
    # Initial zScore Properties
    zScoreW = db.FloatProperty()
    zScoreSv = db.FloatProperty()
    zScoreK = db.FloatProperty()
    zScoreEra = db.FloatProperty()
    zScoreWhip = db.FloatProperty()
    # Weighted (Multiplied by IP) Properties
    weightedW = db.FloatProperty()
    weightedSv = db.FloatProperty()
    weightedK = db.FloatProperty()
    weightedEra = db.FloatProperty()
    weightedWhip = db.FloatProperty()
    # Weighted and RezScored Properties
    weightedZscoreW = db.FloatProperty()
    weightedZscoreSv = db.FloatProperty()
    weightedZscoreK = db.FloatProperty()
    weightedZscoreEra = db.FloatProperty()
    weightedZscoreWhip = db.FloatProperty()
    # Values
    fvaaz = db.FloatProperty()
    dollarValue = db.FloatProperty()
    keeper = db.FloatProperty()
    # FA Status
    isFA = db.BooleanProperty()

def store_batter(batter):
    batter = BatterDB(name=batter.name, normalized_first_name=batter.normalized_first_name,
                      last_name=batter.last_name, team=batter.team, pos=batter.pos,
                      category=batter.category, atbats=batter.atbats, runs=batter.runs,
                      hrs=batter.hrs, rbis=batter.rbis, sbs=batter.sbs, avg=batter.avg,
                      ops=batter.ops, zScoreR=batter.zScoreR, zScoreHr=batter.zScoreHr,
                      zScoreRbi=batter.zScoreRbi, zScoreSb=batter.zScoreSb,
                      zScoreAvg=batter.zScoreAvg, zScoreOps=batter.zScoreOps,
                      weightedR=batter.weightedR, weightedHr=batter.weightedHr,
                      weightedRbi=batter.weightedRbi, weightedSb=batter.weightedSb,
                      weightedAvg=batter.weightedAvg, weightedOps=batter.weightedOps,
                      weightedZscoreR=batter.weightedZscoreR,
                      weightedZscoreHr=batter.weightedZscoreHr,
                      weightedZscoreRbi=batter.weightedZscoreRbi,
                      weightedZscoreSb=batter.weightedZscoreSb,
                      weightedZscoreAvg=batter.weightedZscoreAvg,
                      weightedZscoreOps=batter.weightedZscoreOps, fvaaz=batter.fvaaz,
                      dollarValue=batter.dollarValue, keeper=batter.keeper, isFA=batter.isFA)
    return batter
    # db.put_async(batter)

def store_pitcher(pitcher):
    pitcher = PitcherDB(name=pitcher.name, normalized_first_name=pitcher.normalized_first_name,
                        last_name=pitcher.last_name, team=pitcher.team, pos=pitcher.pos,
                        is_sp=pitcher.is_sp, category=pitcher.category, ips=pitcher.ips,
                        wins=pitcher.wins, svs=pitcher.svs, sos=pitcher.sos, era=pitcher.era,
                        whip=pitcher.whip, kip=pitcher.kip, zScoreW=pitcher.zScoreW,
                        zScoreSv=pitcher.zScoreSv, zScoreK=pitcher.zScoreK,
                        zScoreEra=pitcher.zScoreEra, zScoreWhip=pitcher.zScoreWhip,
                        weightedW=pitcher.weightedW, weightedSv=pitcher.weightedSv,
                        weightedK=pitcher.weightedK, weightedEra=pitcher.weightedEra,
                        weightedWhip=pitcher.weightedWhip, weightedZscoreW=pitcher.weightedZscoreW,
                        weightedZscoreSv=pitcher.weightedZscoreSv,
                        weightedZscoreK=pitcher.weightedZscoreK,
                        weightedZscoreEra=pitcher.weightedZscoreEra,
                        weightedZscoreWhip=pitcher.weightedZscoreWhip,
                        fvaaz=pitcher.fvaaz, dollarValue=pitcher.dollarValue, keeper=pitcher.keeper,
                        isFA=pitcher.isFA)
    return pitcher
    # db.put_async(pitcher)
