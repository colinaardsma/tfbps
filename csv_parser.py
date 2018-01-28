"""CSV Parser"""
import csv
import html_parser
import normalizer
import urllib2
import yql_queries
import pprint

def parse_batters_from_csv(user, user_id, league, csv_file):
    """Parse batter data from CSV file\n
    Args:\n
        csv_file: the CSV file.\n
    Returns:\n
        list of dict of player projections.\n
    Raises:\n
        None.
    """
    batter_dict_list = []
    reader = csv.DictReader(csv_file.file)
    for row in reader:
        batter = {}
        name = ''
        if 'Name' in row:
            name = row["Name"].decode('utf-8').replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "").replace(u"\u201d", "")
        elif '\xef\xbb\xbf"Name"' in row:
            name = row['\xef\xbb\xbf"Name"'].decode('utf-8').replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "").replace(u"\u201d", "")

        if ((row['AB'] is not None and float(row['AB']) == 0.0) or
                (row['OPS'] is not None and float(row['OPS']) == 0.000) or
                (row['AVG'] is not None and float(row['AVG']) == 0.000) or
                (name is None or name == '') or float(row['G']) <= 0.0):
                # or not row["POS"]):
            continue

        norm_name = normalizer.name_normalizer(name)
        pos = []
        status = ""

        if 'YAHOO' in row:
            pos = row['YAHOO'].decode('utf-8').split('/')
        batter['NAME'] = name
        batter['NORMALIZED_FIRST_NAME'] = norm_name['First']
        batter['LAST_NAME'] = norm_name['Last']
        batter['TEAM'] = (normalizer.team_normalizer(row['Team'].decode('utf-8'))
                          if row['Team'] else "FA")
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

def parse_pitchers_from_csv(user, user_id, league, csv_file):
    """Parse pitcher data from CSV file\n
    Args:\n
        csv_file: the CSV file.\n
    Returns:\n
        list of dict of player projections.\n
    Raises:\n
        None.
    """
    pitcher_dict_list = []
    reader = csv.DictReader(csv_file.file)
    max_ip = 0.0
    for row in reader:
        if float(row['IP']) > max_ip:
            max_ip = float(row['IP'])
    print "MAX IP:"
    print max_ip
    csv_file.file.seek(0)
    reader = csv.DictReader(csv_file.file)
    for row in reader:
        pitcher = {}
        name = ''
        if 'Name' in row:
            name = row["Name"].decode('utf-8').replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "").replace(u"\u201d", "")
        elif '\xef\xbb\xbf"Name"' in row:
            name = row['\xef\xbb\xbf"Name"'].decode('utf-8').replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "").replace(u"\u201d", "")

        if (row['IP'] is None or float(row['IP']) <= (max_ip * 0.05) or
                row['W'] is None or float(row['W']) < 0.0 or
                row['SV'] is None or float(row['SV']) < 0.0 or
                row['K'] is None or float(row['K']) < 0.0 or
                row['ERA'] is None or float(row['ERA']) <= 0.0 or
                row['WHIP'] is None or float(row['WHIP']) <= 0.0 or
                (name is None or name == '') or float(row['G']) <= 0.0):
                # or not row['POS']):
            continue

        norm_name = normalizer.name_normalizer(name)
        pos = []
        status = ""

        if 'POS' in row:
            pos = row['POS'].decode('utf-8')
        pitcher['NAME'] = name
        pitcher['NORMALIZED_FIRST_NAME'] = norm_name['First']
        pitcher['LAST_NAME'] = norm_name['Last']
        pitcher['TEAM'] = (normalizer.team_normalizer(row['Team'].decode('utf-8'))
                           if row['Team'] else "FA")
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
