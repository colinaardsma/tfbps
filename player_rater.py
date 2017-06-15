"""Rate players"""
import operator
import math
import re
import collections
import itertools
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
        if any(fa['NAME'].lower() ==
               player.name.lower() for fa in fa_list):
            player.isFA = True
            fa_player_list.append(player)
    dollar_value = 100.00
    player_number = 0
    team = ""
    if ("SP" in ros_projection_list[0].pos or "RP" in ros_projection_list[0].pos or
            "P" in ros_projection_list[0].pos):
        while dollar_value > 1.0:
            team += ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^25}" +
                     " - {player.wins:^3} - {player.svs:^2} - {player.sos:^3} - {player.era:^4}" +
                     " - {player.whip:^4}\n").format(player=fa_player_list[player_number])
            dollar_value = fa_player_list[player_number].dollarValue
            player_number += 1
    else:
        while dollar_value > 1.0:
            team += ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^25}" +
                     " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3} - {player.sbs:^2}" +
                     " - {player.ops:^5}\n").format(player=fa_player_list[player_number])
            dollar_value = fa_player_list[player_number].dollarValue
            player_number += 1
    return team

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
    team_roster_list = [roster.lower() for roster in team_dict['ROSTER']]
    team_player_list = []
    for player in ros_projection_list:
        if player.name.lower() in team_roster_list:
            team_player_list.append(player)
    team = ""
    for player in team_player_list:
        if ("SP" in ros_projection_list[0].pos or "RP" in ros_projection_list[0].pos or
                "P" in ros_projection_list[0].pos):
            team += ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^25}" +
                     " - {player.wins:^3} - {player.svs:^2} - {player.sos:^3} - {player.era:^4}" +
                     " - {player.whip:^4}\n").format(player=player)
        else:
            team += ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^25}" +
                     " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3} - {player.sbs:^2}" +
                     " - {player.ops:^5}\n").format(player=player)
    return team

# def rater_string_creator(player):
#     if player 
#     pitcher_field_list = [player.dollarValue, name]


# def full_season_standings_projection(team_dict, current_stangings, ros_projection_list):
#     """Full Season Standings Projection"""

#     roster_optimizer(team_dict)

def batting_roster_optimizer(team_dict, ros_projection_list, league_pos_dict):
    """Optimizes Batting Roster for remainder of year\n
    Args:\n
        team_dict: dict of players on team.\n
        ros_projection_list: Rest of Season projection list.\n
        league_pos_dict: dict of team positions.\n
    Returns:\n
        dict of recommended starting batters.\n
    Raises:\n
        None.
    """
    team_roster_list = [roster.lower() for roster in team_dict['ROSTER']]
    team_player_list = []
    for player in ros_projection_list:
        if player.name.lower() in team_roster_list:
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
                        starting_batters[pos] = [player]
                        del team_player_list[i]
            else:
                i += 1
    return starting_batters

def order_batting_pos_by_scarcity(league_batting_roster_pos):
    """Order league specific roster batting positions based on position scarcity\n
    Args:\n
        league_batting_roster_pos: Yahoo! league roster batting positions.\n
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
        league_pos_dict: dict of team positions.\n
        current_stangings: current league standings.\n
        league_settings: league settings.\n
    Returns:\n
        dict of recommended starting pitchers.\n
    Raises:\n
        None.
    """
    team_roster_list = [roster.lower() for roster in team_dict['ROSTER']]
    team_player_list = []
    current_ip = 0
    starter_ip = 0
    max_ip = int(league_settings['Max Innings Pitched:'])
    for standing in current_stangings:
        if standing['PointsTeam'] == team_dict['TEAM_NAME']:
            current_ip += int(math.ceil(float(standing['StatsIP'])))
    for player in ros_projection_list:
        if player.name.lower() in team_roster_list:
            team_player_list.append(player)
    sorted(team_player_list, key=operator.attrgetter('dollarValue'))
    starting_pitchers = {}
    pitching_pos = league_pos_dict['Pitching POS']
    for pos in pitching_pos:
        i = 0
        regex_pos = re.compile(pos)
        multi_pos = False
        if current_ip >= max_ip:
            break
        else:
            while i < len(team_player_list):
                player = team_player_list[i]
                if player.ips + current_ip > max_ip:
                    player = partial_pitcher(player, max_ip, current_ip)
                if filter(regex_pos.match, player.pos) or pos == "P":
                    if (pos == "SP" and not player.is_sp) or (pos == "RP" and player.is_sp):
                        i += 1
                        continue
                    elif multi_pos is True or pitching_pos.count(pos) > 1:
                        multi_pos = True
                        if (filter(regex_pos.match, starting_pitchers.keys()) and
                                len(starting_pitchers[pos]) < pitching_pos.count(pos)):
                            starting_pitchers[pos].append(player)
                            current_ip += player.ips
                            starter_ip += player.ips
                            del team_player_list[i]
                        elif not filter(regex_pos.match, starting_pitchers.keys()):
                            starting_pitchers[pos] = [player]
                            current_ip += player.ips
                            starter_ip += player.ips
                            del team_player_list[i]
                        else:
                            i += 1
                    else:
                        multi_pos = False
                        if filter(regex_pos.match, starting_pitchers.keys()):
                            i += 1
                        else:
                            starting_pitchers[pos] = [player]
                            current_ip += player.ips
                            starter_ip += player.ips
                            del team_player_list[i]
                else:
                    i += 1
    starting_pitchers['Starter IP'] = starter_ip
    return starting_pitchers

def bench_roster_optimizer(team_dict, ros_batter_projection_list, ros_pitcher_projection_list,
                           league_pos_dict, current_stangings, league_settings, optimized_batters,
                           optimized_pitchers):
    """Optimizes Bench Roster for remainder of year\n
    Args:\n
        team_dict: dict of players on team.\n
        ros_batter_projection_list: Rest of Season batter projection list.\n
        ros_pitcher_projection_list: Rest of Season pitcher projection list.\n
        league_pos_dict: dict of team positions.\n
        current_stangings: current league standings.\n
        league_settings: league settings.\n
        optimized_batters: optimized batters from batter_roster_optimizer.\n
        optimized_pitchers: optimized batters from pitcher_roster_optimizer.\n
    Returns:\n
        dict of recommended bench players.\n
    Raises:\n
        None.
    """
    bench_pos = league_pos_dict['Bench POS']
    team_roster_list = [roster.lower() for roster in team_dict['ROSTER']]
    bench_roster_list = []
    team_player_list = []
    starter_ip = optimized_pitchers.pop('Starter IP')
    opt_batters = list(sum(optimized_batters.values(), []))
    opt_pitchers = list(sum(optimized_pitchers.values(), []))
    for player in team_roster_list:
        if (not any(batter.name.lower() == player for batter in opt_batters) and
                not any(pitcher.name.lower() == player for pitcher in opt_pitchers)):
            bench_roster_list.append(player)
    # TODO: can i iterate through the shorter list (bench_roster_list)
    for player in ros_pitcher_projection_list:
        if player.name.lower() in bench_roster_list:
            team_player_list.append(player)
    for player in ros_batter_projection_list:
        if player.name.lower() in bench_roster_list:
            team_player_list.append(player)
    bench_players = {}
    bench_players['pitchers'] = []
    bench_players['batters'] = []
    current_ip = 0
    bench_ip = 0
    max_ip = int(league_settings['Max Innings Pitched:'])
    for standing in current_stangings:
        if standing['PointsTeam'] == team_dict['TEAM_NAME']:
            current_ip += int(math.ceil(float(standing['StatsIP'])))
    current_ip += starter_ip
    # i = 0
    # while i < len(team_player_list):
    for player in team_player_list:
        # player = team_player_list[i]
        if any("P" in pos for pos in player.pos):
            if current_ip < max_ip:
                if player.ips + current_ip > max_ip:
                    player = partial_pitcher(player, max_ip, current_ip)
                bench_players['pitchers'].append(player)
                current_ip += player.ips
                bench_ip += player.ips
                # del team_player_list[i]
                # bench_list = list(itertools.chain.from_iterable(bench_players.values()))
                # if len(bench_list) == bench_pos.count:
                if (sum(map(len, bench_players.values()))) == len(bench_pos):
                    break
        else:
            bench_players['batters'].append(bench_batter(player))
            # del team_player_list[i]
            if (sum(map(len, bench_players.values()))) == len(bench_pos):
                break
    # bench_players['Bench IP'] = bench_ip
    return bench_players

def partial_pitcher(player, max_ip, current_ip):
    """Calculates percentage of pitcher values based on remaining ip\n
    Args:\n
        player: player object.\n
        max_ip: maximum ip for the league.\n
        current_ip: current ip for the team.\n
    Returns:\n
        player object with stats based on remaining ip.\n
    Raises:\n
        None.
    """
    stat_pct = (float(max_ip) - current_ip) / player.ips
    player.ips *= stat_pct
    player.wins *= stat_pct
    player.svs *= stat_pct
    player.sos *= stat_pct
    return player

def bench_batter(player):
    """Reduces the stat values of a bench batter by a percentage\n
    Args:\n
        player: player object.\n
    Returns:\n
        player object with stats based percentage.\n
    Raises:\n
        None.
    """
    stat_pct = .10
    player.atbats *= stat_pct
    player.runs *= stat_pct
    player.hrs *= stat_pct
    player.rbis *= stat_pct
    player.sbs *= stat_pct
    return player
