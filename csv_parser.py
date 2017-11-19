"""CSV Parser"""
import csv
import html_parser
import normalizer

def parse_batters_from_csv(csv_file):
    """Parse batter data from CSV file\n
    Args:\n
        csv_file: the CSV file.\n
    Returns:\n
        list of dict of player projections.\n
    Raises:\n
        None.
    """
    avail_players = html_parser.yahoo_players(5091, "B", 300, True)
    batter_dict_list = []
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            batter = {}
            norm_name = normalizer.name_normalizer(row['\xef\xbb\xbf"Name"'])
            avail_player = [ player for player in avail_players if player['NORMALIZED_FIRST_NAME'] in norm_name['First'] and player['LAST_NAME'] in norm_name['Last'] ]
            batter['Name'] = row['\xef\xbb\xbf"Name"']
            batter['NORMALIZED_FIRST_NAME'] = norm_name['First']
            batter['LAST_NAME'] = norm_name['Last']
            batter['TEAM'] = row['Team']
            batter['POS'] = avail_player['POS']
            batter['STATUS'] = avail_player['STATUS']
            batter['category'] = "batter"
            batter['AB'] = row['AB']
            batter['R'] = row['R']
            batter['HR'] = row['HR']
            batter['RBI'] = row['RBI']
            batter['SB'] = row['SB']
            batter['AVG'] = row['AVG']
            batter['OPS'] = row['OPS']
            batter_dict_list.append(batter)
    return batter_dict_list
# ['\xef\xbb\xbf"Name"', 'Team', 'G', 'PA', 'AB', 'H', '2B', '3B', 'HR', 'R', 'RBI', 'BB', 'SO', 'HBP', 'SB', 'CS', '-1', 'AVG', 'OBP', 'SLG', 'OPS', 'wOBA', '-1', 'wRC+', 'BsR', 'Fld', '-1', 'Off', 'Def', 'WAR', 'playerid']

def parse_pitchers_from_csv(csv_file):
    """Parse pitcher data from CSV file\n
    Args:\n
        csv_file: the CSV file.\n
    Returns:\n
        list of dict of player projections.\n
    Raises:\n
        None.
    """
    pitcher_dict_list = []
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pitcher = {}
            pitcher['Name'] = row['\xef\xbb\xbf"Name"']
            pitcher['TEAM'] = row['Team']
            pitcher['POS'] = html_parser.parse_pos_from_url(row['playerid'])
            # TODO: how to incorporate minors data?
            # batter['STATUS'] = row['STATUS']
            pitcher['category'] = "pitcher"
            pitcher['AB'] = row['IP']
            pitcher['R'] = row['W']
            pitcher['HR'] = row['SV']
            pitcher['RBI'] = row['SO']
            pitcher['SB'] = row['ERA']
            pitcher['AVG'] = row['WHIP']
            pitcher['playerid'] = row['playerid']
            pitcher_dict_list.append(pitcher)
    return pitcher_dict_list
# ['\xef\xbb\xbf"Name"', 'Team', 'W', 'L', 'SV', 'HLD', 'ERA', 'GS', 'G', 'IP', 'H', 'ER', 'HR', 'SO', 'BB', 'WHIP', 'K/9', 'BB/9', 'FIP', 'WAR', 'playerid']

print parse_batters_from_csv("/Users/colinaardsma/Downloads/FanGraphs Leaderboard.csv")
# print parse_pitchers_from_csv("/Users/colinaardsma/Downloads/FanGraphs Leaderboard (1).csv")
