# """TESTS"""
import html_parser
import player_rater
import player_creator
import tests_long_variables

#VARIABLES
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

# TEAM_DICT = html_parser.get_single_yahoo_team(LEAGUE_NO, "MachadoAboutNothing")
TEAM_DICT = tests_long_variables.TEAM_DICT

# LEAGUE_SETTINGS = html_parser.get_league_settings(5091)
LEAGUE_SETTINGS = tests_long_variables.LEAGUE_SETTINGS

# LEAGUE_POS_DICT = LEAGUE_SETTINGS["Roster Positions:"]
LEAGUE_POS_DICT = tests_long_variables.LEAGUE_POS_DICT

# CURRENT_STANDINGS = html_parser.get_standings(LEAGUE_NO, TEAM_COUNT)
CURRENT_STANDINGS = tests_long_variables.CURRENT_STANDINGS


#TESTS
# print LEAGUE_SETTINGS
# print player_rater.batting_roster_optimizer(TEAM_DICT, ROS_PROJ_B_LIST, LEAGUE_POS_DICT)
print player_rater.pitching_roster_optimizer(TEAM_DICT, ROS_PROJ_P_LIST, LEAGUE_POS_DICT,
                                             CURRENT_STANDINGS, LEAGUE_SETTINGS)
