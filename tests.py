"""TESTS"""
import urllib
import platform
import html_parser
import player_rater
import player_creator
import tests_long_variables
import fa_vs_team

#VARIABLES
WIN_ROS_BATTER_URL = r"file:///C:\dev\git\tfbps\testing html\2017 Rest of Season Fantasy Baseball Projections - Hitters.html"
WIN_ROS_PITCHER_URL = r"file:///C:\dev\git\tfbps\testing html\2017 Rest of Season Fantasy Baseball Projections - Pitchers.html"
MAC_ROS_BATTER_URL = "file:" + urllib.pathname2url(r"/Users/colinaardsma/git/tfbps/testing html/2017 Rest of Season Fantasy Baseball Projections - Hitters.html")
MAC_ROS_PITCHER_URL = "file:" + urllib.pathname2url(r"/Users/colinaardsma/git/tfbps/testing html/2017 Rest of Season Fantasy Baseball Projections - Pitchers.html")
PLATFORM = platform.sys.platform
# ROS_BATTER_URL = WIN_ROS_BATTER_URL if platform.sys.platform == 'win32' else MAC_ROS_BATTER_URL
# ROS_PITCHER_URL = WIN_ROS_PITCHER_URL if platform.sys.platform == 'win32' else MAC_ROS_PITCHER_URL
ROS_BATTER_URL = "http://www.fantasypros.com/mlb/projections/ros-hitters.php"
ROS_PITCHER_URL = "https://www.fantasypros.com/mlb/projections/ros-pitchers.php"

BATTER_LIST = player_creator.create_full_batter(ROS_BATTER_URL)
PITCHER_LIST = player_creator.create_full_pitcher(ROS_PITCHER_URL)
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
BATTER_FA_LIST = html_parser.yahoo_fa(LEAGUE_NO, "B")
PITCHER_FA_LIST = html_parser.yahoo_fa(LEAGUE_NO, "P")
ROS_PROJ_B_LIST = player_creator.calc_batter_z_score(BATTER_LIST, BATTERS_OVER_ZERO_DOLLARS,
                                                     ONE_DOLLAR_BATTERS, B_DOLLAR_PER_FVAAZ,
                                                     B_PLAYER_POOL_MULT)
ROS_PROJ_P_LIST = player_creator.calc_pitcher_z_score(PITCHER_LIST, PITCHERS_OVER_ZERO_DOLLARS,
                                                      ONE_DOLLAR_PITCHERS, P_DOLLAR_PER_FVAAZ,
                                                      P_PLAYER_POOL_MULT)

SGP_DICT = {'R SGP': 19.16666667, 'HR SGP': 11.5, 'RBI SGP': 20.83333333, 'SB SGP': 7.537037037,
            'OPS SGP': 0.005055555556, 'W SGP': 3.277777778, 'SV SGP': 10.44444444, 'K SGP': 42.5,
            'ERA SGP': -0.08444444444, 'WHIP SGP': -0.01666666667}

# TEAM_LIST = html_parser.yahoo_teams(LEAGUE_NO)
TEAM_LIST = tests_long_variables.TEAM_LIST

# TEAM_DICT = html_parser.get_single_yahoo_team(LEAGUE_NO, "MachadoAboutNothing")
TEAM_DICT = tests_long_variables.TEAM_DICT

LEAGUE_SETTINGS = html_parser.get_league_settings(5091)
# LEAGUE_SETTINGS = tests_long_variables.LEAGUE_SETTINGS

LEAGUE_POS_DICT = html_parser.split_league_pos_types(LEAGUE_SETTINGS["Roster Positions:"])
# LEAGUE_POS_DICT = tests_long_variables.LEAGUE_POS_DICT

CURRENT_STANDINGS = html_parser.get_standings(LEAGUE_NO, TEAM_COUNT)
# CURRENT_STANDINGS = tests_long_variables.CURRENT_STANDINGS

# OPTIMIZED_BATTERS = player_rater.batting_roster_optimizer(TEAM_DICT, ROS_PROJ_B_LIST,
#                                                           LEAGUE_POS_DICT)
# OPTIMIZED_PITCHERS = player_rater.pitching_roster_optimizer(TEAM_DICT, ROS_PROJ_P_LIST,
#                                                             LEAGUE_POS_DICT, CURRENT_STANDINGS,
#                                                             LEAGUE_SETTINGS)
# OPTIMIZED_BENCH = player_rater.bench_roster_optimizer(TEAM_DICT, ROS_PROJ_B_LIST, ROS_PROJ_P_LIST,
#                                                       LEAGUE_POS_DICT, CURRENT_STANDINGS,
#                                                       LEAGUE_SETTINGS, OPTIMIZED_BATTERS,
#                                                       OPTIMIZED_PITCHERS)

FINAL_STATS_PROJECTION = tests_long_variables.FINAL_STATS_PROJECTION
# FINAL_STATS_PROJECTION = player_rater.final_stats_projection(LEAGUE_NO, TEAM_LIST,
#                                                              ROS_PROJ_B_LIST,
#                                                              ROS_PROJ_P_LIST,
#                                                              LEAGUE_POS_DICT,
#                                                              CURRENT_STANDINGS,
#                                                              LEAGUE_SETTINGS)

FINAL_POINTS_PROJECTION = tests_long_variables.FINAL_STATS_PROJECTION
# FINAL_POINTS_PROJECTION = player_rater.rank_list(FINAL_STATS_PROJECTION)

# print OPTIMIZED_BATTERS
# print OPTIMIZED_PITCHERS
# print OPTIMIZED_BENCH
# print player_rater.team_optimizer(TEAM_DICT, ROS_PROJ_B_LIST, ROS_PROJ_P_LIST, LEAGUE_POS_DICT,
#                                   CURRENT_STANDINGS, LEAGUE_SETTINGS)
# print player_rater.rank_list(FINAL_STANDINGS_PROJECTION)
# print html_parser.html_to_document(ROS_BATTER_URL)

# print player_rater.volatility(SGP_DICT, FINAL_STATS_PROJECTION)
print fa_vs_team.batter_projections()
# print PITCHER_LIST

#TESTS

# print player_rater

# print html_parser.get_single_yahoo_team(LEAGUE_NO, "MachadoAboutNothing")
