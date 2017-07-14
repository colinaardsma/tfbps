"""Interface with program here"""
import operator
import html_parser
import player_rater
import player_creator

# https://developer.yahoo.com/fantasysports/guide/players-collection.html

# static variables
ROS_BATTER_URL = "http://www.fantasypros.com/mlb/projections/ros-hitters.php"
ROS_PITCHER_URL = "https://www.fantasypros.com/mlb/projections/ros-pitchers.php"
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

SGP_DICT = {'R SGP': 19.16666667, 'HR SGP': 11.5, 'RBI SGP': 20.83333333, 'SB SGP': 7.537037037,
            'OPS SGP': 0.005055555556, 'W SGP': 3.277777778, 'SV SGP': 10.44444444, 'K SGP': 42.5,
            'ERA SGP': -0.08444444444, 'WHIP SGP': -0.01666666667}

# dynamic variables
BATTER_LIST = player_creator.create_full_batter(ROS_BATTER_URL)
PITCHER_LIST = player_creator.create_full_pitcher(ROS_PITCHER_URL)
ROS_PROJ_B_LIST = player_creator.calc_batter_z_score(BATTER_LIST, BATTERS_OVER_ZERO_DOLLARS,
                                                     ONE_DOLLAR_BATTERS, B_DOLLAR_PER_FVAAZ,
                                                     B_PLAYER_POOL_MULT)
ROS_PROJ_P_LIST = player_creator.calc_pitcher_z_score(PITCHER_LIST, PITCHERS_OVER_ZERO_DOLLARS,
                                                      ONE_DOLLAR_PITCHERS, P_DOLLAR_PER_FVAAZ,
                                                      P_PLAYER_POOL_MULT)
# variable defined within methods
# BATTER_FA_LIST = html_parser.yahoo_fa(LEAGUE_NO, "B")
# PITCHER_FA_LIST = html_parser.yahoo_fa(LEAGUE_NO, "P")
# LEAGUE_SETTINGS = html_parser.get_league_settings(LEAGUE_NO)
# CURRENT_STANDINGS = html_parser.get_standings(LEAGUE_NO, int(LEAGUE_SETTINGS['Max Teams:']))
# TEAM_LIST = html_parser.yahoo_teams(LEAGUE_NO)
# LEAGUE_POS_DICT = html_parser.split_league_pos_types(LEAGUE_SETTINGS["Roster Positions:"])

def fa_vs_team(league_no, team_name):
    """Compare team player values with available FA player values\n
    Args:\n
        league_no: Yahoo! fantasy baseball league number.\n
        team_name: name of the team to retreive.\n
    Returns:\n
        string comparing team values against fa values.\n
    Raises:\n
        None.
    """
    player_comp = {}
    pitching_fa_list = html_parser.yahoo_fa(league_no, "P")
    batting_fa_list = html_parser.yahoo_fa(LEAGUE_NO, "B")
    avail_pitching_fas = player_rater.rate_fa(pitching_fa_list, ROS_PROJ_P_LIST)
    team_pitching_values = player_rater.rate_team(html_parser.get_single_yahoo_team(league_no,
                                                                                    team_name),
                                                  ROS_PROJ_P_LIST)
    avail_batting_fas = player_rater.rate_fa(batting_fa_list, ROS_PROJ_B_LIST)
    team_batting_values = player_rater.rate_team(html_parser.get_single_yahoo_team(league_no,
                                                                                   team_name),
                                                 ROS_PROJ_B_LIST)
    player_comp['Pitching FAs'] = avail_pitching_fas
    player_comp['Pitching Team'] = team_pitching_values
    player_comp['Batting FAs'] = avail_batting_fas
    player_comp['Batting Team'] = team_batting_values

    return player_comp

def single_player_rater(player_name):
    """Searches for and returns rating of and individual player\n
    Args:\n
        player_name: name of the player to search for.\n
    Returns:\n
        rated player object.\n
    Raises:\n
        None.
    """
    player = player_rater.single_player_rater(player_name, ROS_PROJ_B_LIST, ROS_PROJ_P_LIST)
    player_stats = ""
    if any("P" in pos for pos in player.pos):
        player_stats = ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^25}" +
                        " - {player.wins:^3} - {player.svs:^2} - {player.sos:^3}" +
                        "- {player.era:^4} - {player.whip:^4}\n").format(player=player)
    else:
        player_stats = ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^25}" +
                        " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3}" +
                        " - {player.sbs:^2} - {player.ops:^5}\n").format(player=player)

    return player_stats

def final_standing_projection(league_no):
    """Returns projection of final standings for league based on\n
    current standings and team projections\n
    Args:\n
        league_no: Yahoo! fantasy baseball league number.\n
    Returns:\n
        Final point standings.\n
    Raises:\n
        None.
    """
    league_settings = html_parser.get_league_settings(league_no)
    current_standings = html_parser.get_standings(league_no, int(league_settings['Max Teams:']))
    team_list = html_parser.yahoo_teams(league_no)
    league_post_dict = html_parser.split_league_pos_types(league_settings["Roster Positions:"])
    final_stats = player_rater.final_stats_projection(league_no, team_list, ROS_PROJ_B_LIST,
                                                      ROS_PROJ_P_LIST, league_post_dict,
                                                      current_standings, league_settings)
    volatility_standings = player_rater.league_volatility(SGP_DICT, final_stats)
    ranked_standings = player_rater.rank_list(volatility_standings)
    return ranked_standings

def batter_projections():
    projections = player_creator.calc_batter_z_score(BATTER_LIST, BATTERS_OVER_ZERO_DOLLARS,
                                                     ONE_DOLLAR_BATTERS, B_DOLLAR_PER_FVAAZ,
                                                     B_PLAYER_POOL_MULT)
    sorted_proj = sorted(projections, key=lambda x: x.dollarValue, reverse=True)
    return sorted_proj

def pitcher_projections():
    projections = player_creator.calc_pitcher_z_score(PITCHER_LIST, PITCHERS_OVER_ZERO_DOLLARS,
                                                      ONE_DOLLAR_PITCHERS, P_DOLLAR_PER_FVAAZ,
                                                      P_PLAYER_POOL_MULT)
    sorted_proj = sorted(projections, key=lambda x: x.dollarValue, reverse=True)
    return sorted_proj
