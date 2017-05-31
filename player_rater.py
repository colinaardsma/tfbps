"""Rate players"""
import operator
import math
import html_parser
import player_models

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

def batting_roster_optimizer(team_dict, ros_projection_list, league_pos_dict):
    """Optimizes Batting Roster for remainder of year\n
    Args:\n
        team_dict: dict of players on team.\n
        ros_projection_list: Rest of Season projection list.\n
    Returns:\n
        dict of recommended starting batters.\n
    Raises:\n
        None.
    """
    team_roster_list = [roster.lower().replace('.', '') for roster in team_dict['ROSTER']]
    team_player_list = []
    for player in ros_projection_list:
        if player.name.lower().replace('.', '') in team_roster_list:
            team_player_list.append(player)
    sorted(team_player_list, key=operator.attrgetter('dollarValue'))
    starting_batters = {}
    batting_pos_scarc = order_batting_pos_by_scarcity(league_pos_dict['Batting POS'])
    batting_pos_scarc_elig = []
    pos_elig_dict = {}
    for pos in batting_pos_scarc:
        for player in team_player_list:
            if pos == "C" and "CF" in player.pos:
                continue
            elif pos in player.pos or (pos == "OF" and ("RF" in player.pos
                                                        or "LF" in player.pos
                                                        or "CF" in player.pos)):
                if pos not in pos_elig_dict:
                    pos_elig_dict[pos] = 1
                else:
                    pos_elig_dict[pos] += 1
            elif pos == "Util":
                pos_elig_dict[pos] = len(team_player_list)
    for pos in batting_pos_scarc:
        if pos_elig_dict[pos] == 1:
            batting_pos_scarc_elig.append(pos)
    for pos in batting_pos_scarc:
        if pos_elig_dict[pos] != 1:
            batting_pos_scarc_elig.append(pos)
    for pos in batting_pos_scarc_elig:
        i = 0
        multi_pos = False
        while i < len(team_player_list):
            player = team_player_list[i]
            if pos == "C" and "CF" in player.pos:
                i += 1
            elif pos in player.pos or pos == "Util" or (pos == "OF" and ("RF" in player.pos
                                                                         or "LF" in player.pos
                                                                         or "CF" in player.pos)):
                if multi_pos is True or batting_pos_scarc_elig.count(pos) > 1:
                    multi_pos = True
                    if (pos in starting_batters and len(starting_batters[pos]) <
                            batting_pos_scarc_elig.count(pos)):
                        starting_batters[pos].append(player)
                        del team_player_list[i]
                    elif pos not in starting_batters:
                        starting_batters[pos] = [player]
                        del team_player_list[i]
                    else:
                        i += 1
                else:
                    multi_pos = False
                    if pos in starting_batters:
                        i += 1
                    else:
                        starting_batters[pos] = player
                        del team_player_list[i]
            else:
                i += 1
    return starting_batters

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


def pitching_roster_optimizer(team_dict, ros_projection_list, league_pos_dict, current_stangings,
                              league_settings):
    """Optimizes Pitching Roster for remainder of year\n
    Args:\n
        team_dict: dict of players on team.\n
        ros_projection_list: Rest of Season projection list.\n
    Returns:\n
        dict of recommended starting pitchers.\n
    Raises:\n
        None.
    """
    team_roster_list = [roster.lower().replace('.', '') for roster in team_dict['ROSTER']]
    team_player_list = []
    current_ip = 0
    max_ip = int(league_settings['Max Innings Pitched:'])
    for standing in current_stangings:
        if standing['PointsTeam'] == team_dict['TEAM_NAME']:
            current_ip += int(math.ceil(float(standing['StatsIP'])))
    for player in ros_projection_list:
        if player.name.lower().replace('.', '') in team_roster_list:
            team_player_list.append(player)
    sorted(team_player_list, key=operator.attrgetter('dollarValue'))
    starting_pitchers = {}
    pitching_pos = league_pos_dict['Pitching POS']
    for pos in pitching_pos:
        i = 0
        multi_pos = False
        if current_ip >= max_ip:
            break
        else:
            while i < len(team_player_list):
                player = team_player_list[i]
            # for player in team_player_list:
                if player.ips + current_ip > max_ip:
                    stat_pct = (max_ip - current_ip) / player.ips
                    partial_player = player_models.Pitcher(name=player.name, team=player.team,
                                                           pos=player.pos, category=player.category,
                                                           ips=player.ips * stat_pct,
                                                           wins=player.wins * stat_pct,
                                                           svs=player.svs * stat_pct,
                                                           sos=player.sos * stat_pct,
                                                           era=player.era, whip=player.whip)
                    starting_pitchers[pos] = partial_player
                    current_ip += partial_player.ips
                    del team_player_list[i]
                    #this logic isnt right, needs to be applicable to any pitching pos
                elif pos in player.pos:
                    if multi_pos is True or pitching_pos.count(pos) > 1:
                        multi_pos = True
                        if (pos in starting_pitchers and len(starting_pitchers[pos]) <
                                pitching_pos.count(pos)):
                            starting_pitchers[pos].append(player)
                            current_ip += player.ips
                            del team_player_list[i]
                        elif pos not in starting_pitchers:
                            starting_pitchers[pos] = [player]
                            current_ip += player.ips
                            del team_player_list[i]
                        else:
                            i += 1
                    else:
                        multi_pos = False
                        if pos in starting_pitchers:
                            i += 1
                        else:
                            starting_pitchers[pos] = player
                            current_ip += player.ips
                            del team_player_list[i]
                else:
                    i += 1
        starting_pitchers['Team IP'] = current_ip
        return starting_pitchers

                        
