# """Long Variables for Testing"""
import html_parser
import player_rater
import player_creator

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

# CURRENT_STANDINGS = html_parser.get_standings(LEAGUE_NO, TEAM_COUNT)
CURRENT_STANDINGS = [{'StatsTotalGP': '549', 'StatsOPS': '.840', 'StatsERA': '3.66',
                      'PointsSB': '7', 'StatsRBI': '305', 'StatsR': '338', 'PointsSV': '12',
                      'StatsWHIP': '1.19*', 'StatsHR': '105', 'PointsTotal': '97', 'StatsSB': '37',
                      'PointsTeam': 'Big Sack', 'StatsIP': '415.1', 'PointsRBI': '10',
                      'PointsWHIP': '9', 'StatsK': '405', 'PointsOPS': '12', 'StatsSV': '54',
                      'StatsTeam': 'Big Sack', 'PointsR': '11', 'StatsW': '26', 'PointsW': '6',
                      'PointsK': '8', 'PointsRank': '1', 'PointsERA': '10', 'StatsRank': '1',
                      'PointsHR': '12'},
                     {'StatsTotalGP': '563', 'StatsOPS': '.762', 'StatsERA': '3.56',
                      'PointsSB': '12', 'StatsRBI': '298', 'StatsR': '307', 'PointsSV': '11',
                      'StatsWHIP': '1.22', 'StatsHR': '94', 'PointsTotal': '89', 'StatsSB': '62',
                      'PointsTeam': "R.Odor's PunchOut!!!", 'StatsIP': '444.1', 'PointsRBI': '8',
                      'PointsWHIP': '8', 'StatsK': '389', 'PointsOPS': '4', 'StatsSV': '43',
                      'StatsTeam': "R.Odor's PunchOut!!!", 'PointsR': '9', 'StatsW': '33',
                      'PointsW': '11', 'PointsK': '4', 'PointsRank': '2', 'PointsERA': '12',
                      'StatsRank': '2', 'PointsHR': '10'},
                     {'StatsTotalGP': '533', 'StatsOPS': '.793', 'StatsERA': '3.76',
                      'PointsSB': '6', 'StatsRBI': '304', 'StatsR': '272', 'PointsSV': '10',
                      'StatsWHIP': '1.17*', 'StatsHR': '92', 'PointsTotal': '87', 'StatsSB': '33',
                      'PointsTeam': 'MachadoAboutNothing', 'StatsIP': '464.2', 'PointsRBI': '9',
                      'PointsWHIP': '12', 'StatsK': '425', 'PointsOPS': '9', 'StatsSV': '38',
                      'StatsTeam': 'MachadoAboutNothing', 'PointsR': '3', 'StatsW': '38',
                      'PointsW': '12', 'PointsK': '9', 'PointsRank': '3', 'PointsERA': '8',
                      'StatsRank': '3', 'PointsHR': '9'},
                     {'StatsTotalGP': '562', 'StatsOPS': '.791', 'StatsERA': '3.78',
                      'PointsSB': '8.5', 'StatsRBI': '270', 'StatsR': '341', 'PointsSV': '5',
                      'StatsWHIP': '1.24', 'StatsHR': '84', 'PointsTotal': '78.5', 'StatsSB': '41',
                      'PointsTeam': 'Crow Ned', 'StatsIP': '507.2', 'PointsRBI': '3',
                      'PointsWHIP': '7', 'StatsK': '498', 'PointsOPS': '8', 'StatsSV': '21',
                      'StatsTeam': 'Crow Ned', 'PointsR': '12', 'StatsW': '31', 'PointsW': '10',
                      'PointsK': '12', 'PointsRank': '4', 'PointsERA': '7', 'StatsRank': '4',
                      'PointsHR': '6'},
                     {'StatsTotalGP': '546', 'StatsOPS': '.827', 'StatsERA': '3.79',
                      'PointsSB': '8.5', 'StatsRBI': '311', 'StatsR': '320', 'PointsSV': '8',
                      'StatsWHIP': '1.28', 'StatsHR': '83', 'PointsTotal': '75', 'StatsSB': '41',
                      'PointsTeam': 'The Southsiders', 'StatsIP': '418.0', 'PointsRBI': '11',
                      'PointsWHIP': '4', 'StatsK': '447', 'PointsOPS': '10', 'StatsSV': '28',
                      'StatsTeam': 'The Southsiders', 'PointsR': '10', 'StatsW': '22',
                      'PointsW': '3', 'PointsK': '10', 'PointsRank': '5', 'PointsERA': '6',
                      'StatsRank': '5', 'PointsHR': '4.5'},
                     {'StatsTotalGP': '535', 'StatsOPS': '.838', 'StatsERA': '4.17',
                      'PointsSB': '3', 'StatsRBI': '312', 'StatsR': '301', 'PointsSV': '7',
                      'StatsWHIP': '1.35', 'StatsHR': '101', 'PointsTotal': '66.5', 'StatsSB': '26',
                      'PointsTeam': 'WHIPmyHairBackNForth', 'StatsIP': '410.1', 'PointsRBI': '12',
                      'PointsWHIP': '1', 'StatsK': '394', 'PointsOPS': '11', 'StatsSV': '24',
                      'StatsTeam': 'WHIPmyHairBackNForth', 'PointsR': '8', 'StatsW': '23',
                      'PointsW': '5', 'PointsK': '6.5', 'PointsRank': '6', 'PointsERA': '2',
                      'StatsRank': '6', 'PointsHR': '11'},
                     {'StatsTotalGP': '556', 'StatsOPS': '.763', 'StatsERA': '3.89',
                      'PointsSB': '5', 'StatsRBI': '276', 'StatsR': '297', 'PointsSV': '4',
                      'StatsWHIP': '1.27*', 'StatsHR': '91', 'PointsTotal': '62.5', 'StatsSB': '28',
                      'PointsTeam': 'Yates Dynasty v12.0', 'StatsIP': '453.2', 'PointsRBI': '5',
                      'PointsWHIP': '5', 'StatsK': '494', 'PointsOPS': '5', 'StatsSV': '20',
                      'StatsTeam': 'Yates Dynasty v12.0', 'PointsR': '7', 'StatsW': '28',
                      'PointsW': '7.5', 'PointsK': '11', 'PointsRank': '7', 'PointsERA': '5',
                      'StatsRank': '7', 'PointsHR': '8'},
                     {'StatsTotalGP': '541', 'StatsOPS': '.781', 'StatsERA': '3.59',
                      'PointsSB': '1', 'StatsRBI': '287', 'StatsR': '278', 'PointsSV': '9',
                      'StatsWHIP': '1.17*', 'StatsHR': '89', 'PointsTotal': '62', 'StatsSB': '14',
                      'PointsTeam': '10-Day DL', 'StatsIP': '366.0', 'PointsRBI': '7',
                      'PointsWHIP': '11', 'StatsK': '351', 'PointsOPS': '6', 'StatsSV': '31',
                      'StatsTeam': '10-Day DL', 'PointsR': '5', 'StatsW': '22', 'PointsW': '3',
                      'PointsK': '2', 'PointsRank': '8', 'PointsERA': '11', 'StatsRank': '8',
                      'PointsHR': '7'},
                     {'StatsTotalGP': '541', 'StatsOPS': '.755', 'StatsERA': '3.68',
                      'PointsSB': '10', 'StatsRBI': '263', 'StatsR': '287', 'PointsSV': '2.5',
                      'StatsWHIP': '1.19*', 'StatsHR': '81', 'PointsTotal': '58', 'StatsSB': '45',
                      'PointsTeam': 'NK Sluggers', 'StatsIP': '386.2', 'PointsRBI': '2',
                      'PointsWHIP': '10', 'StatsK': '391', 'PointsOPS': '3', 'StatsSV': '18',
                      'StatsTeam': 'NK Sluggers', 'PointsR': '6', 'StatsW': '28', 'PointsW': '7.5',
                      'PointsK': '5', 'PointsRank': '9', 'PointsERA': '9', 'StatsRank': '9',
                      'PointsHR': '3'},
                     {'StatsTotalGP': '526', 'StatsOPS': '.783', 'StatsERA': '4.04',
                      'PointsSB': '2', 'StatsRBI': '284', 'StatsR': '271', 'PointsSV': '1',
                      'StatsWHIP': '1.27*', 'StatsHR': '83', 'PointsTotal': '43.5', 'StatsSB': '18',
                      'PointsTeam': 'Thome Dont Play Dat', 'StatsIP': '403.1', 'PointsRBI': '6',
                      'PointsWHIP': '6', 'StatsK': '381', 'PointsOPS': '7', 'StatsSV': '10',
                      'StatsTeam': 'Thome Dont Play Dat', 'PointsR': '2', 'StatsW': '30',
                      'PointsW': '9', 'PointsK': '3', 'PointsRank': '10', 'PointsERA': '3',
                      'StatsRank': '10', 'PointsHR': '4.5'},
                     {'StatsTotalGP': '521', 'StatsOPS': '.724', 'StatsERA': '3.92',
                      'PointsSB': '4', 'StatsRBI': '274', 'StatsR': '226', 'PointsSV': '6',
                      'StatsWHIP': '1.34', 'StatsHR': '67', 'PointsTotal': '33.5', 'StatsSB': '27',
                      'PointsTeam': 'Yo Mammas RustyKuntz', 'StatsIP': '432.0', 'PointsRBI': '4',
                      'PointsWHIP': '2', 'StatsK': '394', 'PointsOPS': '1', 'StatsSV': '23',
                      'StatsTeam': 'Yo Mammas RustyKuntz', 'PointsR': '1', 'StatsW': '22',
                      'PointsW': '3', 'PointsK': '6.5', 'PointsRank': '11', 'PointsERA': '4',
                      'StatsRank': '11', 'PointsHR': '2'},
                     {'StatsTotalGP': '546', 'StatsOPS': '.741', 'StatsERA': '4.31',
                      'PointsSB': '11', 'StatsRBI': '202', 'StatsR': '273', 'PointsSV': '2.5',
                      'StatsWHIP': '1.31', 'StatsHR': '62', 'PointsTotal': '27.5', 'StatsSB': '58',
                      'PointsTeam': 'Stats in Binary', 'StatsIP': '329.2', 'PointsRBI': '1',
                      'PointsWHIP': '3', 'StatsK': '345', 'PointsOPS': '2', 'StatsSV': '18',
                      'StatsTeam': 'Stats in Binary', 'PointsR': '4', 'StatsW': '18',
                      'PointsW': '1', 'PointsK': '1', 'PointsRank': '12', 'PointsERA': '1',
                      'StatsRank': '12', 'PointsHR': '1'}]
