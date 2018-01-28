import pprint
import collections

def calc_sgp(stats):
    """Calculate the SGP of a list of stats"""
    stat_diff = []
    stat_diff_sum = 0
    ordered_dict = collections.OrderedDict(sorted(stats.items()))
    for i in range(len(ordered_dict) - 1):
        next_dict = ordered_dict.items()[i + 1][1]
        current_dict = ordered_dict.items()[i][1]
        diff = next_dict - current_dict
        stat_diff.append(diff)
        i += 1
    stat_diff.remove(max(stat_diff))
    stat_diff.remove(min(stat_diff))

    for diff in stat_diff:
        stat_diff_sum += diff

    avg_diff = stat_diff_sum / len(stat_diff)

    return avg_diff

def get_sgp(standings):
    sgp = {}
    stats = {}
    for team in standings:
        for key in team['Stats']:
            if key == 'IP' or key == 'TotalGP':
                continue
            stat = team['Stats'][key]
            point_value = stat['Point_Value']
            stat_value = stat['Stat_Value']
            if key not in stats:
                stats[key] = {}
            checked_point_value = check_key(stats[key], point_value)
            stats[key][checked_point_value] = stat_value
    for stat in stats:
        sgp[stat] = calc_sgp(stats[stat])
    return sgp

def check_key(stat_dict, value):
    if value in stat_dict:
        value += 0.01
        check_key(stat_dict, value)
    return value
