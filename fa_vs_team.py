"""Interface with program here"""
import html_parser
import player_rater
import player_creator

# https://developer.yahoo.com/fantasysports/guide/players-collection.html

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

print "Avail Pitching FAs"
player_rater.rate_fa(PITCHER_FA_LIST, ROS_PROJ_P_LIST)
print "\nTeam Pitching Values"
player_rater.rate_team(html_parser.get_single_yahoo_team(LEAGUE_NO, "MachadoAboutNothing"),
                       ROS_PROJ_P_LIST)
print "\nAvail Batting FAs"
player_rater.rate_fa(BATTER_FA_LIST, ROS_PROJ_B_LIST)
print "\nTeam Batting Values"
player_rater.rate_team(html_parser.get_single_yahoo_team(LEAGUE_NO, "MachadoAboutNothing"),
                       ROS_PROJ_B_LIST)

def fa_vs_team():
    """Compare team player values with available FA player values\n
    Args:\n
        None.\n
    Returns:\n
        string with player data for diplay in html.\n
    Raises:\n
        None.
    """
    avail_pitching_fas = player_rater.rate_fa(PITCHER_FA_LIST, ROS_PROJ_P_LIST)
    team_pitching_values = player_rater.rate_team(html_parser.get_single_yahoo_team(LEAGUE_NO, "MachadoAboutNothing"),
                       ROS_PROJ_P_LIST)
    avail_batting_fas = player_rater.rate_fa(BATTER_FA_LIST, ROS_PROJ_B_LIST)
    team_batting_values = player_rater.rate_team(html_parser.get_single_yahoo_team(LEAGUE_NO, "MachadoAboutNothing"),
                        ROS_PROJ_B_LIST)
    player_comp = "Avail Pitching FAs\n"
    player_comp += avail_pitching_fas
    player_comp += "\nTeam Pitching Values\n"
    player_comp += team_pitching_values
    player_comp += "\nAvail Batting FAs\n"
    player_comp += avail_batting_fas
    player_comp += "\nTeam Batting Values"
    player_comp += team_batting_values

    return player_comp

