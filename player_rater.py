"""Rate players"""
import operator
import math
import re
import copy
import collections

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
    for player_proj in ros_projection_list:
        if any(team_comparer(player_proj.team, fa_player['TEAM']) and
               name_comparer(player_proj.name, fa_player['NAME'])
               for fa_player in fa_list):
            name = player_proj.name
            player_proj.isFA = True
            fa_player_list.append(player_proj)
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
    team_player_list = []
    for player_proj in ros_projection_list:
        if any(team_comparer(player_proj.team, roster_player['TEAM']) and
               name_comparer(player_proj.name, roster_player['NAME'])
               for roster_player in team_dict['ROSTER']):
            team_player_list.append(player_proj)
    return team_player_list

def team_optimizer(team_dict, ros_proj_b_list, ros_proj_p_list, league_pos_dict,
                   current_stangings, league_settings):
    """Optimizes full season lineups for team\n
    Args:\n
        team_dict: dict of players on team.\n
        ros_proj_b_list: Rest of Season batter projection list.\n
        ros_proj_p_list: Rest of Season pitcher projection list.\n
        league_pos_dict: dict of team positions.\n
        current_stangings: current league standings.\n
        league_settings: league settings.\n
    Returns:\n
        Optimized team lineup as a dict.\n
    Raises:\n
        None.
    """
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
    team_player_list = []
    for player_proj in ros_projection_list:
        if any(team_comparer(player_proj.team, roster_player['TEAM']) and
               name_comparer(player_proj.name, roster_player['NAME'])
               for roster_player in team_dict['ROSTER']):
            team_player_list.append(player_proj)
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
    team_player_list = []
    current_ip = 0
    starter_ip = 0
    max_ip = int(league_settings['Max Innings Pitched:'])
    for standing in current_stangings:
        if standing['PointsTeam'] == team_dict['TEAM_NAME']:
            current_ip += int(math.ceil(float(standing['StatsIP'])))
    for player_proj in ros_projection_list:
        if any(team_comparer(player_proj.team, roster_player['TEAM']) and
               name_comparer(player_proj.name, roster_player['NAME'])
               for roster_player in team_dict['ROSTER']):
            team_player_list.append(player_proj)
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
    bench_roster_list = []
    team_player_list = []
    starter_ip = optimized_pitchers.pop('Starter IP')
    opt_batters = list(sum(optimized_batters.values(), []))
    opt_pitchers = list(sum(optimized_pitchers.values(), []))
    for player in team_dict['ROSTER']:
        if (not any(team_comparer(player['TEAM'], batter.team) and
                    name_comparer(batter.name, player['NAME'])
                    for batter in opt_batters) and
                not any(team_comparer(player['TEAM'], pitcher.team) and
                        name_comparer(pitcher.name, player['NAME'])
                        for pitcher in opt_pitchers)):
            bench_roster_list.append(player)
    for player in ros_pitcher_projection_list:
        if any(team_comparer(player.team, bench_player['TEAM']) and
               name_comparer(player.name, bench_player['NAME'])
               for bench_player in bench_roster_list):
            team_player_list.append(player)
    for player in ros_batter_projection_list:
        if any(team_comparer(player.team, bench_player['TEAM']) and
               name_comparer(player.name, bench_player['NAME'])
               for bench_player in bench_roster_list):
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
        if name_comparer(player_name, player_proj.name):
            player = player_proj
    if player is None:
        for player_proj in ros_batter_projection_list:
            if name_comparer(player_name, player_proj.name):
                player = player_proj
    return player

def final_stats_projection(team_list, ros_proj_b_list, ros_proj_p_list,
                           league_pos_dict, current_stangings, league_settings):
    """Calculates final stats of the team based on an optimized lineup\n
    Args:\n
        team_list: a list of dicts of teams in the league with current rosters and stats.\n
        ros_proj_b_list: Rest of Season batter projection list.\n
        ros_proj_p_list: Rest of Season pitcher projection list.\n
        league_pos_dict: dict of team positions.\n
        current_stangings: current league standings.\n
        league_settings: league settings.\n
    Returns:\n
        list of dicts of teams with full season stat projections.\n
    Raises:\n
        None.
    """
    final_standings = []
    for team in team_list:
        post_dict_copy = copy.deepcopy(league_pos_dict)
        optimized_team = team_optimizer(team, ros_proj_b_list, ros_proj_p_list,
                                        post_dict_copy, current_stangings, league_settings)
        final_standings.append(optimized_team)
    return final_standings

def rank_list(projected_final_stats_list):
    """Ranks each stat and calculates total points in final stat projections\n
    Args:\n
        projected_final_stats_list: a list of dicts of teams with full season stat projections.\n
    Returns:\n
        list of dicts of teams with full season stat projections, ranks, and final point totals.\n
    Raises:\n
        None.
    """
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
    """Orders stats by value and calculates point value\n
    Args:\n
        projected_final_stats_list: a list of dicts of teams with full season stat projections.\n
        stat: statistic to calculate\n
        reverse: whether or not to reverse the ranking (ERA/WHIP = False, else = True)\n
    Returns:\n
        list of dicts of teams with full season stat projections and rank for secific stat.\n
    Raises:\n
        None.
    """
    stats_title = "Stats" + stat
    points_title = "Points" + stat
    projected_final_stats_list.sort(key=operator.itemgetter(stats_title), reverse=reverse)
    points = 12
    highest_shared_point = 0
    new_stat_value = 0
    old_stat_value = 0
    for team in projected_final_stats_list:
        counter = collections.Counter([s[stats_title] for s in projected_final_stats_list])
        shared_count = counter[team[stats_title]]
        if shared_count > 1:
            new_stat_value = team[stats_title]
            if new_stat_value == 0 or new_stat_value != old_stat_value:
                highest_shared_point = points
            lowest_shared_point = (highest_shared_point - shared_count)
            shared_point_total = (((float(highest_shared_point) / 2) * (highest_shared_point + 1)) -
                                  ((float(lowest_shared_point) / 2) * (lowest_shared_point + 1)))
            shared_points = float(shared_point_total) / float(shared_count)
            team[points_title] = shared_points
            old_stat_value = new_stat_value
        else:
            highest_shared_point = 0
            team[points_title] = points
        points -= 1

def league_volatility(sgp_dict, final_stats, factor=1):
    """Calculates volatility for each position. Volatility = # of teams within factor * SGP\n
    Args:\n
        sgp_dict: dict of sgp values for each statistic\n
        final_stats: list of dicts of teams with full season stat projections, ranks, and
        final point totals.\n
        factor: sgp multiplier\n
    Returns:\n
        list of dicts of teams with full season stat projections, ranks, final point totals,
        and upward/downward volatility.\n
    Raises:\n
        None.
    """
    calc_volatility(sgp_dict, final_stats, "R", factor)
    calc_volatility(sgp_dict, final_stats, "HR", factor)
    calc_volatility(sgp_dict, final_stats, "RBI", factor)
    calc_volatility(sgp_dict, final_stats, "SB", factor)
    calc_volatility(sgp_dict, final_stats, "OPS", factor)
    calc_volatility(sgp_dict, final_stats, "W", factor)
    calc_volatility(sgp_dict, final_stats, "SV", factor)
    calc_volatility(sgp_dict, final_stats, "K", factor)
    calc_volatility(sgp_dict, final_stats, "ERA", factor, True)
    calc_volatility(sgp_dict, final_stats, "WHIP", factor, True)
    for team in final_stats:
        team['Total Upward Volatility'] = sum([value for key, value in team.items() if 'UpVol' in key])
        team['Total Downward Volatility'] = sum([value for key, value in team.items() if 'DownVol' in key])
    return final_stats

def calc_volatility(sgp_dict, final_stats, stat, factor, reverse=True):
    """Calculates volatility for individual stat. Volatility = # of teams within factor * SGP\n
    Args:\n
        sgp_dict: dict of sgp values for each statistic\n
        final_stats: list of dicts of teams with full season stat projections, ranks, and
        final point totals.\n
        stat: statistic to calculate\n
        factor: sgp multiplier\n
        reverse: whether or not to reverse the ranking (ERA/WHIP = False, else = True)\n
    Returns:\n
        list of dicts of teams with full season stat projections, ranks, final point totals,
        and upward/downward volatility for specific stat.\n
    Raises:\n
        None.
    """
    stats_title = "Stats" + stat
    up_vol_title = "UpVol " + stat
    down_vol_title = "DownVol " + stat
    sgp_title = stat + " SGP"
    sgp = abs(sgp_dict[sgp_title] * factor)
    final_stats.sort(key=operator.itemgetter(stats_title), reverse=reverse)
    list_length = len(final_stats)

    for i in range(list_length):
        up_counter = 0
        down_counter = 0
        j = i - 1
        k = i + 1
        current_team_stat = final_stats[i][stats_title]
        while (j > 0 and (abs(final_stats[j][stats_title] - current_team_stat) <= sgp)):
            if final_stats[j][stats_title] - current_team_stat == sgp:
                up_counter -= .5
            j -= 1
            up_counter += 1
        while (k < list_length and (abs(current_team_stat - final_stats[k][stats_title]) <= sgp)):
            if current_team_stat - final_stats[k][stats_title] == sgp:
                down_counter -= .5
            k += 1
            down_counter += 1
        final_stats[i][up_vol_title] = up_counter
        final_stats[i][down_vol_title] = down_counter

def trade_analyzer(projected_volatility, team_a, team_a_players, team_b, team_b_players, team_list,
                   league_pos_dict, ros_proj_b_list, ros_proj_p_list, current_standings,
                   league_settings, sgp_dict):
    """Analyzes value of trade for 2 teams\n
    Args:\n
        projected_volatility: projected volatility for league\n
        team_a: Team A dict\n
        team_a_players: list of players to be offered\n
        team_b: Team B dict\n
        team_b_players: list of players to be offered\n
        team_list: \n
        league_pos_dict: \n
        ros_proj_b_list: \n
        ros_proj_p_list: \n
        current_standings: \n
        league_settings: \n
        sgp_dict: \n
    Returns:\n
        Updated standings post trade\n
    Raises:\n
        None.
    """
    for player in team_a_players:
        team_a['ROSTER'].remove(player)
        team_b['ROSTER'].append(player)
    for player in team_b_players:
        team_a['ROSTER'].append(player)
        team_b['ROSTER'].remove(player)
    for team in team_list:
        if (team['TEAM_NUMBER'] == team_a['TEAM_NUMBER'] or
                team['TEAM_NUMBER'] == team_b['TEAM_NUMBER']):
            team.update()
            team_list.remove(team)

    for team in team_list:
        if (team['TEAM_NUMBER'] == team_a['TEAM_NUMBER'] or
                team['TEAM_NUMBER'] == team_b['TEAM_NUMBER']):
            team.update((k, "new") for k, v in team.iteritems() if v == "value2")
    
    # for team in team_list:
    #     if team['TEAM_NUMBER'] == team_a['TEAM_NUMBER']:
    #         team_listteam = team_a

    for key, value in enumerate(team_list):
        if team_a['TEAM_NUMBER'] in key:
            value = team_a['ROSTER']

    [team_a if x['TEAM_NUMBER'] == team_a['TEAM_NUMBER'] else x for x in team_list]
    [team_b if x['TEAM_NUMBER'] == team_b['TEAM_NUMBER'] else x for x in team_list]

    final_stats = final_stats_projection(team_list, ros_proj_b_list,
                                         ros_proj_p_list, league_pos_dict,
                                         current_standings, league_settings)
    volatility_standings = league_volatility(sgp_dict, final_stats)
    ranked_standings = rank_list(volatility_standings)
    return ranked_standings

    post_trade_standings = dict(projected_volatility)

def name_checker(name_a, name_b):
    """Checks first names against nicknames/shortened names\n
    Args:\n
        source_name: full name of the source player\n
        destination_name: full name of the destination player\n
    Returns:\n
        True if match\n
    Raises:\n
        None.
    """
    name_a_chars = name_char_pair_creator(name_a)
    name_b_chars = name_char_pair_creator(name_b)
    similarity = name_char_pair_comparer(name_a_chars, name_b_chars)
    match = False
    if similarity > 60.0:
        match = True
    return match

def name_char_pair_creator(name):
    """Checks first names against nicknames/shortened names\n
    Args:\n
        name (str): full name of the source player\n
    Returns:\n
        (list) of the name's character pairs\n
    Raises:\n
        None.
    """
    name = name.strip().lower()
    name = re.sub(r"\W", "", name).strip()
    char_pair_list = []
    i = 0
    while i < len(name) - 1:
        char_pair = name[i] + name[i + 1]
        char_pair_list.append(char_pair)
        i += 1
    return char_pair_list

def name_char_pair_comparer(name_a_chars, name_b_chars):
    """Checks first names against nicknames/shortened names\n
    Args:\n
        name_a_chars (list): list of the name's character pairs\n
        name_b_chars (list): list of the name's character pairs\n
    Returns:\n
        (float) percentage of match value\n
    Raises:\n
        None.
    """
    match_counter = 0
    total_pairs = len(name_a_chars) + len(name_b_chars)
    for a_pair in name_a_chars:
        for b_pair in name_b_chars:
            if a_pair == b_pair:
                match_counter += 1
    match_value = (float(match_counter) / float(total_pairs)) * 100.0 * 2.0
    return match_value

def name_comparer(name_a, name_b):
    name_list = {'chris':['chris', 'christopher', 'topher'],
                 'alex':['alex', 'alexander'],
                 'ken':['ken', 'kenneth'],
                 'jake':['jake', 'jacob'],
                 'greg':['greg', 'gregory'],
                 'matt':['matt', 'matthew'],
                 'brad':['brad', 'bradley'],
                 'mike':['mike', 'michael'],
                 'john':['john', 'jon', 'johnny', 'johnathan'],
                 'dan':['dan', 'danny', 'daniel'],
                 'steve':['steve', 'steven', 'stephen'],
                 'bill':['bill', 'billy', 'will', 'william'],
                 'charlie':['charlie', 'chuck', 'charles'],
                 'tony':['tony', 'anthony'],
                 'zack':['zack', 'zach', 'zachary'],
                 'manny':['manny', 'manuel'],
                 'tom':['tom', 'tommy', 'thomas'],
                 'dave':['dave', 'david'],
                 'josh':['josh', 'joshua'],
                 'drew':['drew', 'andy', 'andrew'],
                 'fred':['fred', 'freddie', 'freddy', 'frederick'],
                 'scott':['scott', 'scotty', 'scottie'],
                 'sam':['sam', 'sammy', 'sammie', 'samuel'],
                 'jim':['jim', 'jimmy', 'jimmie', 'james'],
                 'joe':['joe', 'joey', 'joseph'],
                 'bran':['bran', 'brand', 'brandon'],
                 'javy':['javy', 'javier'],
                 'rob':['rob', 'robbie', 'bob', 'bobbie', 'bobby', 'robert'],
                 'sal':['sal', 'salvador'],
                 'al':['al', 'allen', 'alan', 'allan', 'albert'],
                 'vince':['vince', 'vincent']}
    name_a = name_a.replace(".", "").lower())
    name_b = name_b.replace(".", "").lower())
    name_a_groups = re.search(r'^(\w*)(.*?(?=\sJr)|.*)(\sJr)?', name_a)
    name_a_first = name_a_groups.group(1)
    name_a_last = name_a_groups.group(2)
    name_a_norm = "a"
    name_b_groups = re.search(r'^(\w*)(.*?(?=\sJr)|.*)(\sJr)?', name_b)
    name_b_first = name_b_groups.group(1)
    name_b_last = name_b_groups.group(2)
    name_b_norm = "b"
    if name_a == name_b:
        return True
    if name_a_last != name_b_last:
        return False
    for key, val in name_list.iteritems():
        if name_a_first in val:
            name_a_norm = key
        if name_b_first in val:
            name_b_norm = key
    if name_a_norm == name_b_norm:
        return True
    return False

def team_comparer(team_a, team_b):
    team_list = {'LAA':['LAA', 'AN', 'ANA'],
                 'ARI':['ARI'],
                 'ATL':['ATL'],
                 'BAL':['BAL'],
                 'BOS':['BOS'],
                 'CHW':['CHW', 'CHA', 'CWS'],
                 'CHC':['CHC', 'CHN'],
                 'CIN':['CIN'],
                 'CLE':['CLE'],
                 'COL':['COL'],
                 'DET':['DET'],
                 'FA':['FA'],
                 'MIA':['MIA', 'FLO', 'FL'],
                 'HOU':['HOU'],
                 'KC':['KC', 'KCA'],
                 'LAD':['LAD', 'LAN', 'LA'],
                 'MIL':['MIL'],
                 'MIN':['MIN'],
                 'NYY':['NYY', 'NYA'],
                 'NYM':['NYM', 'NYN'],
                 'OAK':['OAK'],
                 'PHI':['PHI'],
                 'PIT':['PIT'],
                 'SD':['SD', 'SDN'],
                 'SEA':['SEA'],
                 'SF':['SF', 'SFN'],
                 'STL':['STL', 'SLN'],
                 'TB':['TB', 'TBA'],
                 'TEX':['TEX'],
                 'TOR':['TOR'],
                 'WAS':['WAS', 'WSH']}
    team_a = team_a.upper()
    team_b = teams_b.upper()
    team_a_norm = "a"
    team_b_norm = "b"
    if team_a == team_b:
        return True
    for key, val in team_list.iteritems():
        if team_a in val:
            team_a_norm = key
        if team_b) in val:
            team_b_norm = key
    if team_a_norm == team_b_norm:
        return True
    return False

# NAME_A = "Joe H. Smith"
# NAME_B = "Joseph Smith"
# NAME_C = "Joe Smith"
# NAME_D = "Jorge De La Rosa"
# NAME_E = "Rubby De La Rosa"
# CHARS_A = name_char_pair_creator(NAME_A)
# CHARS_B = name_char_pair_creator(NAME_B)
# CHARS_C = name_char_pair_creator(NAME_C)
# CHARS_D = name_char_pair_creator(NAME_D)
# CHARS_E = name_char_pair_creator(NAME_E)
# print CHARS_A
# print CHARS_C
# print name_char_pair_comparer(CHARS_D, CHARS_E)

# print name_checker(NAME_D, NAME_E)
# # # 60

# print name_comparer('Ken Giles Jr.', 'Kenneth Giles')