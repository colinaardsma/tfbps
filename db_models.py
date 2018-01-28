"""Models Module"""
import sys
from google.appengine.ext import db
# sys.path.insert(0, '//Users/colinaardsma/google_appengine')
#define columns of database objects
import caching
import time
import queries
import pprint
import datetime
# import hashing

class League(db.Model):
    """The League Database Model"""
    # Descriptive Properties
    league_name = db.StringProperty(required=True)
    league_key = db.StringProperty(required=True)
    team_count = db.IntegerProperty(required=True)
    max_ip = db.IntegerProperty(required=True)
    season = db.IntegerProperty(required=True)
    # roster_pos = db.ListProperty(required=True)
    batting_pos = db.StringListProperty(required=True)
    pitcher_pos = db.StringListProperty(required=True)
    bench_pos = db.StringListProperty(required=True)
    dl_pos = db.StringListProperty(required=True)
    na_pos = db.StringListProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    # Advanced Stats
    total_money_spent = db.IntegerProperty()
    money_spent_on_batters = db.IntegerProperty()
    money_spent_on_pitchers = db.IntegerProperty()
    batter_budget_pct = db.FloatProperty()
    pitcher_budget_pct = db.FloatProperty()
    batters_over_zero_dollars = db.IntegerProperty()
    pitchers_over_zero_dollars = db.IntegerProperty()
    one_dollar_batters = db.IntegerProperty()
    one_dollar_pitchers = db.IntegerProperty()
    b_dollar_per_fvaaz = db.FloatProperty()
    p_dollar_per_fvaaz = db.FloatProperty()
    b_player_pool_mult = db.FloatProperty()
    p_player_pool_mult = db.FloatProperty()
    # SGP
    r_sgp = db.FloatProperty()
    hr_sgp = db.FloatProperty()
    rbi_sgp = db.FloatProperty()
    sb_sgp = db.FloatProperty()
    ops_sgp = db.FloatProperty()
    avg_sgp = db.FloatProperty()
    w_sgp = db.FloatProperty()
    sv_sgp = db.FloatProperty()
    k_sgp = db.FloatProperty()
    era_sgp = db.FloatProperty()
    whip_sgp = db.FloatProperty()
    # Historical
    prev_year_key = db.StringProperty()
    # 3 Year Advanced Stats Avg
    total_money_spent_avg = db.IntegerProperty()
    money_spent_on_batters_avg = db.IntegerProperty()
    money_spent_on_pitchers_avg = db.IntegerProperty()
    batter_budget_pct_avg = db.FloatProperty()
    pitcher_budget_pct_avg = db.FloatProperty()
    batters_over_zero_dollars_avg = db.IntegerProperty()
    pitchers_over_zero_dollars_avg = db.IntegerProperty()
    one_dollar_batters_avg = db.IntegerProperty()
    one_dollar_pitchers_avg = db.IntegerProperty()
    b_dollar_per_fvaaz_avg = db.FloatProperty()
    p_dollar_per_fvaaz_avg = db.FloatProperty()
    b_player_pool_mult_avg = db.FloatProperty()
    p_player_pool_mult_avg = db.FloatProperty()
    # 3 Year SGP Avg
    r_sgp_avg = db.FloatProperty()
    hr_sgp_avg = db.FloatProperty()
    rbi_sgp_avg = db.FloatProperty()
    sb_sgp_avg = db.FloatProperty()
    ops_sgp_avg = db.FloatProperty()
    avg_sgp_avg = db.FloatProperty()
    w_sgp_avg = db.FloatProperty()
    sv_sgp_avg = db.FloatProperty()
    k_sgp_avg = db.FloatProperty()
    era_sgp_avg = db.FloatProperty()
    whip_sgp_avg = db.FloatProperty()

def store_league(league_name, league_key, team_count, max_ip, batting_pos, pitcher_pos,
                 bench_pos, dl_pos, na_pos, prev_year_key, season, r_sgp=0.00, hr_sgp=0.00,
                 rbi_sgp=0.00, sb_sgp=0.00, ops_sgp=0.00, avg_sgp=0.00, w_sgp=0.00,
                 sv_sgp=0.00, k_sgp=0.00, era_sgp=0.00, whip_sgp=0.00,
                 batters_over_zero_dollars=0.00, pitchers_over_zero_dollars=0.00,
                 one_dollar_batters=0.00, one_dollar_pitchers=0.00, total_money_spent=0,
                 money_spent_on_batters=0.00, money_spent_on_pitchers=0.00,
                 batter_budget_pct=0.00, pitcher_budget_pct=0.00,
                 b_dollar_per_fvaaz=0.00, p_dollar_per_fvaaz=0.00,
                 b_player_pool_mult=0.00, p_player_pool_mult=0.00):
    league = League(league_name=league_name, league_key=league_key, team_count=team_count,
                    max_ip=max_ip, batting_pos=batting_pos, pitcher_pos=pitcher_pos,
                    bench_pos=bench_pos, dl_pos=dl_pos, na_pos=na_pos, prev_year_key=prev_year_key,
                    season=season, r_sgp=r_sgp, hr_sgp=hr_sgp, rbi_sgp=rbi_sgp, sb_sgp=sb_sgp,
                    ops_sgp=ops_sgp, avg_sgp=avg_sgp, w_sgp=w_sgp, sv_sgp=sv_sgp, k_sgp=k_sgp,
                    era_sgp=era_sgp, whip_sgp=whip_sgp,
                    batters_over_zero_dollars=batters_over_zero_dollars,
                    pitchers_over_zero_dollars=pitchers_over_zero_dollars,
                    one_dollar_batters=one_dollar_batters, one_dollar_pitchers=one_dollar_pitchers,
                    total_money_spent=total_money_spent, money_spent_on_batters=money_spent_on_batters,
                    money_spent_on_pitchers=money_spent_on_pitchers,
                    batter_budget_pct=batter_budget_pct, pitcher_budget_pct=pitcher_budget_pct,
                    b_dollar_per_fvaaz=b_dollar_per_fvaaz, p_dollar_per_fvaaz=p_dollar_per_fvaaz,
                    b_player_pool_mult=b_player_pool_mult, p_player_pool_mult=p_player_pool_mult)
    db.put(league)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache
    # league = caching.cached_user_by_name(username)
    # league_id = league.key().id()
    update_league_memcache(league_key)
    return league

def calc_three_year_avgs(league_key):
    r_sgp_list = []
    rbi_sgp_list = []
    hr_sgp_list = []
    sb_sgp_list = []
    avg_sgp_list = []
    ops_sgp_list = []
    w_sgp_list = []
    sv_sgp_list = []
    k_sgp_list = []
    era_sgp_list = []
    whip_sgp_list = []
    total_money_spent_avg_list = []
    money_spent_on_batters_avg_list = []
    money_spent_on_pitchers_avg_list = []
    batter_budget_pct_avg_list = []
    pitcher_budget_pct_avg_list = []
    batters_over_zero_dollars_avg_list = []
    pitchers_over_zero_dollars_avg_list = []
    one_dollar_batters_avg_list = []
    one_dollar_pitchers_avg_list = []
    b_dollar_per_fvaaz_avg_list = []
    p_dollar_per_fvaaz_avg_list = []
    # TODO: populate mults
    b_player_pool_mult_avg_list = []
    p_player_pool_mult_avg_list = []

    league = caching.cached_get_leagues_by_league_key(league_key)
    if league:
        r_sgp_list.append(league.r_sgp)
        rbi_sgp_list.append(league.rbi_sgp)
        hr_sgp_list.append(league.hr_sgp)
        sb_sgp_list.append(league.sb_sgp)
        avg_sgp_list.append(league.avg_sgp)
        ops_sgp_list.append(league.ops_sgp)
        w_sgp_list.append(league.w_sgp)
        sv_sgp_list.append(league.sv_sgp)
        k_sgp_list.append(league.k_sgp)
        era_sgp_list.append(league.era_sgp)
        whip_sgp_list.append(league.whip_sgp)
        total_money_spent_avg_list.append(league.total_money_spent)
        money_spent_on_batters_avg_list.append(league.money_spent_on_batters)
        money_spent_on_pitchers_avg_list.append(league.money_spent_on_pitchers)
        batter_budget_pct_avg_list.append(league.batter_budget_pct)
        pitcher_budget_pct_avg_list.append(league.pitcher_budget_pct)
        batters_over_zero_dollars_avg_list.append(league.batters_over_zero_dollars)
        pitchers_over_zero_dollars_avg_list.append(league.pitchers_over_zero_dollars)
        one_dollar_batters_avg_list.append(league.one_dollar_batters)
        one_dollar_pitchers_avg_list.append(league.one_dollar_pitchers)
        b_dollar_per_fvaaz_avg_list.append(league.b_dollar_per_fvaaz)
        p_dollar_per_fvaaz_avg_list.append(league.p_dollar_per_fvaaz)
        b_player_pool_mult_avg_list.append(league.b_player_pool_mult)
        p_player_pool_mult_avg_list.append(league.p_player_pool_mult)
        prev_year_league = caching.cached_get_leagues_by_league_key(league.prev_year_key)
        if prev_year_league:
            r_sgp_list.append(prev_year_league.r_sgp)
            rbi_sgp_list.append(prev_year_league.rbi_sgp)
            hr_sgp_list.append(prev_year_league.hr_sgp)
            sb_sgp_list.append(prev_year_league.sb_sgp)
            avg_sgp_list.append(prev_year_league.avg_sgp)
            ops_sgp_list.append(prev_year_league.ops_sgp)
            w_sgp_list.append(prev_year_league.w_sgp)
            sv_sgp_list.append(prev_year_league.sv_sgp)
            k_sgp_list.append(prev_year_league.k_sgp)
            era_sgp_list.append(prev_year_league.era_sgp)
            whip_sgp_list.append(prev_year_league.whip_sgp)
            total_money_spent_avg_list.append(prev_year_league.total_money_spent)
            money_spent_on_batters_avg_list.append(prev_year_league.money_spent_on_batters)
            money_spent_on_pitchers_avg_list.append(prev_year_league.money_spent_on_pitchers)
            batter_budget_pct_avg_list.append(prev_year_league.batter_budget_pct)
            pitcher_budget_pct_avg_list.append(prev_year_league.pitcher_budget_pct)
            batters_over_zero_dollars_avg_list.append(prev_year_league.batters_over_zero_dollars)
            pitchers_over_zero_dollars_avg_list.append(prev_year_league.pitchers_over_zero_dollars)
            one_dollar_batters_avg_list.append(prev_year_league.one_dollar_batters)
            one_dollar_pitchers_avg_list.append(prev_year_league.one_dollar_pitchers)
            b_dollar_per_fvaaz_avg_list.append(prev_year_league.b_dollar_per_fvaaz)
            p_dollar_per_fvaaz_avg_list.append(prev_year_league.p_dollar_per_fvaaz)
            b_player_pool_mult_avg_list.append(prev_year_league.b_player_pool_mult)
            p_player_pool_mult_avg_list.append(prev_year_league.p_player_pool_mult)
            two_years_prev_league = caching.cached_get_leagues_by_league_key(prev_year_league.prev_year_key)
            if two_years_prev_league:
                r_sgp_list.append(two_years_prev_league.r_sgp)
                rbi_sgp_list.append(two_years_prev_league.rbi_sgp)
                hr_sgp_list.append(two_years_prev_league.hr_sgp)
                sb_sgp_list.append(two_years_prev_league.sb_sgp)
                avg_sgp_list.append(two_years_prev_league.avg_sgp)
                ops_sgp_list.append(two_years_prev_league.ops_sgp)
                w_sgp_list.append(two_years_prev_league.w_sgp)
                sv_sgp_list.append(two_years_prev_league.sv_sgp)
                k_sgp_list.append(two_years_prev_league.k_sgp)
                era_sgp_list.append(two_years_prev_league.era_sgp)
                whip_sgp_list.append(two_years_prev_league.whip_sgp)
                total_money_spent_avg_list.append(two_years_prev_league.total_money_spent)
                money_spent_on_batters_avg_list.append(two_years_prev_league.money_spent_on_batters)
                money_spent_on_pitchers_avg_list.append(two_years_prev_league.money_spent_on_pitchers)
                batter_budget_pct_avg_list.append(two_years_prev_league.batter_budget_pct)
                pitcher_budget_pct_avg_list.append(two_years_prev_league.pitcher_budget_pct)
                batters_over_zero_dollars_avg_list.append(two_years_prev_league.batters_over_zero_dollars)
                pitchers_over_zero_dollars_avg_list.append(two_years_prev_league.pitchers_over_zero_dollars)
                one_dollar_batters_avg_list.append(two_years_prev_league.one_dollar_batters)
                one_dollar_pitchers_avg_list.append(two_years_prev_league.one_dollar_pitchers)
                b_dollar_per_fvaaz_avg_list.append(two_years_prev_league.b_dollar_per_fvaaz)
                p_dollar_per_fvaaz_avg_list.append(two_years_prev_league.p_dollar_per_fvaaz)
                b_player_pool_mult_avg_list.append(two_years_prev_league.b_player_pool_mult)
                p_player_pool_mult_avg_list.append(two_years_prev_league.p_player_pool_mult)
    r_sgp_avg = sum(r_sgp_list) / len(r_sgp_list)
    rbi_sgp_avg = sum(rbi_sgp_list) / len(rbi_sgp_list)
    hr_sgp_avg = sum(hr_sgp_list) / len(hr_sgp_list)
    sb_sgp_avg = sum(sb_sgp_list) / len(sb_sgp_list)
    avg_sgp_avg = sum(avg_sgp_list) / len(avg_sgp_list)
    ops_sgp_avg = sum(ops_sgp_list) / len(ops_sgp_list)
    w_sgp_avg = sum(w_sgp_list) / len(w_sgp_list)
    sv_sgp_avg = sum(sv_sgp_list) / len(sv_sgp_list)
    k_sgp_avg = sum(k_sgp_list) / len(k_sgp_list)
    era_sgp_avg = sum(era_sgp_list) / len(era_sgp_list)
    whip_sgp_avg = sum(whip_sgp_list) / len(whip_sgp_list)
    total_money_spent_avg = sum(total_money_spent_avg_list) / len(total_money_spent_avg_list)
    money_spent_on_batters_avg = (sum(money_spent_on_batters_avg_list)
                                  / len(money_spent_on_batters_avg_list))
    money_spent_on_pitchers_avg = (sum(money_spent_on_pitchers_avg_list)
                                   / len(money_spent_on_pitchers_avg_list))
    batter_budget_pct_avg = sum(batter_budget_pct_avg_list) / len(batter_budget_pct_avg_list)
    pitcher_budget_pct_avg = sum(pitcher_budget_pct_avg_list) / len(pitcher_budget_pct_avg_list)
    batters_over_zero_dollars_avg = (sum(batters_over_zero_dollars_avg_list)
                                     / len(batters_over_zero_dollars_avg_list))
    pitchers_over_zero_dollars_avg = (sum(pitchers_over_zero_dollars_avg_list)
                                      / len(pitchers_over_zero_dollars_avg_list))
    one_dollar_batters_avg = sum(one_dollar_batters_avg_list) / len(one_dollar_batters_avg_list)
    one_dollar_pitchers_avg = sum(one_dollar_pitchers_avg_list) / len(one_dollar_pitchers_avg_list)
    b_dollar_per_fvaaz_avg = sum(b_dollar_per_fvaaz_avg_list) / len(b_dollar_per_fvaaz_avg_list)
    p_dollar_per_fvaaz_avg = sum(p_dollar_per_fvaaz_avg_list) / len(p_dollar_per_fvaaz_avg_list)
    b_player_pool_mult_avg = sum(b_player_pool_mult_avg_list) / len(b_player_pool_mult_avg_list)
    p_player_pool_mult_avg = sum(p_player_pool_mult_avg_list) / len(p_player_pool_mult_avg_list)

    league.r_sgp_avg = r_sgp_avg
    league.hr_sgp_avg = hr_sgp_avg
    league.rbi_sgp_avg = rbi_sgp_avg
    league.sb_sgp_avg = sb_sgp_avg
    league.ops_sgp_avg = ops_sgp_avg
    league.avg_sgp_avg = avg_sgp_avg
    league.w_sgp_avg = w_sgp_avg
    league.sv_sgp_avg = sv_sgp_avg
    league.k_sgp_avg = k_sgp_avg
    league.era_sgp_avg = era_sgp_avg
    league.whip_sgp_avg = whip_sgp_avg
    league.total_money_spent_avg = total_money_spent_avg
    league.money_spent_on_batters_avg = money_spent_on_batters_avg
    league.money_spent_on_pitchers_avg = money_spent_on_pitchers_avg
    league.batter_budget_pct_avg = batter_budget_pct_avg
    league.pitcher_budget_pct_avg = pitcher_budget_pct_avg
    league.batters_over_zero_dollars_avg = batters_over_zero_dollars_avg
    league.pitchers_over_zero_dollars_avg = pitchers_over_zero_dollars_avg
    league.one_dollar_batters_avg = one_dollar_batters_avg
    league.one_dollar_pitchers_avg = one_dollar_pitchers_avg
    league.b_dollar_per_fvaaz_avg = b_dollar_per_fvaaz_avg
    league.p_dollar_per_fvaaz_avg = p_dollar_per_fvaaz_avg
    league.b_player_pool_mult_avg = b_player_pool_mult_avg
    league.p_player_pool_mult_avg = p_player_pool_mult_avg

    db.put(league)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache
    update_league_memcache(league_key)
    return league

def update_league_memcache(league_key):
    caching.cached_get_leagues_by_league_key(league_key, True)
    caching.cached_get_all_leagues(True)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache

class User(db.Model):
    """The User database model"""
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    authorization = db.StringProperty(required=True)
    yahooGuid = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    last_accessed = db.DateTimeProperty(auto_now=True)
    location = db.GeoPtProperty()
    access_token = db.StringProperty()
    token_expiration = db.DateTimeProperty()
    refresh_token = db.StringProperty()
    main_league = db.StringProperty()

def store_user(username, password, email, location = None, yahooGuid = None, authorization = "basic"):
    user = User(username=username, password=password, email=email, location=location,
                yahooGuid=yahooGuid, authorization=authorization, access_token=None,
                token_expiration=None, refresh_token=None)
    db.put(user)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache
    user = caching.cached_user_by_name(username)
    user_id = user.key().id()
    update_user_memcache(user, user_id)
    return user

def update_user(user, user_id, username=None, hashed_password=None, email=None,
                authorization=None, yahooGuid=None, last_accessed=None,
                location=None, access_token=None, token_expiration=None,
                refresh_token=None, main_league=None):
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
    if main_league:
        user.main_league = main_league
    db.put(user)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache
    update_user_memcache(user, user_id)
    return user

def update_user_memcache(user, user_id):
    caching.cached_user_by_name(user.username, True)
    caching.cached_check_username(user.username, True)
    caching.cached_get_user_by_id(user_id, True)
    caching.cached_get_users(True)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache

class User_League(db.Model):
    """Links between Users and Leagues"""
    user = db.ReferenceProperty(User)
    league = db.ReferenceProperty(League)
    user_guid = db.StringProperty()
    league_key = db.StringProperty()

def store_user_league(user, league):
    user_league = User_League(user=user, league=league, user_guid=user.yahooGuid,
                              league_key=league.league_key)
    db.put(user_league)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache
    # league = caching.cached_user_by_name(username)
    # league_id = league.key().id()
    update_user_league_memcache(user)
    return user_league

def update_user_league_memcache(user):
    caching.cached_get_all_user_leagues_by_user(user, True)
    time.sleep(.5) # wait .5 seconds while post is entered into db and memcache
