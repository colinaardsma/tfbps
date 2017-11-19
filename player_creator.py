"""Create players"""
import heapq
import operator
import player_models
import html_parser
import z_score_calc
import csv_parser

def create_full_batter_html(url):
    """Create batters using html"""
    raw_batter_list = html_parser.fantasy_pro_players(url)
    return create_full_batter(raw_batter_list)

def create_full_batter_csv(csv):
    """Create batters using csv"""
    raw_batter_list = csv_parser.parse_batters_from_csv(csv)
    return create_full_batter(raw_batter_list)

def create_full_batter(raw_batter_list):
    """Create batters"""
    batter_model_list = []
    for raw_batter in raw_batter_list:
        if ((raw_batter.get("AB") is not None and float(raw_batter.get("AB")) == 0.0) or
                (raw_batter.get("OPS") is not None and float(raw_batter.get("OPS")) == .000) or
                (raw_batter.get("AVG") is not None and float(raw_batter.get("AVG")) == .000) or
                raw_batter.get("NAME") is None):
            continue
        else:
            if "DL" in raw_batter.get("STATUS") or "MiLB" in raw_batter.get("STATUS"):
                raw_batter["AB"] = float(raw_batter["AB"]) / 2
                raw_batter["R"] = float(raw_batter["R"]) / 2
                raw_batter["HR"] = float(raw_batter["HR"]) / 2
                raw_batter["RBI"] = float(raw_batter["RBI"]) / 2
                raw_batter["SB"] = float(raw_batter["SB"]) / 2
            batter = player_models.BatterHTML(name=raw_batter.get("NAME"),
                                              team=raw_batter.get("TEAM"),
                                              pos=raw_batter.get("POS"),
                                              status=raw_batter.get("STATUS"),
                                              category="batter",
                                              atbats=float(raw_batter.get("AB")),
                                              runs=float(raw_batter.get("R")),
                                              hrs=float(raw_batter.get("HR")),
                                              rbis=float(raw_batter.get("RBI")),
                                              sbs=float(raw_batter.get("SB")),
                                              avg=raw_batter.get("AVG"),
                                              ops=raw_batter.get("OPS"))
            batter_model_list.append(batter)
    return batter_model_list

def calc_batter_z_score(batter_list, players_over_zero_dollars, one_dollar_players,
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
            batter.dollarValue = 1.0
        else:
            batter.dollarValue = 0.0
    return sorted(batter_list, key=operator.attrgetter('fvaaz'), reverse=True)
        # sorts by fvaaz (largest to smallest)

def create_full_pitcher_html(url):
    """Create pitchers using html"""
    raw_pitcher_list = html_parser.fantasy_pro_players(url)
    return create_full_pitcher(raw_pitcher_list)

def create_full_pitcher_csv(csv):
    """Create pitchers using csv"""
    raw_pitcher_list = csv_parser.parse_pitchers_from_csv(csv)
    return create_full_pitcher(raw_pitcher_list)

def create_full_pitcher(raw_pitcher_list):
    """Create pitchers"""
    raw_pitcher_list = html_parser.fantasy_pro_players(url)
    pitcher_model_list = []
    for raw_pitcher in raw_pitcher_list:
        if (raw_pitcher.get("IP") is None or float(raw_pitcher.get("IP")) <= 0.0 or
                raw_pitcher.get("W") is None or float(raw_pitcher.get("W")) < 0.0 or
                raw_pitcher.get("SV") is None or float(raw_pitcher.get("SV")) < 0.0 or
                raw_pitcher.get("K") is None or float(raw_pitcher.get("K")) < 0.0 or
                raw_pitcher.get("ERA") is None or float(raw_pitcher.get("ERA")) <= 0.0 or
                raw_pitcher.get("WHIP") is None or float(raw_pitcher.get("WHIP")) <= 0.0 or
                raw_pitcher.get("NAME") is None):
            continue
        else:
            if "DL" in raw_pitcher.get("STATUS") or "MiLB" in raw_pitcher.get("STATUS"):
                raw_pitcher["IP"] = float(raw_pitcher["IP"]) / 2
                raw_pitcher["W"] = float(raw_pitcher["W"]) / 2
                raw_pitcher["SV"] = float(raw_pitcher["SV"]) / 2
                raw_pitcher["K"] = float(raw_pitcher["K"]) / 2
            pitcher = player_models.PitcherHTML(name=raw_pitcher.get("NAME"),
                                                team=raw_pitcher.get("TEAM"),
                                                pos=raw_pitcher.get("POS"),
                                                status=raw_pitcher.get("STATUS"),
                                                category="pitcher",
                                                ips=float(raw_pitcher.get("IP")),
                                                wins=float(raw_pitcher.get("W")),
                                                svs=float(raw_pitcher.get("SV")),
                                                sos=float(raw_pitcher.get("K")),
                                                era=raw_pitcher.get("ERA"),
                                                whip=raw_pitcher.get("WHIP"))
            pitcher_model_list.append(pitcher)
    return pitcher_model_list

def calc_pitcher_z_score(pitcher_list, players_over_zero_dollars, one_dollar_players,
                         dollar_per_fvaaz, player_pool_multiplier):
    """Calculate zScores for pitchers"""
    player_pool = int(players_over_zero_dollars * player_pool_multiplier)
    # max_ip = max(pitcher.ips for pitcher in pitcher_list)
    # Standard Calculations
    win_list = []
    sv_list = []
    k_list = []
    era_list = []
    whip_list = []
    # weighted_pitcher_list = []
    for pitcher in pitcher_list:
        if (pitcher.wins < 0 or pitcher.svs < 0 or pitcher.sos < 0 or
                pitcher.era < 0 or pitcher.whip < 0):
            continue
        win_list.append(pitcher.wins)
        sv_list.append(pitcher.svs)
        k_list.append(pitcher.sos)
        # TODO: is dividing by 15 the best route here?
        era_list.append(pitcher.era)
        whip_list.append(pitcher.whip)
        # era_list.append(pitcher.era * (pitcher.ips / 15))
        # whip_list.append(pitcher.whip * (pitcher.ips / 15))
    win_list_nlargest = heapq.nlargest(player_pool, win_list)
    sv_list_nlargest = heapq.nlargest(player_pool, sv_list)
    k_list_nlargest = heapq.nlargest(player_pool, k_list)
    era_list_nsmallest = heapq.nsmallest(player_pool, era_list)
    whip_list_nsmallest = heapq.nsmallest(player_pool, whip_list)
    # Average Calculation
    w_avg = z_score_calc.avg_calc(win_list_nlargest)
    sv_avg = z_score_calc.avg_calc(sv_list_nlargest)
    k_avg = z_score_calc.avg_calc(k_list_nlargest)
    era_avg = z_score_calc.avg_calc(era_list_nsmallest)
    whip_avg = z_score_calc.avg_calc(whip_list_nsmallest)
    # Standard Deviation Calculation
    w_std_dev = z_score_calc.std_dev_calc(win_list_nlargest, w_avg)
    sv_std_dev = z_score_calc.std_dev_calc(sv_list_nlargest, sv_avg)
    k_std_dev = z_score_calc.std_dev_calc(k_list_nlargest, k_avg)
    era_std_dev = z_score_calc.std_dev_calc(era_list_nsmallest, era_avg)
    whip_std_dev = z_score_calc.std_dev_calc(whip_list_nsmallest, whip_avg)
    # zScore Calculation
    for pitcher in pitcher_list:
        pitcher.zScoreW = z_score_calc.z_score_calc(pitcher.wins, w_avg, w_std_dev)
        pitcher.weightedW = pitcher.zScoreW * float(pitcher.ips)
        pitcher.zScoreSv = z_score_calc.z_score_calc(pitcher.svs, sv_avg, sv_std_dev)
        pitcher.weightedSv = pitcher.zScoreSv * float(pitcher.ips)
        pitcher.zScoreK = z_score_calc.z_score_calc(pitcher.sos, k_avg, k_std_dev)
        pitcher.weightedK = pitcher.zScoreK * float(pitcher.ips)
        pitcher.zScoreEra = z_score_calc.z_score_calc_era_whip(pitcher.era, era_avg, era_std_dev)
        pitcher.weightedEra = pitcher.zScoreEra * float(pitcher.ips)
        pitcher.zScoreWhip = z_score_calc.z_score_calc_era_whip(pitcher.whip, whip_avg,
                                                                whip_std_dev)
        pitcher.weightedWhip = pitcher.zScoreWhip * float(pitcher.ips)
        # weighted_pitcher_list.append(pitcher)
    # Weighted Calculations
    weighted_win_list = []
    weighted_sv_list = []
    weighted_k_list = []
    weighted_era_list = []
    weighted_whip_list = []
    # for pitcher in weighted_pitcher_list:
    for pitcher in pitcher_list:
        weighted_win_list.append(pitcher.weightedW)
        weighted_sv_list.append(pitcher.weightedSv)
        weighted_k_list.append(pitcher.weightedK)
        weighted_era_list.append(pitcher.weightedEra)
        weighted_whip_list.append(pitcher.weightedWhip)
    weighted_win_list_nlargest = heapq.nlargest(player_pool, weighted_win_list)
    weighted_sv_list_nlargest = heapq.nlargest(player_pool, weighted_sv_list)
    weighted_k_list_nlargest = heapq.nlargest(player_pool, weighted_k_list)
    weighted_era_list_nlargest = heapq.nlargest(player_pool, weighted_era_list)
    weighted_whip_list_nlargest = heapq.nlargest(player_pool, weighted_whip_list)
    # Weighted Average Calculation
    weighted_w_avg = z_score_calc.avg_calc(weighted_win_list_nlargest)
    weighted_sv_avg = z_score_calc.avg_calc(weighted_sv_list_nlargest)
    weighted_k_avg = z_score_calc.avg_calc(weighted_k_list_nlargest)
    weighted_era_avg = z_score_calc.avg_calc(weighted_era_list_nlargest)
    weighted_whip_avg = z_score_calc.avg_calc(weighted_whip_list_nlargest)
    # Weighted Standard Deviation Calculation
    weighted_w_std_dev = z_score_calc.std_dev_calc(weighted_win_list_nlargest, weighted_w_avg)
    weighted_sv_std_dev = z_score_calc.std_dev_calc(weighted_sv_list_nlargest, weighted_sv_avg)
    weighted_k_std_dev = z_score_calc.std_dev_calc(weighted_k_list_nlargest, weighted_k_avg)
    weighted_era_std_dev = z_score_calc.std_dev_calc(weighted_era_list_nlargest, weighted_era_avg)
    weighted_whip_std_dev = z_score_calc.std_dev_calc(weighted_whip_list_nlargest,
                                                      weighted_whip_avg)
    # Weighted zScore Calculation
    for pitcher in pitcher_list:
        pitcher.weightedZscoreW = z_score_calc.z_score_calc(pitcher.weightedW, weighted_w_avg,
                                                            weighted_w_std_dev)
        pitcher.weightedZscoreSv = z_score_calc.z_score_calc(pitcher.weightedSv, weighted_sv_avg,
                                                             weighted_sv_std_dev)
        pitcher.weightedZscoreK = z_score_calc.z_score_calc(pitcher.weightedK, weighted_k_avg,
                                                            weighted_k_std_dev)
        pitcher.weightedZscoreEra = z_score_calc.z_score_calc(pitcher.weightedEra, weighted_era_avg,
                                                              weighted_era_std_dev)
        pitcher.weightedZscoreWhip = z_score_calc.z_score_calc(pitcher.weightedWhip,
                                                               weighted_whip_avg,
                                                               weighted_whip_std_dev)
    # Calculate Values
    fvaaz_list = []
    for pitcher in pitcher_list:
        # TODO: is 0.06 the best cutoff?
        if "SP" not in pitcher.pos or ("RP" in pitcher.pos and pitcher.winsip < 0.06):
            pitcher.fvaaz = (pitcher.zScoreSv + pitcher.zScoreK +
                             pitcher.weightedZscoreEra + pitcher.weightedZscoreWhip)
        else:
            pitcher.fvaaz = (pitcher.zScoreW + pitcher.zScoreSv +
                             pitcher.zScoreK + pitcher.weightedZscoreEra +
                             pitcher.weightedZscoreWhip)
        #     pitcher.fvaaz = (pitcher.weightedZscoreSv + pitcher.weightedZscoreK +
        #                      pitcher.weightedZscoreEra + pitcher.weightedZscoreWhip)
        # else:
        #     pitcher.fvaaz = (pitcher.weightedZscoreW + pitcher.weightedZscoreSv +
        #                      pitcher.weightedZscoreK + pitcher.weightedZscoreEra +
        #                      pitcher.weightedZscoreWhip)
        fvaaz_list.append(pitcher.fvaaz)
    players_over_one_dollar = players_over_zero_dollars - one_dollar_players
    fvaaz_list_over_zero = heapq.nlargest(players_over_zero_dollars, fvaaz_list)
    fvaaz_list_over_one = heapq.nlargest(players_over_one_dollar, fvaaz_list)
    for pitcher in pitcher_list:
        if pitcher.fvaaz >= fvaaz_list_over_one[players_over_one_dollar - 1]:
            pitcher.dollarValue = pitcher.fvaaz * dollar_per_fvaaz
        elif pitcher.fvaaz >= fvaaz_list_over_zero[players_over_zero_dollars - 1]:
            pitcher.dollarValue = 1.0
        else:
            pitcher.dollarValue = 0.0
    return sorted(pitcher_list, key=operator.attrgetter('fvaaz'), reverse=True)
        # sorts by fvaaz (largest to smallest)
