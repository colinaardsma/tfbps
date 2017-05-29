"""Rate players"""
import html_parser
import operator

def rate_fa(fa_list, ros_projection_list):
    """Compare available FAs with Projections\n
    Args:\n
        fa_list: list of available FA on Yahoo!.\n
        ros_projection_list: Rest of Season projection list.\n
    Returns:\n
        None.\n
    Raises:\n
        None.
    """
    fa_player_list = []
    for player in ros_projection_list:
        if any(fa['NAME'].lower().replace('.', '') ==
               player.name.lower().replace('.', '') for fa in fa_list):
            player.isFA = True
            fa_player_list.append(player)
    dollar_value = 100.00
    player_number = 0
    if "P" in ros_projection_list[0].pos:
        while dollar_value > 1.0:
            print ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^20}" +
                   " - {player.wins:^3} - {player.svs:^2} - {player.sos:^3} - {player.era:^4}" +
                   " - {player.whip:^4}").format(player=fa_player_list[player_number])
            dollar_value = fa_player_list[player_number].dollarValue
            player_number += 1
    else:
        while dollar_value > 1.0:
            print ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^20}" +
                   " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3} - {player.sbs:^2}" +
                   " - {player.ops:^5}").format(player=fa_player_list[player_number])
            dollar_value = fa_player_list[player_number].dollarValue
            player_number += 1

def rate_team(team_dict, ros_projection_list):
    """Compare team with Projections\n
    Args:\n
        team_dict: dict of players on team.\n
        ros_projection_list: Rest of Season projection list.\n
    Returns:\n
        None.\n
    Raises:\n
        None.
    """
    team_roster_list = [roster.lower().replace('.', '') for roster in team_dict['ROSTER']]
    team_player_list = []
    for player in ros_projection_list:
        if player.name.lower().replace('.', '') in team_roster_list:
            team_player_list.append(player)
    for player in team_player_list:
        if "P" in ros_projection_list[0].pos:
            print ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^20}" +
                   " - {player.wins:^3} - {player.svs:^2} - {player.sos:^3} - {player.era:^4}" +
                   " - {player.whip:^4}").format(player=player)
        else:
            print ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^20}" +
                   " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3} - {player.sbs:^2}" +
                   " - {player.ops:^5}").format(player=player)

# def full_season_standings_projection(team_dict, current_stangings, ros_projection_list):
#     """Full Season Standings Projection"""

#     roster_optimizer(team_dict)

def roster_optimizer(team_dict, ros_projection_list, league_pos_dict):
    """Optimizes Roster for remainder of year\n
    Args:\n
        team_dict: dict of players on team.\n
        ros_projection_list: Rest of Season projection list.\n
    Returns:\n
        None.\n
    Raises:\n
        None.
    """
    team_roster_list = [roster.lower().replace('.', '') for roster in team_dict['ROSTER']]
    team_player_list = []
    for player in ros_projection_list:
        if player.name.lower().replace('.', '') in team_roster_list:
            team_player_list.append(player)
    sorted(team_player_list, key=operator.attrgetter('dollarValue'))
    # league_roster_pos = league_settings["Roster Positions:"]
    # league_pos_dict = html_parser.split_league_pos_types(league_roster_pos)
    starting_batters = {}
    batting_pos = order_batting_pos_by_scarcity(league_pos_dict['Batting POS'])
    multi_pos = False
    for pos in batting_pos:
        for player in team_player_list:
            if pos == "C" and "CF" in player.pos:
                continue
            if pos in player.pos or (pos == "OF" and ("RF" in player.pos
                                                      or "LF" in player.pos
                                                      or "CF" in player.pos)):
                if multi_pos is True or batting_pos.count(pos) > 1:
                    multi_pos = True
                    if pos in starting_batters:
                        starting_batters[pos].append(player)
                    while pos not in starting_batters or len(starting_batters[pos]) < batting_pos.count(pos):
                        starting_batters[pos] = [player]
                        team_player_list.remove(player)
                else:
                    starting_batters[pos] = player
                    team_player_list.remove(player)
        multi_pos = False
            # iterate through batting_pos and team_player_list to insert highest rated player for each pos


    return starting_batters
    # for player in team_player_list:
        
    # starting_c = {}

def order_batting_pos_by_scarcity(league_batting_roster_pos):
    """Order league specific roster batting positions based on position scarcity\n
    Args:\n
        league_roster_pos: Yahoo! league roster batting positions.\n
    Returns:\n
        ordered list of league roster positions based on scarcity.\n
    Raises:\n
        None.
    """
    scarcity_order = ["C", "SS", "2B", "MI", "3B", "1B", "CI",
                      "IF", "CF", "LF", "RF", "OF", "Util"]
    ordered_roster_pos_list = []
    for pos in scarcity_order:
        while pos in league_batting_roster_pos:
            ordered_roster_pos_list.append(pos)
            league_batting_roster_pos.remove(pos)
    return ordered_roster_pos_list


# LEAGUE_BATTING_ROSTER_POS = ["C", "Util", "OF", "2B", "OF", "3B", "OF", "OF",
#                              "Util", "OF", "SS"]

# LEAGUE_ROSTER_POS = html_parser.get_league_settings(5901)["Roster Positions:"]
# ROSTER_POS_BY_TYPE = html_parser.split_league_pos_types(LEAGUE_ROSTER_POS)
# LEAGUE_BENCH_POS = ROSTER_POS_BY_TYPE["Bench POS"]
# LEAGUE_BATTING_ROSTER_POS = ROSTER_POS_BY_TYPE["Batting POS"]
# LEAGUE_PITCHING_ROSTER_POS = ROSTER_POS_BY_TYPE["Pitching POS"]

# print order_batting_pos_by_scarcity(LEAGUE_BATTING_ROSTER_POS)
