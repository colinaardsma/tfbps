"""TESTS"""
import player_models
import html_parser
import z_score_calc
import heapq

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

def calculate_batter_z_score(batter_list, top_n_values, dollar_players, dollar_per_fvaaz):
    """Calculate zScores for batters"""
    # Standard Calculations
    run_list = []
    hr_list = []
    rbi_list = []
    sb_list = []
    ops_list = []
    # weighted_batter_list = []
    for batter in batter_list:
        run_list.append(batter.runs)
        hr_list.append(batter.hrs)
        rbi_list.append(batter.rbis)
        sb_list.append(batter.sbs)
        ops_list.append(batter.ops)
    run_list_nlargest = heapq.nlargest(top_n_values, run_list)
    hr_list_nlargest = heapq.nlargest(top_n_values, hr_list)
    rbi_list_nlargest = heapq.nlargest(top_n_values, rbi_list)
    sb_list_nlargest = heapq.nlargest(top_n_values, sb_list)
    ops_list_nlargest = heapq.nlargest(top_n_values, ops_list)
    # Average Calculation
    r_avg = z_score_calc.avg_calc(run_list_nlargest)
    hr_avg = z_score_calc.avg_calc(hr_list_nlargest)
    rbi_avg = z_score_calc.avg_calc(rbi_list_nlargest)
    sb_avg = z_score_calc.avg_calc(sb_list_nlargest)
    ops_avg = z_score_calc.avg_calc(ops_list_nlargest)
    # Standard Deviation Calculation
    r_std_dev = z_score_calc.std_dev_calc(run_list_nlargest, r_avg)
    hr_std_dev = z_score_calc.std_dev_calc(hr_list_nlargest, hr_avg)
    rbi_std_dev = z_score_calc.std_dev_calc(rbi_list_nlargest, rbi_avg)
    sb_std_dev = z_score_calc.std_dev_calc(sb_list_nlargest, sb_avg)
    ops_std_dev = z_score_calc.std_dev_calc(ops_list_nlargest, ops_avg)
    # zScore Calculation
    for batter in batter_list:
        batter.zScoreR = z_score_calc.z_score_calc(batter.runs, r_avg, r_std_dev)
        batter.weightedR = batter.zScoreR * float(batter.atbats)
        batter.zScoreHr = z_score_calc.z_score_calc(batter.hrs, hr_avg, hr_std_dev)
        batter.weightedHr = batter.zScoreHr * float(batter.atbats)
        batter.zScoreRbi = z_score_calc.z_score_calc(batter.rbis, rbi_avg, rbi_std_dev)
        batter.weightedRbi = batter.zScoreRbi * float(batter.atbats)
        batter.zScoreSb = z_score_calc.z_score_calc(batter.sbs, sb_avg, sb_std_dev)
        batter.weightedSb = batter.zScoreSb * float(batter.atbats)
        batter.zScoreOps = z_score_calc.z_score_calc(batter.ops, ops_avg, ops_std_dev)
        batter.weightedOps = batter.zScoreOps * float(batter.atbats)
        # weighted_batter_list.append(batter)
    # Weighted Calculations
    weighted_run_list = []
    weighted_hr_list = []
    weighted_rbi_list = []
    weighted_sb_list = []
    weighted_ops_list = []
    # for batter in weighted_batter_list:
    for batter in batter_list:
        weighted_run_list.append(batter.weightedR)
        weighted_hr_list.append(batter.weightedHr)
        weighted_rbi_list.append(batter.weightedRbi)
        weighted_sb_list.append(batter.weightedSb)
        weighted_ops_list.append(batter.weightedOps)
    weighted_run_list_nlargest = heapq.nlargest(top_n_values, weighted_run_list)
    weighted_hr_list_nlargest = heapq.nlargest(top_n_values, weighted_hr_list)
    weighted_rbi_list_nlargest = heapq.nlargest(top_n_values, weighted_rbi_list)
    weighted_sb_list_nlargest = heapq.nlargest(top_n_values, weighted_sb_list)
    weighted_ops_list_nlargest = heapq.nlargest(top_n_values, weighted_ops_list)
    # Weighted Average Calculation
    weighted_r_avg = z_score_calc.avg_calc(weighted_run_list_nlargest)
    weighted_hr_avg = z_score_calc.avg_calc(weighted_hr_list_nlargest)
    weighted_rbi_avg = z_score_calc.avg_calc(weighted_rbi_list_nlargest)
    weighted_sb_avg = z_score_calc.avg_calc(weighted_sb_list_nlargest)
    weighted_ops_avg = z_score_calc.avg_calc(weighted_ops_list_nlargest)
    # Weighted Standard Deviation Calculation
    weighted_r_std_dev = z_score_calc.std_dev_calc(weighted_run_list_nlargest, weighted_r_avg)
    weighted_hr_std_dev = z_score_calc.std_dev_calc(weighted_hr_list_nlargest, weighted_hr_avg)
    weighted_rbi_std_dev = z_score_calc.std_dev_calc(weighted_rbi_list_nlargest, weighted_rbi_avg)
    weighted_sb_std_dev = z_score_calc.std_dev_calc(weighted_sb_list_nlargest, weighted_sb_avg)
    weighted_ops_std_dev = z_score_calc.std_dev_calc(weighted_ops_list_nlargest, weighted_ops_avg)
    # Weighted zScore Calculation
    for batter in batter_list:
        batter.weightedZscoreR = z_score_calc.z_score_calc(batter.weightedR, weighted_r_avg,
                                                           weighted_r_std_dev)
        batter.weightedZscoreHr = z_score_calc.z_score_calc(batter.weightedHr, weighted_hr_avg,
                                                            weighted_hr_std_dev)
        batter.weightedZscoreRbi = z_score_calc.z_score_calc(batter.weightedRbi, weighted_rbi_avg,
                                                             weighted_rbi_std_dev)
        batter.weightedZscoreSb = z_score_calc.z_score_calc(batter.weightedSb, weighted_sb_avg,
                                                            weighted_sb_std_dev)
        batter.weightedZscoreOps = z_score_calc.z_score_calc(batter.weightedOps, weighted_ops_avg,
                                                             weighted_ops_std_dev)
    # Calculate Values
    # this section isnt done
    for batter in batter_list:
        batter.fvaaz = (batter.zScoreR + batter.zScoreHr + batter.zScoreRbi + batter.zScoreSb +
                        batter.weightedZscoreOps)
    for batter in batter_list:
        fvaaz_list_nlargest = heapq.nlargest(top_n_values, (weighted_hr_list - dollar_players))
        if batter.fvaaz >= fvaaz_list_nlargest[weighted_hr_list - dollar_players]:
            batter.dollarValue = batter.fvaaz * dollar_per_fvaaz
    return batter_list

# print len(create_full_batter_test(ROS_BATTER_URL))
# print create_full_batter_test(ROS_BATTER_URL)[1447].__dict__
# print create_full_batter_test(ROS_BATTER_URL)[0].__dict__
# print calculate_batter_z_score(create_full_batter_test(ROS_BATTER_URL), 175, 30, 3.0)
print calculate_batter_z_score(create_full_batter_test(ROS_BATTER_URL), 175, 30, 3.0)[0].__dict__

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