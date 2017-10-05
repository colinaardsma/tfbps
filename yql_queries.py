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
    api_connector.check_token_expiration(user, user_id, redirect)
    query_path = "/leagues;league_keys=" + league_key + endpoint
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
    api_connector.check_token_expiration(user, user_id, redirect)
    query_path = "/users;use_login=1/games;game_keys=mlb" + endpoint
    # query_path = "/users;use_login=1/games;game_keys=238" + redirect
    user_base_json = api_connector.yql_query(query_path, user.access_token)
    user_base_dict = json.loads(user_base_json)
    return user_base_dict

def get_leagues(user, user_id, redirect):
    api_connector.check_token_expiration(user, user_id, redirect)
# get_user_query doesnt work right
    # current_year_query_path = get_user_query(user, user_id, redirect, "/leagues")
    # current_year_query_json = api_connector.yql_query(current_year_query_path,
    #                                                   user.access_token)
    # current_year_dict = json.loads(current_year_query_json)
    current_year_dict = get_user_query(user, user_id, redirect, "/leagues")
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


LEAGUE_SETTINGS = {'Draft Type:': 'Live Auction Draft',
                   'Post Draft Players:': 'Follow Waiver Rules',
                   'New Players Become Available:': 'As soon as Yahoo adds them',
                   'Max Teams:': '12',
                   'Send unjoined players email reminders:': 'Yes',
                   "Can't Cut List Provider:": 'Yahoo Sports',
                   'Auto-renew Enabled:': 'Yes',
                   'Max Trades for Entire Season': 'No maximum',
                   'Cash League Settings:': 'Not a cash league',
                   'Trade Reject Time:': '2',
                   'Keeper Settings:': 'Yes, enable Keeper League Management tools',
                   'League Name:': 'Grays Sports Almanac',
                   'Roster Changes:': 'Daily - Today',
                   'Keeper Deadline Date:': 'Sun Mar 26 12:00am PDT',
                   'Batters Stat Categories:': 'Runs (R), Home Runs (HR), Runs Batted In (RBI), Stolen Bases (SB), On-base + Slugging Percentage (OPS)',
                   'Invite Permissions:': 'Commissioner Only',
                   'Roster Positions:': 'C, 1B, 2B, 3B, SS, OF, OF, OF, OF, Util, Util, SP, SP, RP, RP, P, P, P, P, BN, BN, BN, BN, BN, BN, DL, DL, NA, NA',
                   'Draft Time:': 'Sat Apr 1 9:00am PDT',
                   'Trade Review:': 'Commissioner',
                   'Max Games Played:': '162',
                   'Trade End Date:': 'August 13, 2017',
                   'Max Innings Pitched:': '1500',
                   'Scoring Type:': 'Rotisserie',
                   'Max Acquisitions for Entire Season:': 'No maximum',
                   'Allow Draft Pick Trades:': 'No',
                   'Waiver Mode:': 'Standard',
                   'Allow injured players from waivers or free agents to be added directly to IR:': 'No',
                   'League ID#:': '5091', 'Waiver Type:': 'FAAB w/ Continual rolling list tiebreak',
                   'Waiver Time:': '2 days',
                   'Pitchers Stat Categories:': 'Wins (W), Saves (SV), Strikeouts (K), Earned Run Average (ERA), (Walks + Hits)/ Innings Pitched (WHIP)',
                   'Custom League URL:': 'https://baseball.fantasysports.yahoo.com/league/grayssportsalmanac',
                   'Player Universe:': 'All baseball',
                   'Make League Publicly Viewable:': 'Yes',
                   'Start Scoring on:': 'Sunday, Apr 2'}



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

def get_team_query(league_key, user, user_id, redirect, endpoint):
    endpoint = "/teams" + endpoint
    team_base_dict = get_league_query(league_key, user, user_id, redirect, endpoint)
    return team_base_dict

def get_all_team_rosters(league_key, user, user_id, redirect):
    query_dict = get_team_query(league_key, user, user_id, redirect, "/roster")
    rosters_dict = query_dict['fantasy_content']['leagues']['0']['league']
    return format_team_rosters_dict(rosters_dict)

def get_single_team_roster(league_key, user, user_id, redirect):
    query_dict = get_user_query(user, user_id, redirect, "/teams/roster")
    rosters_dict = query_dict['fantasy_content']['leagues']['0']['league']
    return format_team_rosters_dict(rosters_dict)

def format_team_rosters_dict(team_rosters_base_dict):
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
    api_connector.check_token_expiration(user, user_id, redirect)
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
