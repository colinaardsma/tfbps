"""CSV Parser"""
import csv
import html_parser
import normalizer
import urllib2

def parse_batters_from_csv(csv_string):
    """Parse batter data from CSV file\n
    Args:\n
        csv_string: the CSV data in string form.\n
    Returns:\n
        list of dict of player projections.\n
    Raises:\n
        None.
    """
    avail_players = html_parser.yahoo_players(5091, "B", 300, True)
    batter_dict_list = []
    csv_data = csv_string.split('\n')
    reader = csv.DictReader(csv_data)
    for row in reader:
        batter = {}
        norm_name = normalizer.name_normalizer(row['\xef\xbb\xbf"Name"'])
        avail_player = [player for player in avail_players
                        if player['NORMALIZED_FIRST_NAME'] in norm_name['First']
                        and player['LAST_NAME'] in norm_name['Last']]
        pos = []
        status = ""
        if avail_player:
            avail_player = avail_player[0]
            pos = avail_player['POS'].split(",")
            status = avail_player['DL_NA_STATUS']
        batter['NAME'] = row['\xef\xbb\xbf"Name"']
        batter['NORMALIZED_FIRST_NAME'] = norm_name['First']
        batter['LAST_NAME'] = norm_name['Last']
        batter['TEAM'] = row['Team'] if row['Team'] else "FA"
        batter['POS'] = pos
        batter['STATUS'] = status
        batter['category'] = "batter"
        # batter['AB'] = int(row['AB']) if row['AB'] else int((row['PA'] - row['BB'] - row['HBP']) * .99)
        batter['AB'] = int(row['AB'])
        batter['PA'] = int(row['PA'])
        batter['R'] = int(row['R'])
        batter['HR'] = int(row['HR'])
        batter['RBI'] = int(row['RBI'])
        batter['SB'] = int(row['SB'])
        batter['AVG'] = float(row['AVG'])
        batter['OPS'] = float(row['OPS'])
        batter['Off'] = float(row['Off'])
        batter['WAR'] = float(row['WAR'])
        batter['playerid'] = row['playerid']
        batter_dict_list.append(batter)
    return batter_dict_list
# ['\xef\xbb\xbf"Name"', 'Team', 'G', 'PA', 'AB', 'H', '2B', '3B', 'HR',
#  'R', 'RBI', 'BB', 'SO', 'HBP', 'SB', 'CS', '-1', 'AVG', 'OBP', 'SLG',
# 'OPS', 'wOBA', '-1', 'wRC+', 'BsR', 'Fld', '-1', 'Off', 'Def', 'WAR', 'playerid']

def parse_pitchers_from_csv(csv_string):
    """Parse pitcher data from CSV file\n
    Args:\n
        csv_string: the CSV data in string form.\n
    Returns:\n
        list of dict of player projections.\n
    Raises:\n
        None.
    """
    avail_players = html_parser.yahoo_players(5091, "P", 300, True)
    pitcher_dict_list = []
    csv_data = csv_string.split('\n')
    reader = csv.DictReader(csv_data)
    for row in reader:
        pitcher = {}
        norm_name = normalizer.name_normalizer(row['\xef\xbb\xbf"Name"'])
        avail_player = [player for player in avail_players
                        if player['NORMALIZED_FIRST_NAME'] in norm_name['First']
                        and player['LAST_NAME'] in norm_name['Last']]
        pos = []
        status = ""
        if avail_player:
            avail_player = avail_player[0]
            pos = avail_player['POS'].split(",")
            status = avail_player['DL_NA_STATUS']
        pitcher['NAME'] = row['\xef\xbb\xbf"Name"']
        pitcher['TEAM'] = row['Team'] if row['Team'] else "FA"
        pitcher['POS'] = pos
        pitcher['STATUS'] = status
        pitcher['category'] = "pitcher"
        pitcher['IP'] = row['IP']
        pitcher['W'] = row['W']
        pitcher['SV'] = row['SV']
        pitcher['K'] = row['SO']
        pitcher['ERA'] = row['ERA']
        pitcher['WHIP'] = row['WHIP']
        pitcher['FIP'] = row['FIP']
        pitcher['WAR'] = row['WAR']
        pitcher['playerid'] = row['playerid']
        pitcher_dict_list.append(pitcher)
    return pitcher_dict_list
# ['\xef\xbb\xbf"Name"', 'Team', 'W', 'L', 'SV', 'HLD', 'ERA', 'GS', 'G',
# 'IP', 'H', 'ER', 'HR', 'SO', 'BB', 'WHIP', 'K/9', 'BB/9', 'FIP', 'WAR', 'playerid']

# print parse_batters_from_csv("/Users/colinaardsma/Downloads/FanGraphsLeaderboard.csv")
# print parse_pitchers_from_csv("/Users/colinaardsma/Downloads/FanGraphs Leaderboard (1).csv")
