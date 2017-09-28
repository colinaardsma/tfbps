import json
import datetime
import api_connector

def get_guid(access_token):
    url = "https://social.yahooapis.com/v1/me/guid"
    raw_json = api_connector.get_json_data(url, access_token)
    return raw_json

def get_prev_year_league(current_league_dict):
    fantasy_content = current_league_dict['fantasy_content']
    if 'users' in fantasy_content:
        fantasy_content = fantasy_content['users']['0']['user'][1]['games']['0']['game'][1]
    prev_year_id = fantasy_content['leagues']['0']['league'][0]['renew']
    prev_year_id = prev_year_id.replace("_", ".l.")
    # print prev_year_id
    return prev_year_id 

def get_league_query(league_key, access_token, endpoint):
    query_path = "/leagues;league_keys=" + league_key + endpoint
    league_base_json = api_connector.yql_query(query_path, access_token)
    league_base_dict = json.loads(league_base_json)
    return league_base_dict

def get_league_settings(league_key, access_token):
    return get_league_query(league_key, access_token, "/settings")

def get_league_standings(league_key, access_token):
    query_dict = get_league_query(league_key, access_token, "/standings")
    standings_dict = query_dict['fantasy_content']['leagues']['0']['league']
    return format_league_standings_dict(standings_dict)

def get_league_transactions(league_key, access_token):
    return get_league_query(league_key, access_token, "/transactions")

def get_leagues(user, user_id):
    api_connector.check_token_expiration(user, user_id, "/get_leagues")
    current_year_query_path = "/users;use_login=1/games;game_keys=mlb/leagues"
    # current_year_query_path = "/users;use_login=1/games;game_keys=238/leagues"
    current_year_query_json = api_connector.yql_query(current_year_query_path,
                                                      user.access_token)
    current_year_dict = json.loads(current_year_query_json)
    # print current_year_dict
    current_year_league_list = []
    current_year_league_base = current_year_dict['fantasy_content']['users']['0']['user'][1]['games']['0']['game'][1]['leagues']
    current_year_league_count = current_year_league_base['count']
    for i in range(current_year_league_count):
        league_dict = current_year_league_base['{}'.format(i)]['league'][0]
        current_year_league_list.append(league_dict)
    league_history_list = []
    for current_year_league in current_year_league_list:
        current_year_league_dict = {}
        current_year_league_key = current_year_league['league_key']
        current_year_league_dict['league_key'] = current_year_league_key
        current_year_league_dict['name'] = current_year_league['name']
        current_year_league_dict['season'] = current_year_league['season']
        if current_year_league['renew'] == '':
            current_year_league_dict['prev_year'] = None
            league_history_list.append(current_year_league_dict)
            continue
        current_year_league_dict['prev_year'] = current_year_league['renew'].replace("_", ".l.")
        league_history_list.append(current_year_league_dict)

        one_year_prior_league_dict = {}
        one_year_prior_league_key = current_year_league_dict['prev_year']
        one_year_prior_dict_base = get_league_query(one_year_prior_league_key, user.access_token, "")
        one_year_prior_dict = one_year_prior_dict_base['fantasy_content']['leagues']['0']['league'][0]
        one_year_prior_league_dict['league_key'] = one_year_prior_league_key
        one_year_prior_league_dict['season'] = one_year_prior_dict['season']        
        one_year_prior_league_dict['name'] = one_year_prior_dict['name']
        if one_year_prior_dict['renew'] == '':
            one_year_prior_league_dict['prev_year'] = None
            league_history_list.append(one_year_prior_league_dict)
            continue
        one_year_prior_league_dict['prev_year'] = one_year_prior_dict['renew'].replace("_", ".l.")
        league_history_list.append(one_year_prior_league_dict)

        two_years_prior_league_dict = {}
        two_years_prior_league_key = one_year_prior_league_dict['prev_year']
        two_years_prior_dict_base = get_league_query(two_years_prior_league_key, user.access_token, "")
        two_years_prior_dict = two_years_prior_dict_base['fantasy_content']['leagues']['0']['league'][0]
        two_years_prior_league_dict['league_key'] = two_years_prior_league_key
        two_years_prior_league_dict['season'] = two_years_prior_dict['season']        
        two_years_prior_league_dict['name'] = two_years_prior_dict['name']
        if two_years_prior_dict['renew'] == '':
            two_years_prior_league_dict['prev_year'] = None
            league_history_list.append(two_years_prior_league_dict)
            continue
        two_years_prior_league_dict['prev_year'] = two_years_prior_dict['renew'].replace("_", ".l.")
        league_history_list.append(two_years_prior_league_dict)
    return league_history_list

def get_current_leagues(league_list):
    season = datetime.datetime.now().year
    current_leagues = []
    while len(current_leagues) < 1:
        current_leagues = [l for l in league_list if l['season'] == str(season)]
        season -= 1
    return current_leagues

def format_league_standings_dict(league_standings_base_dict):
    # team_count = league_standings_base_dict[0]['num_teams']
    team_count = league_standings_base_dict[1]['standings'][0]['teams']['count']
    standings = league_standings_base_dict[1]['standings'][0]['teams']

    formatted_standings = []
    for i in range(team_count):
        team_standing_dict = standings['{}'.format(i)]['team']
        team_info_dict = team_standing_dict[0]

        standing = {}
        standing['PointsTeam'] = [x['name'] for x in team_info_dict if 'name' in x][0]
        standing['StatsTeam'] = standing['PointsTeam']

        team_stats_dict = team_standing_dict[1]['team_stats']['stats']
        for stat in team_stats_dict:
            stat_name = STAT_ID_DICT['{}'.format(stat['stat']['stat_id'])]
            standing['Stats{}'.format(stat_name)] = float(stat['stat']['value']) if stat['stat']['value'] != "" else stat['stat']['value']

        team_points_dict = team_standing_dict[1]['team_points']['stats']
        for point in team_points_dict:
            stat_name = STAT_ID_DICT['{}'.format(point['stat']['stat_id'])]
            standing['Points{}'.format(stat_name)] = float(point['stat']['value']) if point['stat']['value'] != "" else point['stat']['value']

        standing['PointsRank'] = int(team_standing_dict[2]['team_standings']['rank'])
        standing['StatsRank'] = standing['PointsRank']

        formatted_standings.append(standing)
    return formatted_standings

STAT_ID_DICT = {'1': 'TotalGP',
                '60': '',
                '7': 'R',
                '12': 'HR',
                '13': 'RBI',
                '16': 'SB',
                '55': 'OPS',
                '50': 'IP',
                '28': 'W',
                '32': 'SV',
                '42': 'K',
                '26': 'ERA',
                '27': 'WHIP'}
