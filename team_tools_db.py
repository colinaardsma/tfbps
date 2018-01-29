"""Interface with program here"""
# import operator
import time
# next 3 lines are for running locally
import sys
sys.path.append('/usr/local/google_appengine/')
sys.path.append('/usr/local/google_appengine/lib/yaml/lib/')
from google.appengine.ext import db
import urllib
import pprint
import html_parser
import player_rater
import player_creator
import player_models
import queries
import logging
import yql_queries
import caching

RUN_ASYNC = True

# https://developer.yahoo.com/fantasysports/guide/players-collection.html
# https://www.mysportsfeeds.com

# static variables
ROS_BATTER_URL = "http://www.fantasypros.com/mlb/projections/ros-hitters.php"
ROS_PITCHER_URL = "https://www.fantasypros.com/mlb/projections/ros-pitchers.php"
# ROS_BATTER_URL = "file://" + urllib.pathname2url(r"/Users/colinaardsma/git/tfbps/testing html/2017 Rest of Season Fantasy Baseball Projections - Hitters.html")
# ROS_PITCHER_URL = "file://" + urllib.pathname2url(r"/Users/colinaardsma/git/tfbps/testing html/2017 Rest of Season Fantasy Baseball Projections - Pitchers.html")

BATTERS_OVER_ZERO_DOLLARS = 176
PITCHERS_OVER_ZERO_DOLLARS = 124
ONE_DOLLAR_BATTERS = 30
ONE_DOLLAR_PITCHERS = 22
B_DOLLAR_PER_FVAAZ = 3.0
P_DOLLAR_PER_FVAAZ = 2.17
B_PLAYER_POOL_MULT = 2.375
P_PLAYER_POOL_MULT = 4.45
LEAGUE_NO = 5091
TEAM_COUNT = 12
# BATTER_LIST = player_creator.create_full_batter_html(ROS_BATTER_URL)
# PITCHER_LIST = player_creator.create_full_pitcher_html(ROS_PITCHER_URL)
# BATTER_LIST = player_creator.create_full_batter_csv(CSV)
# PITCHER_LIST = player_creator.create_full_pitcher_csv(CSV)

SGP_DICT = {'R SGP': 19.16666667, 'HR SGP': 11.5, 'RBI SGP': 20.83333333, 'SB SGP': 7.537037037,
            'OPS SGP': 0.005055555556, 'W SGP': 3.277777778, 'SV SGP': 10.44444444, 'K SGP': 42.5,
            'ERA SGP': -0.08444444444, 'WHIP SGP': -0.01666666667}

# # dynamic variables
# ROS_PROJ_B_LIST = queries.get_batters()
# ROS_PROJ_P_LIST = queries.get_pitchers()
# ROS_PROJ_B_LIST = player_creator.calc_batter_z_score(BATTER_LIST, BATTERS_OVER_ZERO_DOLLARS,
#                                                      ONE_DOLLAR_BATTERS, B_DOLLAR_PER_FVAAZ,
#                                                      B_PLAYER_POOL_MULT)
# ROS_PROJ_P_LIST = player_creator.calc_pitcher_z_score(PITCHER_LIST, PITCHERS_OVER_ZERO_DOLLARS,
#                                                       ONE_DOLLAR_PITCHERS, P_DOLLAR_PER_FVAAZ,
#                                                       P_PLAYER_POOL_MULT)

# variable defined within methods
# BATTER_FA_LIST = html_parser.yahoo_fa(LEAGUE_NO, "B")
# PITCHER_FA_LIST = html_parser.yahoo_fa(LEAGUE_NO, "P")
# LEAGUE_SETTINGS = html_parser.get_league_settings(LEAGUE_NO)
# CURRENT_STANDINGS = html_parser.get_standings(LEAGUE_NO, int(LEAGUE_SETTINGS['Max Teams:']))
# TEAM_LIST = html_parser.yahoo_teams(LEAGUE_NO)
# LEAGUE_POS_DICT = html_parser.split_league_pos_types(LEAGUE_SETTINGS["Roster Positions:"])

def fa_finder(league_key, user, user_id, redirect):
    """Compare team player values with available FA player values\n
    Args:\n
        league_key: Yahoo! fantasy baseball league number.\n
        team_name: name of the team to retreive.\n
    Returns:\n
        string comparing team values against fa values.\n
    Raises:\n
        None.
    """
    ros_proj_b_list = caching.cached_get_all_batters()
    ros_proj_p_list = caching.cached_get_all_pitchers()

    player_comp = {}
    pitching_fa_list = yql_queries.get_players(league_key, user, user_id, redirect, 300, "P", "FA")
    batting_fa_list = yql_queries.get_players(league_key, user, user_id, redirect, 300, "B", "FA")
    avail_pitching_fas = player_rater.rate_fa(pitching_fa_list, ros_proj_p_list)
    yahoo_team = yql_queries.get_single_team_roster(league_key, user, user_id, redirect)
    # yahoo_team = html_parser.get_single_yahoo_team(league_no, team_name)
    team_pitching_values = player_rater.rate_team(yahoo_team, ros_proj_p_list)
    avail_batting_fas = player_rater.rate_fa(batting_fa_list, ros_proj_b_list)
    team_batting_values = player_rater.rate_team(yahoo_team, ros_proj_b_list)

    player_comp['Team Name'] = yahoo_team['TEAM_NAME']
    player_comp['Pitching FAs'] = avail_pitching_fas
    player_comp['Pitching Team'] = team_pitching_values
    player_comp['Batting FAs'] = avail_batting_fas
    player_comp['Batting Team'] = team_batting_values

    return player_comp

def single_player_rater(player_name):
    """Searches for and returns rating of and individual player\n
    Args:\n
        player_name: name of the player to search for.\n
    Returns:\n
        rated player object.\n
    Raises:\n
        None.
    """
    # player_list = player_rater.single_player_rater_db(player_name)
    # player = player_list[0]
    ros_proj_b_list = caching.cached_get_all_batters()
    ros_proj_p_list = caching.cached_get_all_pitchers()
    player = player_rater.single_player_rater_html(player_name, ros_proj_b_list, ros_proj_p_list)
    player_stats = ""
    if any("P" in pos for pos in player.pos):
        player_stats = ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^25}" +
                        " - {player.wins:^3} - {player.svs:^2} - {player.sos:^3}" +
                        "- {player.era:^4} - {player.whip:^4}\n").format(player=player)
    else:
        player_stats = ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^25}" +
                        " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3}" +
                        " - {player.sbs:^2} - {player.ops:^5}\n").format(player=player)

    return player_stats

def final_standing_projection(league_key, user, user_id, redirect):
    """Returns projection of final standings for league based on\n
    current standings and team projections\n
    Args:\n
        league_no: Yahoo! fantasy baseball league number.\n
    Returns:\n
        Final point standings.\n
    Raises:\n
        None.
    """
    # ros_proj_b_list = player_creator.calc_batter_z_score(BATTER_LIST, BATTERS_OVER_ZERO_DOLLARS,
    #                                                      ONE_DOLLAR_BATTERS, B_DOLLAR_PER_FVAAZ,
    #                                                      B_PLAYER_POOL_MULT)
    # ros_proj_p_list = player_creator.calc_pitcher_z_score(PITCHER_LIST, PITCHERS_OVER_ZERO_DOLLARS,
    #                                                      ONE_DOLLAR_PITCHERS, P_DOLLAR_PER_FVAAZ,
    #                                                      P_PLAYER_POOL_MULT)
    ros_proj_b_list = caching.cached_get_all_batters()
    ros_proj_p_list = caching.cached_get_all_pitchers()
    league_settings = yql_queries.get_league_settings(league_key, user, user_id, redirect)
    league_pos_dict = league_settings['Roster Positions']
    current_standings = yql_queries.get_league_standings(league_key, user, user_id, redirect)
    team_list = yql_queries.get_all_team_rosters(league_key, user, user_id, redirect)
    final_stats = player_rater.final_stats_projection(team_list, ros_proj_b_list,
                                                      ros_proj_p_list, league_pos_dict,
                                                      current_standings, league_settings)
    volatility_standings = player_rater.league_volatility(SGP_DICT, final_stats)
    ranked_standings = player_rater.rank_list(volatility_standings)
    return ranked_standings

def get_keeper_costs(league_key, user, user_id, redirect):
    """Returns current keepers\n
    Args:\n
        league_no: Yahoo! fantasy baseball league number.\n
    Returns:\n
        Final point standings.\n
    Raises:\n
        None.
    """
    keepers = yql_queries.get_keepers(league_key, user, user_id, redirect)
    return keepers

def get_projected_keepers(league_key, user, user_id, redirect):
    """Returns current keepers\n
    Args:\n
        league_no: Yahoo! fantasy baseball league number.\n
    Returns:\n
        Final point standings.\n
    Raises:\n
        None.
    """
    ros_proj_b_list = caching.cached_get_all_batters()
    ros_proj_p_list = caching.cached_get_all_pitchers()
    keepers = yql_queries.get_keepers(league_key, user, user_id, redirect)
    eval_keepers = player_rater.evaluate_keepers(keepers, ros_proj_b_list, ros_proj_p_list)        
    # import pprint
    # pprint.pprint(eval_keepers)
    return eval_keepers

def batter_projections():
    start = time.time()
    projections = caching.cached_get_all_batters()
    end = time.time()
    elapsed = end - start
    logging.info("\r\n***************\r\nGet Batter in %f seconds", elapsed)

    # sorted_proj = sorted(projections, key=lambda x: x.dollarValue, reverse=True)
    return projections

def pitcher_projections():
    start = time.time()
    projections = caching.cached_get_all_pitchers()
    end = time.time()
    elapsed = end - start
    logging.info("\r\n***************\r\nGet Pitcher in %f seconds", elapsed)

    # sorted_proj = sorted(projections, key=lambda x: x.dollarValue, reverse=True)
    return projections

def pull_batters(user, user_id, league, csv):
    start = time.time()
    # batter_list = player_creator.create_full_batter_html(ROS_BATTER_URL)
    batter_list = player_creator.create_full_batter_csv(user, user_id, league, csv)
    end = time.time()
    elapsed = end - start
    logging.info("\r\n***************\r\nBatter Creation in %f seconds", elapsed)

    #delete all records from database before rebuidling
    # if player_models.BatterDB:
    start = time.time()
    batter_query = player_models.BatterProj.all(keys_only=True) #.run() #.fetch(limit=1000) # .all() = "SELECT *"
    end = time.time()
    elapsed = end - start
    logging.info("\r\n***************\r\nBatter Get for Deletion in %f seconds", elapsed)

    start = time.time()
    if RUN_ASYNC:
        db.delete_async(batter_query)
    else:
        db.delete(batter_query)
    end = time.time()
    elapsed = end - start
    logging.info("\r\n***************\r\nBatter Deletion in %f seconds", elapsed)

    start = time.time()
    batters = player_creator.calc_batter_z_score(batter_list, BATTERS_OVER_ZERO_DOLLARS,
                                                 ONE_DOLLAR_BATTERS, B_DOLLAR_PER_FVAAZ,
                                                 B_PLAYER_POOL_MULT)
    batter_models = []
    for batter in batters:
        batter_model = player_models.store_batter(batter)
        batter_models.append(batter_model)
    player_models.put_batters(batter_models)
    player_models.store_batter_values(user.yahooGuid, league, batter_models)
    end = time.time()
    elapsed = end - start
    logging.info("\r\n***************\r\nBatter DB in %f seconds", elapsed)


def pull_pitchers(user, user_id, league, csv):
    start = time.time()
    # pitcher_list = player_creator.create_full_pitcher_html(ROS_PITCHER_URL)
    pitcher_list = player_creator.create_full_pitcher_csv(user, user_id, league, csv)
    end = time.time()
    elapsed = end - start
    logging.info("\r\n***************\r\nPitcher Creation in %f seconds", elapsed)

    #delete all records from database before rebuidling
    # if player_models.PitcherDB:
    start = time.time()
    pitcher_query = player_models.PitcherProj.all(keys_only=True) #.run() #.fetch(limit=1000) # .all() = "SELECT *"
    end = time.time()
    elapsed = end - start
    logging.info("\r\n***************\r\nPitcher Get for Deletion in %f seconds", elapsed)

    start = time.time()
    if RUN_ASYNC:
        db.delete_async(pitcher_query)
    else:
        db.delete(pitcher_query)
    end = time.time()
    elapsed = end - start
    logging.info("\r\n***************\r\nPitcher Deletion in %f seconds", elapsed)

    start = time.time()
    pitchers = player_creator.calc_pitcher_z_score(pitcher_list, PITCHERS_OVER_ZERO_DOLLARS,
                                                   ONE_DOLLAR_PITCHERS, P_DOLLAR_PER_FVAAZ,
                                                   P_PLAYER_POOL_MULT)
    pitcher_models = []
    for pitcher in pitchers:
        pitcher_model = player_models.store_pitcher(pitcher)
        pitcher_models.append(pitcher_model)
    player_models.put_pitchers(pitcher_models)
    player_models.store_pitcher_values(user.yahooGuid, league, pitcher_models)
    end = time.time()
    elapsed = end - start
    logging.info("\r\n***************\r\nPitcher DB in %f seconds", elapsed)


def pull_players(user, user_id, league, pitcher_csv, batter_csv):
    # pitcher_list = player_creator.create_full_pitcher_html(ROS_PITCHER_URL)
    # batter_list = player_creator.create_full_batter_html(ROS_BATTER_URL)
    pitcher_list = player_creator.create_full_pitcher_csv(user, user_id, league, pitcher_csv)
    batter_list = player_creator.create_full_batter_csv(user, user_id, league, batter_csv)
    #delete all records from database before rebuidling
    # if player_models.PitcherDB:
    pitcher_query = player_models.PitcherProj.all() # .all() = "SELECT *"
    pitcher_value_query = player_models.PitcherValue.all() # .all() = "SELECT *"
    # if player_models.BatterDB:
    batter_query = player_models.BatterProj.all() # .all() = "SELECT *"
    batter_value_query = player_models.BatterValue.all() # .all() = "SELECT *"
    pitchers = player_creator.calc_pitcher_z_score(pitcher_list, PITCHERS_OVER_ZERO_DOLLARS,
                                                   ONE_DOLLAR_PITCHERS, P_DOLLAR_PER_FVAAZ,
                                                   P_PLAYER_POOL_MULT)
    batters = player_creator.calc_batter_z_score(batter_list, BATTERS_OVER_ZERO_DOLLARS,
                                                 ONE_DOLLAR_BATTERS, B_DOLLAR_PER_FVAAZ,
                                                 B_PLAYER_POOL_MULT)
    pitcher_models = []
    for pitcher in pitchers:
        pitcher_model = player_models.store_pitcher(pitcher)
        pitcher_models.append(pitcher_model)
    batter_models = []
    for batter in batters:
        batter_model = player_models.store_batter(batter)
        batter_models.append(batter_model)

    if RUN_ASYNC:
        db.delete_async(pitcher_query)
        db.delete_async(batter_query)
        db.put_async(pitcher_models)
        db.put_async(batter_models)
    else:
        db.delete(pitcher_query)
        db.delete(pitcher_value_query)
        db.delete(batter_query)
        db.delete(batter_value_query)
    player_models.put_batters(batter_models)
    player_models.store_batter_values(user.yahooGuid, league, batter_models)
    player_models.put_pitchers(pitcher_models)
    player_models.store_pitcher_values(user.yahooGuid, league, pitcher_models)





# print pull_batters()
# start = time.time()
# print single_player_rater("mike trout")
# # print fa_finder(5091, "MachadoAboutNothing") #42sec #29sec
# # print final_standing_projection(5091) #21sec #5sec
# end = time.time()
# elapsed = end - start
# print "{elapsed:.2f} seconds".format(elapsed=elapsed)
