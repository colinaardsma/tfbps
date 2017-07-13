"""Rate players"""
import operator
import math
import re
import copy

def rate_fa(fa_list, ros_projection_list):
    """Compare available FAs with Projections\n
    Args:\n
        fa_list: list of available FA on Yahoo!.\n
        ros_projection_list: Rest of Season projection list.\n
    Returns:\n
        list of players using FA projections.\n
    Raises:\n
        None.
    """
    fa_player_list = []
    for player in ros_projection_list:
        if any(fa['NAME'].lower() ==
               player.name.lower() for fa in fa_list):
            player.isFA = True
            fa_player_list.append(player)
    fa_above_repl = []
    dollar_value = 100.00
    player_number = 0
    # team = ""
    # if ("SP" in ros_projection_list[0].pos or "RP" in ros_projection_list[0].pos or
    #         "P" in ros_projection_list[0].pos):
    while dollar_value > 1.0:
    #         team += ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^25}" +
    #                  " - {player.wins:^3} - {player.svs:^2} - {player.sos:^3} - {player.era:^4}" +
    #                  " - {player.whip:^4}\n").format(player=fa_player_list[player_number])
        fa_above_repl.append(fa_player_list[player_number])
        dollar_value = fa_player_list[player_number].dollarValue
        player_number += 1
    # else:
    #     while dollar_value > 1.0:
    #         team += ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^25}" +
    #                  " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3} - {player.sbs:^2}" +
    #                  " - {player.ops:^5}\n").format(player=fa_player_list[player_number])
    #         dollar_value = fa_player_list[player_number].dollarValue
    #         player_number += 1
    return fa_above_repl

def rate_team(team_dict, ros_projection_list):
    """Compare team with Projections\n
    Args:\n
        team_dict: dict of players on team.\n
        ros_projection_list: Rest of Season projection list.\n
    Returns:\n
        list of players using team projections.\n
    Raises:\n
        None.
    """
    team_roster_list = [roster.lower() for roster in team_dict['ROSTER']]
    team_player_list = []
    for player in ros_projection_list:
        if player.name.lower() in team_roster_list:
            team_player_list.append(player)
    return team_player_list

def team_optimizer(team_dict, ros_proj_b_list, ros_proj_p_list, league_pos_dict,
                   current_stangings, league_settings):
    opt_batters = batting_roster_optimizer(team_dict, ros_proj_b_list, league_pos_dict)
    opt_pitchers = pitching_roster_optimizer(team_dict, ros_proj_p_list, league_pos_dict,
                                             current_stangings, league_settings)
    opt_bench = bench_roster_optimizer(team_dict, ros_proj_b_list, ros_proj_p_list,
                                       league_pos_dict, current_stangings, league_settings,
                                       opt_batters, opt_pitchers)
    team_stats = {}
    for standing in current_stangings:
        if standing['PointsTeam'] == team_dict['TEAM_NAME']:
            batters = [val for sublist in opt_batters.values() for val in sublist]
            batters.extend(opt_bench['batters'])
            team_stats['StatsR'] = int(standing['StatsR'])
            team_stats['StatsHR'] = int(standing['StatsHR'])
            team_stats['StatsRBI'] = int(standing['StatsRBI'])
            team_stats['StatsSB'] = int(standing['StatsSB'])
            team_stats['StatsOPS'] = float(standing['StatsOPS'])
            team_stats['StatsTotalGP'] = int(standing['StatsTotalGP'])
            for batter in batters:
                team_stats['StatsR'] += int(batter.runs)
                team_stats['StatsHR'] += int(batter.hrs)
                team_stats['StatsRBI'] += int(batter.rbis)
                team_stats['StatsSB'] += int(batter.sbs)
                # calc ab and gp for use in ops weighting
                avg_ab_per_team = 34.1 # per game
                avg_ab_per_player = avg_ab_per_team / 9
                batter_est_gp = batter.atbats / avg_ab_per_player
                team_abs = int(team_stats['StatsTotalGP']) * avg_ab_per_player
                total_abs = team_abs + batter.atbats
                # calc ops
                current_weighted_ops = float(team_stats['StatsOPS']) * team_abs
                batter_weighted_ops = batter.ops * batter.atbats
                team_stats['StatsOPS'] = (current_weighted_ops + batter_weighted_ops) / total_abs
                team_stats['StatsTotalGP'] += batter_est_gp
            pitchers = [val for sublist in opt_pitchers.values() for val in sublist]
            pitchers.extend(opt_bench['pitchers'])
            team_stats['StatsW'] = int(standing['StatsW'])
            team_stats['StatsSV'] = int(standing['StatsSV'])
            team_stats['StatsK'] = int(standing['StatsK'])
            team_stats['StatsERA'] = float(standing['StatsERA'])
            team_stats['StatsWHIP'] = float(standing['StatsWHIP'])
            team_stats['StatsIP'] = float(standing['StatsIP'])
            for pitcher in pitchers:
                team_stats['StatsW'] += int(pitcher.wins)
                team_stats['StatsSV'] += int(pitcher.svs)
                team_stats['StatsK'] += int(pitcher.sos)
                # calc ip
                ip_add = team_stats['StatsIP'] + pitcher.ips
                current_ip = ip_add if (1 - ip_add % 1) < .3 else math.ceil(ip_add)
                # calc era and whip
                weighted_team_era = float(team_stats['StatsERA']) * float(team_stats['StatsIP'])
                weighted_pitcher_era = pitcher.era * pitcher.ips
                team_stats['StatsERA'] = (weighted_team_era + weighted_pitcher_era) / current_ip
                weighted_team_whip = float(team_stats['StatsWHIP']) * float(team_stats['StatsIP'])
                weighted_pitcher_whip = pitcher.whip * pitcher.ips
                team_stats['StatsWHIP'] = (weighted_team_whip + weighted_pitcher_whip) / current_ip
                team_stats['StatsIP'] = current_ip
            team_stats['TEAM_NAME'] = standing['PointsTeam']
    return team_stats

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
    for player in team_player_list:
        if any("P" in pos for pos in player.pos):
            if current_ip < max_ip:
                if player.ips + current_ip > max_ip:
                    player = partial_pitcher(player, max_ip, current_ip)
                bench_players['pitchers'].append(player)
                current_ip += player.ips
                bench_ip += player.ips
                if (sum(map(len, bench_players.values()))) == len(bench_pos):
                    break
        else:
            bench_players['batters'].append(bench_batter(player))
            if (sum(map(len, bench_players.values()))) == len(bench_pos):
                break
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
    pitcher = copy.deepcopy(player)
    stat_pct = (float(max_ip) - current_ip) / pitcher.ips
    pitcher.ips *= stat_pct
    pitcher.wins *= stat_pct
    pitcher.svs *= stat_pct
    pitcher.sos *= stat_pct
    return pitcher

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
    batter = copy.deepcopy(player)
    batter.atbats *= stat_pct
    batter.runs *= stat_pct
    batter.hrs *= stat_pct
    batter.rbis *= stat_pct
    batter.sbs *= stat_pct
    return batter

def single_player_rater(player_name, ros_batter_projection_list, ros_pitcher_projection_list):
    """Searches for and returns rating of and individual player\n
    Args:\n
        player_name: name of the player to search for.\n
        ros_batter_projection_list: Rest of Season batter projection list.\n
        ros_pitcher_projection_list: Rest of Season pitcher projection list.\n
    Returns:\n
        rated player object.\n
    Raises:\n
        None.
    """
    player = None
    for player_proj in ros_pitcher_projection_list:
        if player_name.lower() == player_proj.name.lower():
            player = player_proj
    for player_proj in ros_batter_projection_list:
        if player_name.lower() == player_proj.name.lower():
            player = player_proj
    return player

def final_stats_projection(league_no, team_list, ros_proj_b_list, ros_proj_p_list,
                               league_pos_dict, current_stangings, league_settings):
    final_standings = []
    for team in team_list:
        post_dict_copy = copy.deepcopy(league_pos_dict)
        optimized_team = team_optimizer(team, ros_proj_b_list, ros_proj_p_list,
                                        post_dict_copy, current_stangings, league_settings)
        final_standings.append(optimized_team)
    return final_standings

def rank_list(projected_final_stats_list):
    stat_ranker(projected_final_stats_list, "R")
    stat_ranker(projected_final_stats_list, "HR")
    stat_ranker(projected_final_stats_list, "RBI")
    stat_ranker(projected_final_stats_list, "SB")
    stat_ranker(projected_final_stats_list, "OPS")
    stat_ranker(projected_final_stats_list, "W")
    stat_ranker(projected_final_stats_list, "SV")
    stat_ranker(projected_final_stats_list, "K")
    stat_ranker(projected_final_stats_list, "ERA", False)
    stat_ranker(projected_final_stats_list, "WHIP", False)
    for team in projected_final_stats_list:
        team['PointsTotal'] = sum([value for key, value in team.items() if 'Points' in key])
    projected_final_stats_list.sort(key=operator.itemgetter('PointsTotal'), reverse=True)
    return projected_final_stats_list

def stat_ranker(projected_final_stats_list, stat, reverse=True):
    stats_title = "Stats" + stat
    points_title = "Points" + stat
    projected_final_stats_list.sort(key=operator.itemgetter(stats_title), reverse=reverse)
    points = 12
    for team in projected_final_stats_list:
        team[points_title] = points
        points -= 1

def league_volatility(sgp_dict, final_stats):
    calc_volatility(sgp_dict, final_stats, "R")
    calc_volatility(sgp_dict, final_stats, "HR")
    calc_volatility(sgp_dict, final_stats, "RBI")
    calc_volatility(sgp_dict, final_stats, "SB")
    calc_volatility(sgp_dict, final_stats, "OPS")
    calc_volatility(sgp_dict, final_stats, "W")
    calc_volatility(sgp_dict, final_stats, "SV")
    calc_volatility(sgp_dict, final_stats, "K")
    calc_volatility(sgp_dict, final_stats, "ERA", False)
    calc_volatility(sgp_dict, final_stats, "WHIP", False)
    for team in final_stats:
        team['Total Upward Volatility'] = sum([value for key, value in team.items() if 'UpVol' in key])
        team['Total Downward Volatility'] = sum([value for key, value in team.items() if 'DownVol' in key])
    return final_stats

def calc_volatility(sgp_dict, final_stats, stat, reverse=True):
    stats_title = "Stats" + stat
    up_vol_title = "UpVol " + stat
    down_vol_title = "DownVol " + stat
    sgp_title = stat + " SGP"
    sgp = sgp_dict[sgp_title]
    final_stats.sort(key=operator.itemgetter(stats_title), reverse=reverse)
    list_length = len(final_stats) - 1

    for i in range(list_length):
        up_counter = 0
        down_counter = 0
        j = i
        k = i
        current_team_stat = final_stats[i][stats_title]
        up_team_stat = final_stats[j][stats_title]
        down_team_stat = final_stats[k][stats_title]
        while (j >= 0 and (up_team_stat - current_team_stat <= sgp)):
            j -= 1
            up_counter += 1
            if up_team_stat - current_team_stat == sgp:
                up_counter -= .5
        while (k <= list_length and (current_team_stat - down_team_stat <= sgp)):
            k += 1
            down_counter += 1
            if current_team_stat - down_team_stat == sgp:
                down_counter -= .5
        final_stats[i][up_vol_title] = up_counter
        final_stats[i][down_vol_title] = down_counter
