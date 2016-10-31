import math
import caching


def get_z_score(stats):
    numPlayers = len(stats)
    get_r_z_score(stats, numPlayers)


def get_r_z_score(stats, numPlayers):
    #calculate mean
    rTotal = 0
    for s in stats:
        if s.ab >= 400:
            rTotal += float(s.r)
    rMean = rTotal / numPlayers

    #calculate variance
    rVar = 0
    for s in stats:
        if s.ab >= 400:
            rVar += math.pow(s.r - rMean, 2)
    rTotalVar = rVar / (numPlayers - 1)

    #calculate standard deviation
    rStdDev = math.sqrt(rTotalVar)

    # calculate z-scores
    for s in stats: # doesn't enter data for all players, times out?
        if s.ab >= 200:
            s.zr = (s.r - rMean) / rStdDev # calculate z-score
            s.put()


#####################
# def get_batter_z_score(stats):
#     # stats = caching.cached_get_fpprojb()
#     players = len(stats)
#
#     #calculate avg for each stat
#     abTotal = 0
#     rTotal = 0
#     hrTotal = 0
#     rbiTotal = 0
#     sbTotal = 0
#     avgTotal = 0
#     obpTotal = 0
#     hTotal = 0
#     doubleTotal = 0
#     tripleTotal = 0
#     bbTotal = 0
#     kTotal = 0
#     slgTotal = 0
#     opsTotal = 0
#
#     for s in stats:
#         abTotal += float(s.ab)
#         rTotal += float(s.r)
#         hrTotal += float(s.hr)
#         rbiTotal += float(s.rbi)
#         sbTotal += float(s.sb)
#         avgTotal += s.avg
#         obpTotal += s.obp
#         hTotal += float(s.h)
#         doubleTotal += float(s.double)
#         tripleTotal += float(s.triple)
#         bbTotal += float(s.bb)
#         kTotal += float(s.k)
#         slgTotal += s.slg
#         opsTotal += s.ops
#     abAvg = abTotal / players
#     rAvg = rTotal / players
#     hrAvg = hrTotal / players
#     rbiAvg = rbiTotal / players
#     sbAvg = sbTotal / players
#     avgAvg = avgTotal / players
#     obpAvg = obpTotal / players
#     hAvg = hTotal / players
#     doubleAvg = doubleTotal / players
#     tripleAvg = tripleTotal / players
#     bbAvg = bbTotal / players
#     kAvg = kTotal / players
#     slgAvg = slgTotal / players
#     opsAvg = opsTotal / players
#
#     batterAvg = {"abAvg":abAvg, "rAvg":rAvg, "hrAvg":hrAvg, "rbiAvg":rbiAvg, "sbAvg":sbAvg, "avgAvg":avgAvg, "obpAvg":obpAvg, "hAvg":hAvg, "doubleAvg":doubleAvg, "tripleAvg":tripleAvg, "bbAvg":bbAvg, "kAvg":kAvg, "slgAvg":slgAvg, "opsAvg":opsAvg}
#
#     #calculate variance for each stat
#     abVar = 0
#     rVar = 0
#     hrVar = 0
#     rbiVar = 0
#     sbVar = 0
#     avgVar = 0
#     obpVar = 0
#     hVar = 0
#     doubleVar = 0
#     tripleVar = 0
#     bbVar = 0
#     kVar = 0
#     slgVar = 0
#     opsVar = 0
#
#     for s in stats:
#         abVar += math.pow(s.ab - abAvg, 2)
#         rVar += math.pow(s.r - rAvg, 2)
#         hrVar += math.pow(s.hr - hrAvg, 2)
#         rbiVar += math.pow(s.rbi - rbiAvg, 2)
#         sbVar += math.pow(s.sb - sbAvg, 2)
#         avgVar += math.pow(s.avg - avgAvg, 2)
#         obpVar += math.pow(s.obp - obpAvg, 2)
#         hVar += math.pow(s.h - hAvg, 2)
#         doubleVar += math.pow(s.double - doubleAvg, 2)
#         tripleVar += math.pow(s.triple - tripleAvg, 2)
#         bbVar += math.pow(s.bb - bbAvg, 2)
#         kVar += math.pow(s.k - kAvg, 2)
#         slgVar += math.pow(s.slg - slgAvg, 2)
#         opsVar += math.pow(s.ops - opsAvg, 2)
#     abTotalVar = abVar / (players - 1)
#     rTotalVar = rVar / (players - 1)
#     hrTotalVar = hrVar / (players - 1)
#     rbiTotalVar = rbiVar / (players - 1)
#     sbTotalVar = sbVar / (players - 1)
#     avgTotalVar = avgVar / (players - 1)
#     obpTotalVar = obpVar / (players - 1)
#     hTotalVar = hVar / (players - 1)
#     doubleTotalVar = doubleVar / (players - 1)
#     tripleTotalVar = tripleVar / (players - 1)
#     bbTotalVar = bbVar / (players - 1)
#     kTotalVar = kVar / (players - 1)
#     slgTotalVar = slgVar / (players - 1)
#     opsTotalVar = opsVar / (players - 1)
#
#     batterVar = {"abTotalVar":abTotalVar, "rTotalVar":rTotalVar, "hrTotalVar":hrTotalVar, "rbiTotalVar":rbiTotalVar, "sbTotalVar":sbTotalVar, "avgTotalVar":avgTotalVar, "obpTotalVar":obpTotalVar, "hTotalVar":hTotalVar, "doubleTotalVar":doubleTotalVar, "tripleTotalVar":tripleTotalVar, "bbTotalVar":bbTotalVar, "kTotalVar":kTotalVar, "slgTotalVar":slgTotalVar, "opsTotalVar":opsTotalVar}
#
#     #calculate standard deviation for each stat
#     abStdDev = math.sqrt(abTotalVar)
#     rStdDev = math.sqrt(rTotalVar)
#     hrStdDev = math.sqrt(hrTotalVar)
#     rbiStdDev = math.sqrt(rbiTotalVar)
#     sbStdDev = math.sqrt(sbTotalVar)
#     avgStdDev = math.sqrt(avgTotalVar)
#     obpStdDev = math.sqrt(obpTotalVar)
#     hStdDev = math.sqrt(hTotalVar)
#     doubleStdDev = math.sqrt(doubleTotalVar)
#     tripleStdDev = math.sqrt(tripleTotalVar)
#     bbStdDev = math.sqrt(bbTotalVar)
#     kStdDev = math.sqrt(kTotalVar)
#     slgStdDev = math.sqrt(slgTotalVar)
#     opsStdDev = math.sqrt(opsTotalVar)
#
#     batterStdDev = {"abStdDev":abStdDev, "rStdDev":rStdDev, "hrStdDev":hrStdDev, "rbiStdDev":rbiStdDev, "sbStdDev":sbStdDev, "avgStdDev":avgStdDev, "obpStdDev":obpStdDev, "hStdDev":hStdDev, "doubleStdDev":doubleStdDev, "tripleStdDev":tripleStdDev, "bbStdDev":bbStdDev, "kStdDev":kStdDev, "slgStdDev":slgStdDev, "opsStdDev":opsStdDev}
#
#     #calculate z-score for each stat
#     for s in stats:
#         abVar += math.pow(s.ab - abAvg, 2)
#         rVar += math.pow(s.r - rAvg, 2)
#         hrVar += math.pow(s.hr - hrAvg, 2)
#         rbiVar += math.pow(s.rbi - rbiAvg, 2)
#         sbVar += math.pow(s.sb - sbAvg, 2)
#         avgVar += math.pow(s.avg - avgAvg, 2)
#         obpVar += math.pow(s.obp - obpAvg, 2)
#         hVar += math.pow(s.h - hAvg, 2)
#         doubleVar += math.pow(s.double - doubleAvg, 2)
#         tripleVar += math.pow(s.triple - tripleAvg, 2)
#         bbVar += math.pow(s.bb - bbAvg, 2)
#         kVar += math.pow(s.k - kAvg, 2)
#         slgVar += math.pow(s.slg - slgAvg, 2)
#         opsVar += math.pow(s.ops - opsAvg, 2)
#     abZScore = math.sqrt(abTotalVar)
#     rZScore = math.sqrt(rTotalVar)
#     hrZScore = math.sqrt(hrTotalVar)
#     rbiZScore = math.sqrt(rbiTotalVar)
#     sbZScore = math.sqrt(sbTotalVar)
#     avgZScore = math.sqrt(avgTotalVar)
#     obpZScore = math.sqrt(obpTotalVar)
#     hZScore = math.sqrt(hTotalVar)
#     doubleZScore = math.sqrt(doubleTotalVar)
#     tripleZScore = math.sqrt(tripleTotalVar)
#     bbZScore = math.sqrt(bbTotalVar)
#     kZScore = math.sqrt(kTotalVar)
#     slgZScore = math.sqrt(slgTotalVar)
#     opsZScore = math.sqrt(opsTotalVar)
#
#     batterZScore = {"abZScore":abZScore, "rZScore":rZScore, "hrZScore":hrZScore, "rbiZScore":rbiZScore, "sbZScore":sbZScore, "avgZScore":avgZScore, "obpZScore":obpZScore, "hZScore":hZScore, "doubleZScore":doubleZScore, "tripleZScore":tripleZScore, "bbZScore":bbZScore, "kZScore":kZScore, "slgZScore":slgZScore, "opsZScore":opsZScore}
#
#     batter = [batterAvg, batterVar, batterStdDev, batterZScore]
#
#     return batter
