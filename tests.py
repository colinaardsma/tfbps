"""TESTS"""
import player_models
import html_parser
import z_score_calc

ROS_BATTER_URL = "http://www.fantasypros.com/mlb/projections/ros-hitters.php"

def create_full_batter_test(url):
    """Test creation of batters"""
    raw_batter_list = html_parser.fantasy_pro_batters(url)
    batter_model_list = []
    for raw_batter in raw_batter_list:
        if raw_batter.get("OPS") == .000 or raw_batter.get("AVG") == .000:
            continue
        batter = player_models.Batter(name=raw_batter.get("NAME"), team=raw_batter.get("TEAM"),
                                      pos=raw_batter.get("POS"), category="FantProBatter",
                                      atbats=raw_batter.get("AB"), runs=raw_batter.get("R"),
                                      hrs=raw_batter.get("HR"), rbis=raw_batter.get("RBI"),
                                      sbs=raw_batter.get("SB"), avg=raw_batter.get("AVG"),
                                      ops=raw_batter.get("OPS"))
        batter_model_list.append(batter)
    return batter_model_list

print create_full_batter_test(ROS_BATTER_URL)

def calculate_batter_z_score(batter_list):
    """Calculate zScores for batters"""
    run_list = []
    hr_list = []
    rbi_list = []
    sb_list = []
    ops_list = []
    for batter in batter_list:
        run_list.append(batter.runs)
        hr_list.append(batter.hrs)
        rbi_list.append(batter.rbi)
        sb_list.append(batter.sbs)
        ops_list.append(batter.ops)
    # Average Calculation
    r_avg = z_score_calc.avg_calc(run_list)
    hr_avg = z_score_calc.avg_calc(hr_list)
    rbi_avg = z_score_calc.avg_calc(rbi_list)
    sb_avg = z_score_calc.avg_calc(sb_list)
    ops_avg = z_score_calc.avg_calc(ops_list)
    # Standard Deviation Calculation
    r_std_dev = z_score_calc.std_dev_calc(run_list, r_avg)
    hr_std_dev = z_score_calc.std_dev_calc(hr_list, hr_avg)
    rbi_std_dev = z_score_calc.std_dev_calc(rbi_list, rbi_avg)
    sb_std_dev = z_score_calc.std_dev_calc(sb_list, sb_avg)
    ops_std_dev = z_score_calc.std_dev_calc(ops_list, ops_avg)
    # zScore Calculation
    for batter in batter_list:
        batter.zScoreR = z_score_calc.z_score_calc(batter.run, r_avg, r_std_dev)
        batter.weightedR = batter.zScoreR * batter.atbats
        batter.zScoreHr = z_score_calc.z_score_calc(batter.hrs, hr_avg, hr_std_dev)
        batter.weightedHr = batter.zScoreHr * batter.atbats
        batter.zScoreRbi = z_score_calc.z_score_calc(batter.rbi, rbi_avg, rbi_std_dev)
        batter.weightedRbi = batter.zScoreRbi * batter.atbats
        batter.zScoreSb = z_score_calc.z_score_calc(batter.sbs, sb_avg, sb_std_dev)
        batter.weightedSb = batter.zScoreSb * batter.atbats
        batter.zScoreOps = z_score_calc.z_score_calc(batter.ops, ops_avg, ops_std_dev)
        batter.weightedOps = batter.zScoreOps * batter.atbats

# weighted zscore here

print calculate_batter_z_score()

"""  
0 VBR
1 NAME
2 TEAM
3 POS
4 AB
5 R
6 HR
7 RBI
8 SB
9 AVG
10 OBP
11 H
12 2B
13 3B
14 BB
15 SO
16 SLG
17 OPS
18 OWN
"""

# class Create_batter_test():
#     def create_batter():
#         batter = dbmodels.Batter(name="Kris Bryant", team="CHC", pos="3B", category="Test Category",
#                                  atbats=500, runs=100, hrs=40, rbis=100, sbs=20, avg=.300, ops=.999)