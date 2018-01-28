"""CSV Parser"""
import csv
import html_parser
import normalizer
import urllib2
import yql_queries
import pprint

def parse_batters_from_csv(user, user_id, league, csv_string):
    """Parse batter data from CSV file\n
    Args:\n
        csv_string: the CSV data in string form.\n
    Returns:\n
        list of dict of player projections.\n
    Raises:\n
        None.
    """
    # TODO: yahoo not returning all players for some reason
    # avail_players = yql_queries.get_players(league.league_key, user, user_id,
    #                                         "team_tools_db.html", 600, "B", "A")
    batter_dict_list = []
    csv_data = csv_string.split('\n')
    reader = csv.DictReader(csv_data)
    for row in reader:
        batter = {}
        name = ''
        if 'Name' in row:
            name = row["Name"].decode('utf-8').replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "").replace(u"\u201d", "")
        elif '\xef\xbb\xbf"Name"' in row:
            name = row['\xef\xbb\xbf"Name"'].decode('utf-8').replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "").replace(u"\u201d", "")
        norm_name = normalizer.name_normalizer(name)
        # avail_player = [player for player in avail_players
        #                 if player['NORMALIZED_FIRST_NAME'] in norm_name['First']
        #                 and player['LAST_NAME'] in norm_name['Last']]
        pos = []
        status = ""
        # if avail_player:
        #     avail_player = avail_player[0]
        #     pos = avail_player['POS']
        #     status = avail_player['STATUS']
        #questionable_float_cats = ['Off', 'WAR', 'G', '1B', '2B', '3B', 'TB']
        #questionable_string_cats = ['playerid']
        if 'YAHOO' in row:
            pos = row['YAHOO'].decode('utf-8').split('/')
        batter['NAME'] = name
        batter['NORMALIZED_FIRST_NAME'] = norm_name['First']
        batter['LAST_NAME'] = norm_name['Last']
        batter['TEAM'] = normalizer.team_normalizer(row['Team'].decode('utf-8')) if row['Team'] else "FA"
        batter['POS'] = pos
        batter['STATUS'] = status
        batter['category'] = "batter"
        batter['AB'] = float(row['AB'])
        batter['PA'] = float(row['PA'])
        batter['R'] = float(row['R'])
        batter['HR'] = float(row['HR'])
        batter['RBI'] = float(row['RBI'])
        batter['SB'] = float(row['SB'])
        batter['AVG'] = float(row['AVG'])
        batter['OPS'] = float(row['OPS'])
        batter['G'] = float(row['G'])
        # for cat in questionable_float_cats:
        #     if cat in row:
        #         batter[cat] = float(row[cat])
        # for cat in questionable_string_cats:
        #     if cat in row:
        #         batter[cat] = str(row[cat])
        batter_dict_list.append(batter)
    return batter_dict_list
# ['\xef\xbb\xbf"Name"', 'Team', 'G', 'PA', 'AB', 'H', '2B', '3B', 'HR',
#  'R', 'RBI', 'BB', 'SO', 'HBP', 'SB', 'CS', '-1', 'AVG', 'OBP', 'SLG',
# 'OPS', 'wOBA', '-1', 'wRC+', 'BsR', 'Fld', '-1', 'Off', 'Def', 'WAR', 'playerid']

def parse_pitchers_from_csv(user, user_id, league, csv_string):
    """Parse pitcher data from CSV file\n
    Args:\n
        csv_string: the CSV data in string form.\n
    Returns:\n
        list of dict of player projections.\n
    Raises:\n
        None.
    """
    # TODO: yahoo not returning all players for some reason
    # avail_players = yql_queries.get_players(league.league_key, user, user_id,
    #                                         "team_tools_db.html", 600, "P", "A")
    pitcher_dict_list = []
    csv_data = csv_string.split('\n')
    reader = csv.DictReader(csv_data)
    for row in reader:
        pitcher = {}
        name = ''
        if 'Name' in row:
            name = row["Name"].decode('utf-8').replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "").replace(u"\u201d", "")
        elif '\xef\xbb\xbf"Name"' in row:
            name = row['\xef\xbb\xbf"Name"'].decode('utf-8').replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "").replace(u"\u201d", "")
        norm_name = normalizer.name_normalizer(name)
        # avail_player = [player for player in avail_players
        #                 if player['NORMALIZED_FIRST_NAME'] in norm_name['First']
        #                 and player['LAST_NAME'] in norm_name['Last']]
        pos = []
        status = ""
        # if avail_player:
        #     avail_player = avail_player[0]
        #     pos = avail_player['POS']
        #     status = avail_player['STATUS']
#,Name,Team,POS,R/L,G,GS,QS,TBF,IP,W,L,SV,HLD,ERA,SIERA,WHIP,K,BB,H,HBP,ER,R,HR,GB%,FB%,LD%,BABIP
        #questionable_float_cats = ['QS', 'FIP', 'WAR']
        #questionable_string_cats = ['playerid']
        if 'POS' in row:
            pos = row['POS'].decode('utf-8')
        pitcher['NAME'] = name
        pitcher['NORMALIZED_FIRST_NAME'] = norm_name['First']
        pitcher['LAST_NAME'] = norm_name['Last']
        pitcher['TEAM'] = normalizer.team_normalizer(row['Team'].decode('utf-8')) if row['Team'] else "FA"
        pitcher['POS'] = pos
        pitcher['STATUS'] = status
        pitcher['category'] = "pitcher"
        pitcher['IP'] = float(row['IP'])
        pitcher['W'] = float(row['W'])
        pitcher['G'] = float(row['G'])
        pitcher['SV'] = float(row['SV'])
        if 'SO' in row:
            pitcher['K'] = float(row['SO'])
        else:
            pitcher['K'] = float(row['K'])
        pitcher['ERA'] = float(row['ERA'])
        pitcher['WHIP'] = float(row['WHIP'])
        # for cat in questionable_float_cats:
        #     if cat in row:
        #         pitcher[cat] = float(row[cat])
        # for cat in questionable_string_cats:
        #     if cat in row:
        #         pitcher[cat] = str(row[cat])
        pitcher_dict_list.append(pitcher)
    return pitcher_dict_list
# ['\xef\xbb\xbf"Name"', 'Team', 'W', 'L', 'SV', 'HLD', 'ERA', 'GS', 'G',
# 'IP', 'H', 'ER', 'HR', 'SO', 'BB', 'WHIP', 'K/9', 'BB/9', 'FIP', 'WAR', 'playerid']

# print parse_batters_from_csv("/Users/colinaardsma/Downloads/FanGraphsLeaderboard.csv")
# print parse_pitchers_from_csv("/Users/colinaardsma/Downloads/FanGraphs Leaderboard (1).csv")
