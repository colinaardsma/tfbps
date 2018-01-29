"""Player models"""
# next 3 lines are for running locally
import sys
import datetime
sys.path.append('/usr/local/google_appengine/')
sys.path.append('/usr/local/google_appengine/lib/yaml/lib/')
from google.appengine.ext import ndb
import pprint
import normalizer
import caching
import time
import player_creator
# sys.path.insert(0, '//Users/colinaardsma/google_appengine')
#define columns of database objects

RUN_ASYNC = True

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

class BatterProj(ndb.Model):
    """The Batter Projection Database Model"""
    # Descriptive Properties
    name = ndb.StringProperty(required=True)
    normalized_first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    team = ndb.StringProperty(required=True)
    pos = ndb.StringProperty(repeated=True)
    status = ndb.StringProperty()
    last_modified = ndb.DateTimeProperty(auto_now=True)
    category = ndb.StringProperty(required=True)
    # Raw Stat Properties
    atbats = ndb.FloatProperty(required=True)
    runs = ndb.FloatProperty(required=True)
    hrs = ndb.FloatProperty(required=True)
    rbis = ndb.FloatProperty(required=True)
    sbs = ndb.FloatProperty(required=True)
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
    # Values
    fvaaz = ndb.FloatProperty()
    dollarValue = ndb.FloatProperty()
    keeper = ndb.FloatProperty()
    # FA Status
    isFA = ndb.BooleanProperty()

class BatterValue(ndb.Model):
    """The Batter Value Database Model"""
    # Descriptive Properties
    name = ndb.StringProperty(required=True)
    normalized_first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    team = ndb.StringProperty(required=True)
    pos = ndb.StringProperty(repeated=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    category = ndb.StringProperty(required=True)
    league_key = ndb.StringProperty(required=True)
    yahooGuid = ndb.StringProperty(required=True)
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
    # Values
    fvaaz = ndb.FloatProperty()
    dollarValue = ndb.FloatProperty()
    keeper = ndb.FloatProperty()

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
    # ndb.put_async(batter)

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
    if RUN_ASYNC:
        ndb.put_multi_async(batter_value_list)
    else:
        ndb.put_multi(batter_value_list)
    return batter_value_list

class PitcherProj(ndb.Model):
    """The Pitcher Projection Database Model"""
    # Descriptive Properties
    name = ndb.StringProperty(required=True)
    normalized_first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    team = ndb.StringProperty(required=True)
    pos = ndb.StringProperty(repeated=True)
    is_sp = ndb.BooleanProperty()
    status = ndb.StringProperty()
    last_modified = ndb.DateTimeProperty(auto_now=True)
    category = ndb.StringProperty(required=True)
    # Raw Stat Properties
    ips = ndb.FloatProperty(required=True)
    wins = ndb.FloatProperty(required=True)
    svs = ndb.FloatProperty(required=True)
    sos = ndb.FloatProperty(required=True)
    era = ndb.FloatProperty(required=True)
    whip = ndb.FloatProperty(required=True)
    kip = ndb.FloatProperty()
    winsip = ndb.FloatProperty()
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
    # Values
    fvaaz = ndb.FloatProperty()
    dollarValue = ndb.FloatProperty()
    keeper = ndb.FloatProperty()
    # FA Status
    isFA = ndb.BooleanProperty()

class PitcherValue(ndb.Model):
    """The Pitcher Value Database Model"""
    name = ndb.StringProperty(required=True)
    normalized_first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    team = ndb.StringProperty(required=True)
    pos = ndb.StringProperty(repeated=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    category = ndb.StringProperty(required=True)
    league_key = ndb.StringProperty(required=True)
    yahooGuid = ndb.StringProperty(required=True)
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
    # Values
    fvaaz = ndb.FloatProperty()
    dollarValue = ndb.FloatProperty()
    keeper = ndb.FloatProperty()
    # FA Status
    isFA = ndb.BooleanProperty()

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
    # ndb.put_async(pitcher)

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
    if RUN_ASYNC:
        ndb.put_multi_async(pitcher_value_list)
    else:
        ndb.put_multi(pitcher_value_list)
    return pitcher_value_list

def update_batter_db(batter_list):
    if RUN_ASYNC:
        batters = ndb.put_multi_async(batter_list)
    else:
        ndb.put_multi(batter_list)

def update_batter_memcache():
    caching.cached_get_all_batters(True)
    time.sleep(.5) # wait .5 seconds while post is entered into memcache

def update_pitcher_db(pitcher_list):
    if RUN_ASYNC:
        pitchers = ndb.put_multi_async(pitcher_list)
    else:
        ndb.put_multi(pitcher_list)

def update_pitcher_memcache():
    caching.cached_get_all_pitchers(True)
    time.sleep(.5) # wait .5 seconds while post is entered into memcache

def put_batters(batter_list):
    update_batter_db(batter_list)
    update_batter_memcache()

def put_pitchers(pitcher_list):
    update_pitcher_db(pitcher_list)
    update_pitcher_memcache()
