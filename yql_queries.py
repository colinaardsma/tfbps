import json
import datetime
import api_connector
import normalizer

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
    return prev_year_id 

def get_league_query(league_key, user, user_id, redirect, endpoint):
    updated_user = api_connector.check_token_expiration(user, user_id, redirect)
    if updated_user:
        user = updated_user
    query_path = "/leagues;league_keys=" + league_key + endpoint
    league_base_json = api_connector.yql_query(query_path, user.access_token)
    league_base_dict = json.loads(league_base_json)
    return league_base_dict

def get_player_query(player_keys, user, user_id, redirect, endpoint):
    updated_user = api_connector.check_token_expiration(user, user_id, redirect)
    if updated_user:
        user = updated_user
    player_key_string = ",".join(player_keys)
    query_path = "/players;player_keys=" + player_key_string + endpoint
    league_base_json = api_connector.yql_query(query_path, user.access_token)
    league_base_dict = json.loads(league_base_json)
    return league_base_dict

def get_league_settings(league_key, user, user_id, redirect):
    query_dict = get_league_query(league_key, user, user_id, redirect, "/settings")
    settings_dict = query_dict['fantasy_content']['leagues']['0']['league']
    return format_league_settings_dict(settings_dict)

def get_league_standings(league_key, user, user_id, redirect):
    query_dict = get_league_query(league_key, user, user_id, redirect, "/standings")
    standings_dict = query_dict['fantasy_content']['leagues']['0']['league']
    return format_league_standings_dict(standings_dict)

def get_league_players(league_key, user, user_id, redirect, player_type):
    # player types:
    # A (all available players)
    # FA (free agents only)
    # W (waivers only)
    # T (all taken players)
    # K (keepers only)
    endpoint = "/players;status=" + player_type
    query_dict = get_league_query(league_key, user, user_id, redirect, endpoint)
    players_dict = query_dict['fantasy_content']['leagues']['0']['league']
    return players_dict
    # return format_players_dict(players_dict)

def get_league_transactions(league_key, user, user_id, redirect):
    return get_league_query(league_key, user, user_id, redirect, "/transactions")

def get_user_query(user, user_id, redirect, endpoint):
    updated_user = api_connector.check_token_expiration(user, user_id, redirect)
    if updated_user:
        user = updated_user
    query_path = "/users;use_login=1/games;game_keys=mlb" + endpoint
    user_base_json = api_connector.yql_query(query_path, user.access_token)
    user_base_dict = json.loads(user_base_json)
    return user_base_dict

def get_leagues(user, user_id, redirect):
    updated_user = api_connector.check_token_expiration(user, user_id, redirect)
    if updated_user:
        user = updated_user
    current_year_dict = get_user_query(user, user_id, redirect, "/leagues")
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
        one_year_prior_dict_base = get_league_query(one_year_prior_league_key, user, user_id, redirect, "")
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
        two_years_prior_dict_base = get_league_query(two_years_prior_league_key, user, user_id, redirect, "")
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

def format_league_settings_dict(league_settings_base_dict):
    formatted_settings = {}
    roster_pos_base = league_settings_base_dict[1]['settings'][0]['roster_positions']
    pitching_list = []
    bench_list = []
    dl_list = []
    batting_list = []
    na_list = []
    for pos in roster_pos_base:
        pos_dict = pos['roster_position']
        if pos_dict['position'] == 'BN':
            for i in range(int(pos_dict['count'])):
                bench_list.append('BN')
        elif pos_dict['position'] == 'NA':
            for i in range(int(pos_dict['count'])):
                na_list.append('NA')
        elif pos_dict['position'] == 'DL':
            for i in range(int(pos_dict['count'])):
                dl_list.append('DL')
        elif pos_dict['position_type'] == 'B':
            for i in range(int(pos_dict['count'])):
                batting_list.append(str(pos_dict['position']))
        elif pos_dict['position_type'] == 'P':
            for i in range(int(pos_dict['count'])):
                pitching_list.append(str(pos_dict['position']))
    formatted_settings['Roster Positions'] = {}
    formatted_settings['Roster Positions']['Pitching POS'] = pitching_list
    formatted_settings['Roster Positions']['Bench POS'] = bench_list
    formatted_settings['Roster Positions']['DL POS'] = dl_list
    formatted_settings['Roster Positions']['Batting POS'] = batting_list
    formatted_settings['Roster Positions']['NA POS'] = na_list
    formatted_settings['Max Teams'] = league_settings_base_dict[0]['num_teams']
    formatted_settings['Max Innings Pitched:'] = league_settings_base_dict[1]['settings'][1]['max_innings_pitched']
    return formatted_settings

def get_team_query(league_key, user, user_id, redirect, endpoint):
    endpoint = "/teams" + endpoint
    team_base_dict = get_league_query(league_key, user, user_id, redirect, endpoint)
    return team_base_dict

def get_all_team_rosters(league_key, user, user_id, redirect):
    query_dict = get_team_query(league_key, user, user_id, redirect, "/roster")
    rosters_dict = query_dict['fantasy_content']['leagues']['0']['league']
    return format_all_team_rosters_dict(rosters_dict)

def get_single_team_roster(league_key, user, user_id, redirect):
    query_dict = get_user_query(user, user_id, redirect, "/teams/roster")
    rosters_dict = query_dict['fantasy_content']['users']['0']['user'][1]['games']['0']['game'][1]['teams']
    user_team_list = format_single_team_rosters_dict(rosters_dict)
    for team in user_team_list:
        if league_key in team['TEAM_KEY']:
            return team

# TODO: don't need 2 methods that do effectively the same thing, combine these
def format_single_team_rosters_dict(team_rosters_base_dict):
    team_count = team_rosters_base_dict['count']
    rosters = team_rosters_base_dict

    formatted_rosters = []
    for i in range(team_count):
        team_dict = {}
        team_rosters_dict = rosters['{}'.format(i)]['team']
        team_dict['TEAM_NAME'] = team_rosters_dict[0][2]['name']
        team_dict['TEAM_NUMBER'] = team_rosters_dict[0][1]['team_id']
        team_dict['TEAM_KEY'] = team_rosters_dict[0][0]['team_key']
        roster = []
        roster_count = team_rosters_dict[2]['roster']['0']['players']['count']
        for i in range(roster_count):
            player_dict = {}
            for info in team_rosters_dict[2]['roster']['0']['players']['{}'.format(i)]['player'][0]:
                if 'name' in info:
                    first_name = info['name']['ascii_first']
                    last_name = info['name']['ascii_last']
                    player_name = str(first_name) + " " + str(last_name)
                    norm_name = normalizer.name_normalizer(player_name)
                    player_dict['NAME'] = player_name
                    player_dict["NORMALIZED_FIRST_NAME"] = norm_name['First']
                    player_dict["LAST_NAME"] = norm_name['Last']
                if 'editorial_team_abbr' in info:
                    team = info['editorial_team_abbr']
                    player_dict['TEAM'] = normalizer.team_normalizer(team)
            roster.append(player_dict)
        team_dict['ROSTER'] = roster
        formatted_rosters.append(team_dict)
    return formatted_rosters

def format_all_team_rosters_dict(team_rosters_base_dict):
    team_count = team_rosters_base_dict[0]['num_teams']
    rosters = team_rosters_base_dict[1]['teams']

    formatted_rosters = []
    for i in range(team_count):
        team_dict = {}
        team_rosters_dict = rosters['{}'.format(i)]['team']
        team_dict['TEAM_NAME'] = team_rosters_dict[0][2]['name']
        team_dict['TEAM_NUMBER'] = team_rosters_dict[0][1]['team_id']
        roster = []
        roster_count = team_rosters_dict[1]['roster']['0']['players']['count']
        for i in range(roster_count):
            player_dict = {}
            for info in team_rosters_dict[1]['roster']['0']['players']['{}'.format(i)]['player'][0]:
                if 'name' in info:
                    first_name = info['name']['ascii_first']
                    last_name = info['name']['ascii_last']
                    player_name = str(first_name) + " " + str(last_name)
                    norm_name = normalizer.name_normalizer(player_name)
                    player_dict['NAME'] = player_name
                    player_dict["NORMALIZED_FIRST_NAME"] = norm_name['First']
                    player_dict["LAST_NAME"] = norm_name['Last']
                if 'editorial_team_abbr' in info:
                    team = info['editorial_team_abbr']
                    player_dict['TEAM'] = normalizer.team_normalizer(team)
            roster.append(player_dict)
        team_dict['ROSTER'] = roster
        formatted_rosters.append(team_dict)
    return formatted_rosters

def get_teams(user, user_id, redirect):
    updated_user = api_connector.check_token_expiration(user, user_id, redirect)
    if updated_user:
        user = updated_user
    teams_query_path = get_user_query(user, user_id, redirect, "/teams")
    teams_query_json = api_connector.yql_query(teams_query_path, user.access_token)
    teams_dict = json.loads(teams_query_json)
    return teams_dict

def get_fa_players(league_key, user, user_id, redirect, pOrB):
    formatted_fas = []
    count = 25
    total_players = 300
    for i in range(0, total_players, count):
        player_type = "FA;sort=AR;position=" + pOrB + ";count=" + str(count) + ";start=" + str(i)
        fa_dict = get_league_players(league_key, user, user_id, redirect, player_type)
        for i in range(count):
            player = fa_dict[1]['players']['{}'.format(i)]['player'][0]
            player_name = player[2]['name']['ascii_first'] + " " + player[2]['name']['ascii_last']
            player_dict = {}
            norm_name = normalizer.name_normalizer(player_name)
            player_dict['NAME'] = player_name
            player_dict["NORMALIZED_FIRST_NAME"] = norm_name['First']
            player_dict["LAST_NAME"] = norm_name['Last']
            team = ""
            for info in player:
                if 'editorial_team_abbr' in info:
                    team = info['editorial_team_abbr']
                    player_dict['TEAM'] = normalizer.team_normalizer(team)
            formatted_fas.append(player_dict)
    return formatted_fas

def get_auction_results(league_key, user, user_id, redirect):
    auction_results = []
    auction_query_results_dict = get_league_query(league_key, user, user_id, redirect, '/draftresults')
    auction_results_dict = auction_query_results_dict['fantasy_content']['leagues']['0']['league'][1]['draft_results']
    auction_count = auction_results_dict['count']
    all_player_keys = []
    for i in range(auction_count):
        result = auction_results_dict['{}'.format(i)]['draft_result']
        auction_result = {}
        auction_result['cost'] = result['cost']
        auction_result['player_key'] = result['player_key']
        auction_result['team_key'] = result['team_key']
        all_player_keys.append(result['player_key'])
        auction_results.append(auction_result)
    max_list_values = 25
    query_player_keys = []
    player_query_results_dict_list = []
    for i, player_key in enumerate(all_player_keys):
        if i != 0 and i % 25 == 0:
            player_query_results_dict_list.append(get_player_query(query_player_keys, user, user_id, redirect, ''))
            max_list_values = i + 25
            query_player_keys[:] = []
        if i < max_list_values:
            query_player_keys.append(player_key)
    player_query_results_dict_list.append(get_player_query(query_player_keys, user, user_id, redirect, ''))
    player_data = []
    for results_dict in player_query_results_dict_list:
        data_dict = results_dict['fantasy_content']['players']
        player_count = data_dict['count']
        for i in range(player_count):
            player = {}
            print i
            result = data_dict['{}'.format(i)]['player'][0]
            player['player_key'] = result[0]['player_key']
            player['full_name'] = result[2]['name']['full']
            player['first_name'] = result[2]['name']['ascii_first']
            player['last_name'] = result[2]['name']['ascii_last']
            player['status'] = result[3]['status_full'] if 'status_full' in result[3] else ''
            if 'editorial_team_abbr' in result[6]:
                player['team'] = result[6]['editorial_team_abbr']
            elif 'editorial_team_abbr' in result[7]:
                player['team'] = result[7]['editorial_team_abbr']
            else:
                player['team'] = 'FA'
            if 'position_type' in result[11]:
                if result[11]['position_type'] == 'B':
                    player['category'] = 'batter'
            elif 'position_type' in result[12]:
                if result[12]['position_type'] == 'B':
                    player['category'] = 'batter'
            else:
                player['category'] = 'pitcher'
            positions = []
            if 'eligible_positions' in result[12]:
                for pos in result[12]['eligible_positions']:
                    positions.append(pos['position'])
            elif 'eligible_positions' in result[13]:
                for pos in result[13]['eligible_positions']:
                    positions.append(pos['position'])
            else:
                positions.append('')
            player['pos'] = positions
            player_data.append(player)
    for i, auction_result in enumerate(auction_results):
        auction_result['first_name'] = player_data[i]['first_name']
        auction_result['last_name'] = player_data[i]['last_name']
        auction_result['status'] = player_data[i]['status']
        auction_result['pos'] = player_data[i]['pos']
    auction_results.append(auction_result)
    return auction_results

# http://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys=370.l.5091/teams/roster;date=2017-11-28
def get_current_rosters(league_key, user, user_id, redirect):
    current_rosters = []
    now = datetime.datetime.now()
    date = '{year}-{month}-{day}'.format(year=now.year, month=now.month, day=now.day)
    endpoint = '/teams/roster;date={date}'.format(date=date)
    roster_query_results_dict = get_league_query(league_key, user, user_id, redirect, endpoint)
    current_rosters_dict = roster_query_results_dict['fantasy_content']['leagues']['0']['league'][1]['teams']
    team_count = current_rosters_dict['count']
    for i in range(team_count):
        team = {}
        team_data = current_rosters_dict['{}'.format(i)]['team']
        team['team_key'] = team_data[0][0]['team_key']
        team['team_name'] = team_data[0][2]['name']
        team['waiver_priority'] = team_data[0][7]['waiver_priority']
        team['faab_balance'] = team_data[0][8]['faab_balance']
        managers = team_data[0][19]['managers']
        manager_guid_list = []
        for manager in managers:
            guid = manager['manager']['guid']
            manager_guid_list.append(guid)
        team['manager_guids'] = manager_guid_list
        roster = []
        roster_dict = team_data[1]['roster']['0']['players']
        roster_count = roster_dict['count']
        for j in range(roster_count):
            player = {}
            player_data = roster_dict['{}'.format(j)]['player'][0]
            player['player_key'] = player_data[0]['player_key']
            player['full_name'] = player_data[2]['name']['full']
            player['first_name'] = player_data[2]['name']['ascii_first']
            player['last_name'] = player_data[2]['name']['ascii_last']
            if 'status_full' in player_data[3]:
                player['status'] = player_data[3]['status_full']
            else:
                player['status'] = ''
            if 'editorial_team_abbr' in player_data[6]:
                player['team'] = player_data[6]['editorial_team_abbr']
            elif 'editorial_team_abbr' in player_data[7]:
                player['team'] = player_data[7]['editorial_team_abbr']
            else:
                player['team'] = 'FA'
            if 'position_type' in player_data[10]:
                if player_data[10]['position_type'] == 'B':
                    player['category'] = 'batter'
            elif 'position_type' in player_data[11]:
                if player_data[11]['position_type'] == 'B':
                    player['category'] = 'batter'
            elif 'position_type' in player_data[12]:
                if player_data[12]['position_type'] == 'B':
                    player['category'] = 'batter'
            else:
                player['category'] = 'pitcher'
            if 'eligible_positions' in player_data[11]:
                positions = player_data[11]['eligible_positions']
            elif 'eligible_positions' in player_data[12]:
                positions = player_data[12]['eligible_positions']
            elif 'eligible_positions' in player_data[13]:
                positions = player_data[13]['eligible_positions']
            position_list = []
            for position in positions:
                pos = position['position']
                position_list.append(pos)
            player['positions'] = position_list
            roster.append(player)
        team['roster'] = roster
        current_rosters.append(team)
    return current_rosters

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
