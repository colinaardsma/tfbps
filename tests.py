# """TESTS"""
import html_parser
import player_rater
import player_creator

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
TEAM_DICT = {'TEAM_NAME': 'MachadoAboutNothing', 'TEAM_NUMBER': '1',
             'ROSTER': ['Kurt Suzuki', 'Carlos Santana', 'Trea Turner', 'Anthony Rendon',
                        'Manny Machado', 'Adam Duvall', 'Scott Schebler', 'Nelson Cruz',
                        'Tommy Pham', 'Kyle Seager', 'Melky Cabrera', 'Chris Devenski',
                        'Matt Shoemaker', 'Raisel Iglesias', 'Kenley Jansen', 'Tony Watson',
                        'Addison Reed', 'Kenta Maeda', 'Dallas Keuchel', 'Bryce Harper',
                        'Domingo Santana', 'Randal Grichuk', 'Andrew McCutchen', 'Amed Rosario',
                        'Victor Robles', 'Ivan Nova', 'Tanner Roark', 'Felix Hernandez',
                        'J.A. Happ']}

# LEAGUE_SETTINGS = html_parser.get_league_settings(5091)
LEAGUE_SETTINGS = {'Draft Type:': 'Live Auction Draft',
                   'Post Draft Players:': 'Follow Waiver Rules',
                   'New Players Become Available:': 'As soon as Yahoo adds them',
                   'Max Teams:': '12', 'Send unjoined players email reminders:': 'Yes',
                   "Can't Cut List Provider:": 'Yahoo Sports', 'Auto-renew Enabled:': 'Yes',
                   'Max Trades for Entire Season': 'No maximum',
                   'Cash League Settings:': 'Not a cash league', 'Trade Reject Time:': '2',
                   'Keeper Settings:': 'Yes, enable Keeper League Management tools',
                   'League Name:': 'Grays Sports Almanac', 'Roster Changes:': 'Daily - Today',
                   'Keeper Deadline Date:': 'Sun Mar 26 12:00am PDT',
                   'Batters Stat Categories:': 'Runs (R), Home Runs (HR), Runs Batted In (RBI), Stolen Bases (SB), On-base + Slugging Percentage (OPS)',
                   'Invite Permissions:': 'Commissioner Only',
                   'Roster Positions:': 'C, 1B, 2B, 3B, SS, OF, OF, OF, OF, Util, Util, SP, SP, RP, RP, P, P, P, P, BN, BN, BN, BN, BN, BN, DL, DL, NA, NA',
                   'Draft Time:': 'Sat Apr 1 9:00am PDT', 'Trade Review:': 'Commissioner',
                   'Max Games Played:': '162', 'Trade End Date:': 'August 13, 2017',
                   'Max Innings Pitched:': '1500', 'Scoring Type:': 'Rotisserie',
                   'Max Acquisitions for Entire Season:': 'No maximum',
                   'Allow Draft Pick Trades:': 'No', 'Waiver Mode:': 'Standard',
                   'Allow injured players from waivers or free agents to be added directly to IR:': 'No',
                   'League ID#:': '5091', 'Waiver Type:': 'FAAB w/ Continual rolling list tiebreak',
                   'Waiver Time:': '2 days',
                   'Pitchers Stat Categories:': 'Wins (W), Saves (SV), Strikeouts (K), Earned Run Average (ERA), (Walks + Hits)/ Innings Pitched (WHIP)',
                   'Custom League URL:': 'https://baseball.fantasysports.yahoo.com/league/grayssportsalmanac',
                   'Player Universe:': 'All baseball', 'Make League Publicly Viewable:': 'Yes',
                   'Start Scoring on:': 'Sunday, Apr 2'}

# LEAGUE_POS_DICT = LEAGUE_SETTINGS["Roster Positions:"]
LEAGUE_POS_DICT = {'Pitching POS': ['SP', 'SP', 'RP', 'RP', 'P', 'P', 'P', 'P'],
                   'Bench POS': ['BN', 'BN', 'BN', 'BN', 'BN', 'BN'],
                   'DL POS': ['DL', 'DL'],
                   'Batting POS': ['C', '1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF',
                                   'OF', 'Util', 'Util'],
                   'NA POS': ['NA', 'NA']}


#TESTS
# print LEAGUE_SETTINGS

print player_rater.roster_optimizer(TEAM_DICT, ROS_PROJ_B_LIST, LEAGUE_POS_DICT)

# print ROS_PROJ_B_LIST

