"""Player models"""
# next 3 lines are for running locally
import sys
import datetime
sys.path.append('/usr/local/google_appengine/')
sys.path.append('/usr/local/google_appengine/lib/yaml/lib/')
from google.appengine.ext import db
import pprint
import normalizer
import caching
import time
import player_creator
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
    status = ""
    last_modified = datetime.datetime.now()
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

    def __init__(self, name, team, pos, status, category, atbats=0.0, runs=0.0, hrs=0.0, rbis=0.0,
                 sbs=0.0, avg=0.000, ops=0.000):
        # Descriptive Properties
        self.name = str(name)
        norm_name = normalizer.name_normalizer(name)
        self.normalized_first_name = str(norm_name['First'])
        self.last_name = str(norm_name['Last'])
        self.team = str(normalizer.team_normalizer(str(team)))
        self.pos = str(pos).split(",")
        self.status = str(status)
        self.last_modified = datetime.datetime.now()
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
    status = ""
    last_modified = datetime.datetime.now()
    category = ""
    # Raw Stat Properties
    ips = 0.0
    wins = 0.0
    svs = 0.0
    sos = 0.0
    era = 0.0
    whip = 0.00
    kip = 0.00
    winsip = 0.000
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

    def __init__(self, name, team, pos, status, category, ips=0.0, wins=0.0, svs=0.0, sos=0.0,
                 era=0.00, whip=0.00):
        # Descriptive Properties
        self.name = str(name)
        norm_name = normalizer.name_normalizer(name)
        self.normalized_first_name = str(norm_name['First'])
        self.last_name = str(norm_name['Last'])
        self.team = str(normalizer.team_normalizer(team))
        self.pos = str(pos).split(",")
        self.status = str(status)
        self.last_modified = datetime.datetime.now()
        self.category = str(category)
        # Raw Stat Properties
        self.ips = float(ips if ips != None else 0.0)
        self.wins = float(wins if wins != None else 0.0)
        self.svs = float(svs if svs != None else 0.0)
        self.sos = float(sos if sos != None else 0.0)
        self.era = float(era if era != None else 0.0)
        self.whip = float(whip if whip != None else 0.0)
        self.kip = float(sos) / float(ips) if sos != None and ips != None else 0.0
        self.winsip = float(wins) / float(ips) if wins != None and ips != None else 0.0
        # SP Status
        self.is_sp = (False if 'SP' not in str(pos) or int(svs) > 0 or
                      float(wins) / float(ips) < 0.05 else True)

class BatterProj(db.Model):
    """The Batter Projection Database Model"""
    # Descriptive Properties
    name = db.StringProperty(required=True)
    normalized_first_name = db.StringProperty()
    last_name = db.StringProperty()
    team = db.StringProperty(required=True)
    pos = db.StringListProperty(required=True)
    status = db.StringProperty()
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

class BatterValue(db.Model):
    """The Batter Value Database Model"""
    # Descriptive Properties
    name = db.StringProperty(required=True)
    normalized_first_name = db.StringProperty()
    last_name = db.StringProperty()
    team = db.StringProperty(required=True)
    pos = db.StringListProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    category = db.StringProperty(required=True)
    league_key = db.StringProperty(required=True)
    yahooGuid = db.StringProperty(required=True)
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

def store_batter(batter):
    batter = BatterProj(name=batter.name, normalized_first_name=batter.normalized_first_name,
                        last_name=batter.last_name, team=batter.team, pos=batter.pos,
                        status=batter.status,
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

def store_batter_values(yahooGuid, league, batter_proj_list):
    batter_value_list = []
    for batter_proj in batter_proj_list:
        batter_values = player_creator.calc_batter_z_score(batter_proj_list,
                                                           league.batters_over_zero_dollars_avg,
                                                           league.one_dollar_batters_avg,
                                                           league.b_dollar_per_fvaaz_avg,
                                                           league.b_player_pool_mult_avg)
        batter_proj_value = [batter for batter in batter_values
                             if batter.name == batter_proj.name
                             and batter.team == batter_proj.team
                             and batter.pos == batter_proj.pos][0]

        batter_value = BatterValue(name=batter_proj.name,
                                   normalized_first_name=batter_proj.normalized_first_name,
                                   last_name=batter_proj.last_name, team=batter_proj.team,
                                   pos=batter_proj.pos, category=batter_proj.category,
                                   league_key=league.league_key, yahooGuid=yahooGuid,
                                   zScoreR=batter_proj_value.zScoreR,
                                   zScoreHr=batter_proj_value.zScoreHr,
                                   zScoreRbi=batter_proj_value.zScoreRbi,
                                   zScoreSb=batter_proj_value.zScoreSb,
                                   zScoreAvg=batter_proj_value.zScoreAvg,
                                   zScoreOps=batter_proj_value.zScoreOps,
                                   weightedR=batter_proj_value.weightedR,
                                   weightedHr=batter_proj_value.weightedHr,
                                   weightedRbi=batter_proj_value.weightedRbi,
                                   weightedSb=batter_proj_value.weightedSb,
                                   weightedAvg=batter_proj_value.weightedAvg,
                                   weightedOps=batter_proj_value.weightedOps,
                                   weightedZscoreR=batter_proj_value.weightedZscoreR,
                                   weightedZscoreHr=batter_proj_value.weightedZscoreHr,
                                   weightedZscoreRbi=batter_proj_value.weightedZscoreRbi,
                                   weightedZscoreSb=batter_proj_value.weightedZscoreSb,
                                   weightedZscoreAvg=batter_proj_value.weightedZscoreAvg,
                                   weightedZscoreOps=batter_proj_value.weightedZscoreOps,
                                   fvaaz=batter_proj_value.fvaaz,
                                   dollarValue=batter_proj_value.dollarValue,
                                   keeper=batter_proj_value.keeper)
        batter_value_list.append(batter_value)
    db.put(batter_value_list)
    return batter_value_list

class PitcherProj(db.Model):
    """The Pitcher Projection Database Model"""
    # Descriptive Properties
    name = db.StringProperty(required=True)
    normalized_first_name = db.StringProperty()
    last_name = db.StringProperty()
    team = db.StringProperty(required=True)
    pos = db.StringListProperty(required=True)
    is_sp = db.BooleanProperty()
    status = db.StringProperty()
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
    winsip = db.FloatProperty()
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

class PitcherValue(db.Model):
    """The Pitcher Value Database Model"""
    name = db.StringProperty(required=True)
    normalized_first_name = db.StringProperty()
    last_name = db.StringProperty()
    team = db.StringProperty(required=True)
    pos = db.StringListProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    category = db.StringProperty(required=True)
    league_key = db.StringProperty(required=True)
    yahooGuid = db.StringProperty(required=True)
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

def store_pitcher(pitcher):
    pitcher = PitcherProj(name=pitcher.name, normalized_first_name=pitcher.normalized_first_name,
                          last_name=pitcher.last_name, team=pitcher.team, pos=pitcher.pos,
                          is_sp=pitcher.is_sp, status=pitcher.status,
                          category=pitcher.category, ips=pitcher.ips,
                          wins=pitcher.wins, svs=pitcher.svs, sos=pitcher.sos, era=pitcher.era,
                          whip=pitcher.whip, kip=pitcher.kip, winsip=pitcher.winsip,
                          zScoreW=pitcher.zScoreW, zScoreSv=pitcher.zScoreSv,
                          zScoreK=pitcher.zScoreK, zScoreEra=pitcher.zScoreEra,
                          zScoreWhip=pitcher.zScoreWhip, weightedW=pitcher.weightedW,
                          weightedSv=pitcher.weightedSv, weightedK=pitcher.weightedK,
                          weightedEra=pitcher.weightedEra, weightedWhip=pitcher.weightedWhip,
                          weightedZscoreW=pitcher.weightedZscoreW,
                          weightedZscoreSv=pitcher.weightedZscoreSv,
                          weightedZscoreK=pitcher.weightedZscoreK,
                          weightedZscoreEra=pitcher.weightedZscoreEra,
                          weightedZscoreWhip=pitcher.weightedZscoreWhip,
                          fvaaz=pitcher.fvaaz, dollarValue=pitcher.dollarValue, keeper=pitcher.keeper,
                          isFA=pitcher.isFA)
    return pitcher
    # db.put_async(pitcher)

def store_pitcher_values(yahooGuid, league, pitcher_proj_list):
    pitcher_value_list = []
    for pitcher_proj in pitcher_proj_list:
        pitcher_values = player_creator.calc_pitcher_z_score(pitcher_proj_list,
                                                             league.pitchers_over_zero_dollars_avg,
                                                             league.one_dollar_pitchers_avg,
                                                             league.p_dollar_per_fvaaz_avg,
                                                             league.p_player_pool_mult_avg)
        pitcher_proj_value = [pitcher for pitcher in pitcher_values
                              if pitcher.name == pitcher_proj.name
                              and pitcher.team == pitcher_proj.team
                              and pitcher.pos == pitcher_proj.pos][0]

        pitcher_value = PitcherValue(name=pitcher_proj.name,
                                     normalized_first_name=pitcher_proj.normalized_first_name,
                                     last_name=pitcher_proj.last_name, team=pitcher_proj.team,
                                     pos=pitcher_proj.pos, category=pitcher_proj.category,
                                     league_key=league.league_key, yahooGuid=yahooGuid,
                                     zScoreW=pitcher_proj_value.zScoreW,
                                     zScoreSv=pitcher_proj_value.zScoreSv,
                                     zScoreK=pitcher_proj_value.zScoreK,
                                     zScoreEra=pitcher_proj_value.zScoreEra,
                                     zScoreWhip=pitcher_proj_value.zScoreWhip,
                                     weightedW=pitcher_proj_value.weightedW,
                                     weightedSv=pitcher_proj_value.weightedSv,
                                     weightedK=pitcher_proj_value.weightedK,
                                     weightedEra=pitcher_proj_value.weightedEra,
                                     weightedWhip=pitcher_proj_value.weightedWhip,
                                     weightedZscoreW=pitcher_proj_value.weightedZscoreW,
                                     weightedZscoreSv=pitcher_proj_value.weightedZscoreSv,
                                     weightedZscoreK=pitcher_proj_value.weightedZscoreK,
                                     weightedZscoreEra=pitcher_proj_value.weightedZscoreEra,
                                     weightedZscoreWhip=pitcher_proj_value.weightedZscoreWhip,
                                     fvaaz=pitcher_proj_value.fvaaz,
                                     dollarValue=pitcher_proj_value.dollarValue,
                                     keeper=pitcher_proj_value.keeper)
        pitcher_value_list.append(pitcher_value)
    db.put(pitcher_value_list)
    return pitcher_value_list

def update_batter_memcache():
    caching.cached_get_all_batters(True)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache

def update_pitcher_memcache():
    caching.cached_get_all_pitchers(True)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache

def put_batters(batter_list):
    db.put(batter_list)
    update_batter_memcache()

def put_pitchers(pitcher_list):
    db.put(pitcher_list)
    update_pitcher_memcache()
