"""TESTS"""
import heapq
import operator
import player_models
import html_parser
import z_score_calc

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

def calculate_batter_z_score(batter_list, players_over_zero_dollars, one_dollar_players,
                             dollar_per_fvaaz, player_pool_multiplier):
    """Calculate zScores for batters"""
    player_pool = int(players_over_zero_dollars * player_pool_multiplier)
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
    run_list_nlargest = heapq.nlargest(player_pool, run_list)
    hr_list_nlargest = heapq.nlargest(player_pool, hr_list)
    rbi_list_nlargest = heapq.nlargest(player_pool, rbi_list)
    sb_list_nlargest = heapq.nlargest(player_pool, sb_list)
    ops_list_nlargest = heapq.nlargest(player_pool, ops_list)
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
    weighted_run_list_nlargest = heapq.nlargest(player_pool, weighted_run_list)
    weighted_hr_list_nlargest = heapq.nlargest(player_pool, weighted_hr_list)
    weighted_rbi_list_nlargest = heapq.nlargest(player_pool, weighted_rbi_list)
    weighted_sb_list_nlargest = heapq.nlargest(player_pool, weighted_sb_list)
    weighted_ops_list_nlargest = heapq.nlargest(player_pool, weighted_ops_list)
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
    fvaaz_list = []
    for batter in batter_list:
        batter.fvaaz = (batter.zScoreR + batter.zScoreHr + batter.zScoreRbi + batter.zScoreSb +
                        batter.weightedZscoreOps)
        fvaaz_list.append(batter.fvaaz)
    players_over_one_dollar = players_over_zero_dollars - one_dollar_players
    fvaaz_list_over_zero = heapq.nlargest(players_over_zero_dollars, fvaaz_list)
    fvaaz_list_over_one = heapq.nlargest(players_over_one_dollar, fvaaz_list)
    for batter in batter_list:
        if batter.fvaaz >= fvaaz_list_over_one[players_over_one_dollar - 1]:
            batter.dollarValue = batter.fvaaz * dollar_per_fvaaz
        elif batter.fvaaz >= fvaaz_list_over_zero[players_over_zero_dollars - 1]:
            batter.dollarValue = 1
        else:
            batter.dollarValue = 0
    # print ("Run Avg: " + str(r_avg) + "\nRun StDev: " + str(r_std_dev) + "\nHr Avg: " +
    #        str(hr_avg) + "\nHr StDev: " + str(hr_std_dev) + "\nRBI Avg: " + str(rbi_avg) +
    #        "\nRBI StDev: " + str(rbi_std_dev) + "\nsb Avg: " + str(sb_avg) + "\nsb StDev: " +
    #        str(sb_std_dev) + "\nops Avg: " + str(ops_avg) + "\nops StDev: " + str(ops_std_dev) +
    #        "\nweighted_Run Avg: " + str(weighted_r_avg) + "\nweighted_Run StDev: " +
    #        str(weighted_r_std_dev) + "\nweighted_Hr Avg: " + str(weighted_hr_avg) +
    #        "\nweighted_Hr StDev: " + str(weighted_hr_std_dev) + "\nweighted_RBI Avg: " +
    #        str(weighted_rbi_avg) + "\nweighted_RBI StDev: " + str(weighted_rbi_std_dev) +
    #        "\nweighted_sb Avg: " + str(weighted_sb_avg) + "\nweighted_sb StDev: " +
    #        str(weighted_sb_std_dev) + "\nweighted_ops Avg: " + str(weighted_ops_avg) +
    #        "\nweighted_ops StDev: " + str(weighted_ops_std_dev))
    # return batter_list.sort(key=player_models.Batter.get_dollar_value)
    return sorted(batter_list, key=operator.attrgetter('fvaaz'), reverse=True)
        # sorts by fvaaz (largest to smallest)

ROS_BATTER_URL = "http://www.fantasypros.com/mlb/projections/ros-hitters.php"
BATTER_LIST = create_full_batter_test(ROS_BATTER_URL)
PLAYERS_OVER_ZERO_DOLLARS = 176
ONE_DOLLAR_PLAYERS = 30
DOLLAR_PER_FVAAZ = 3.0
PLAYER_POOL_MULTIPLIER = 2.375
LEAGUE_NO = 5091
FA_LIST = html_parser.yahoo_batter_fa(LEAGUE_NO)
ROS_PROJECTION_LIST = calculate_batter_z_score(BATTER_LIST, PLAYERS_OVER_ZERO_DOLLARS,
                                               ONE_DOLLAR_PLAYERS, DOLLAR_PER_FVAAZ,
                                               PLAYER_POOL_MULTIPLIER)

def rate_fa(fa_list, ros_projection_list):
    """Compare available FAs with Projections"""
    fa_player_list = []
    for player in ros_projection_list:
        if any(d['NAME'] == player.name for d in fa_list):
            player.isFA = True
            fa_player_list.append(player)
    dollar_value = 100.00
    player_number = 0
    while dollar_value != 1.0:
    # for N in range(0, 10):
        print ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^20}" +
               " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3} - {player.sbs:^2}" +
               " - {player.ops:^5}").format(player=fa_player_list[player_number])
        dollar_value = fa_player_list[player_number].dollarValue
        player_number += 1

def rate_team(team_dict, ros_projection_list):
    """Compare team with Projections"""
    team_roster_list = team_dict['ROSTER']
    team_player_list = []
    for player in ros_projection_list:
        if player.name in team_roster_list:
            team_player_list.append(player)
    for player in team_player_list:
        print ("${player.dollarValue:^5.2f} - {player.name:^25} - {player.pos:^20}" +
               " - {player.runs:^3} - {player.hrs:^2} - {player.rbis:^3} - {player.sbs:^2}" +
               " - {player.ops:^5}").format(player=player)

print "Avail FAs"
rate_fa(FA_LIST, ROS_PROJECTION_LIST)
print "\nTeam Value"
rate_team(html_parser.get_single_yahoo_team(LEAGUE_NO, "MachadoAboutNothing"), ROS_PROJECTION_LIST)



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