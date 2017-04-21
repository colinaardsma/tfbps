"""zScore Calculation"""
import math

def avg_calc(stat_list):
    """Calculate the average of a list"""
    stat_total = 0
    stat_count = 0
    for stat in stat_list:
        stat_total += float(stat)
        stat_count += 1
    avg = stat_total / stat_count
    return avg

def std_dev_calc(stat_list, stat_avg):
    """Calculate the standard deviation of a list"""
    z_list = []
    for stat in stat_list:
        z_stat = math.pow(float(stat) - stat_avg, 2)
        z_list.append(z_stat)
    std_dev = math.sqrt(avg_calc(z_list))
    return std_dev

def z_score_calc(stat, stat_avg, std_dev):
    """Calculate the zScore for a list."""
    z_score = (float(stat) - stat_avg) / std_dev
    return z_score

def z_score_calc_era_whip(stat, stat_avg, std_dev):
    """Calculate the zScore for a list."""
    z_score = (stat_avg - float(stat)) / std_dev
    return z_score
