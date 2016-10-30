import math
import caching

def get_batter_z_score(stats):
    # stats = caching.cached_get_fpprojb()
    players = len(stats)

    #calculate avg for each stat
    abTotal = 0
    rTotal = 0
    hrTotal = 0
    rbiTotal = 0
    sbTotal = 0
    avgTotal = 0
    obpTotal = 0
    hTotal = 0
    doubleTotal = 0
    tripleTotal = 0
    bbTotal = 0
    kTotal = 0
    slgTotal = 0
    opsTotal = 0

    for s in stats:
        abTotal += s.ab
        rTotal += s.r
        hrTotal += s.hr
        rbiTotal += s.rbi
        sbTotal += s.sb
        avgTotal += s.avg
        obpTotal += s.obp
        hTotal += s.h
        doubleTotal += s.double
        tripleTotal += s.triple
        bbTotal += s.bb
        kTotal += s.k
        slgTotal += s.slg
        opsTotal += s.ops
    abAvg = abTotal / players
    rAvg = rTotal / players
    hrAvg = hrTotal / players
    rbiAvg = rbiTotal / players
    sbAvg = sbTotal / players
    avgAvg = avgTotal / players
    obpAvg = obpTotal / players
    hAvg = hTotal / players
    doubleAvg = doubleTotal / players
    tripleAvg = tripleTotal / players
    bbAvg = bbTotal / players
    kAvg = kTotal / players
    slgAvg = slgTotal / players
    opsAvg = opsTotal / players

    batterAvg = {"abAvg":abAvg, "rAvg":rAvg, "hrAvg":hrAvg, "rbiAvg":rbiAvg, "sbAvg":sbAvg, "avgAvg":avgAvg, "obpAvg":obpAvg, "hAvg":hAvg, "doubleAvg":doubleAvg, "tripleAvg":tripleAvg, "bbAvg":bbAvg, "kAvg":kAvg, "slgAvg":slgAvg, "opsAvg":opsAvg}

    #calculate variance for each stat
    abVar = 0
    rVar = 0
    hrVar = 0
    rbiVar = 0
    sbVar = 0
    avgVar = 0
    obpVar = 0
    hVar = 0
    doubleVar = 0
    tripleVar = 0
    bbVar = 0
    kVar = 0
    slgVar = 0
    opsVar = 0

    for s in stats:
        abVar += math.pow(s.ab, 2)
        rVar += math.pow(s.r, 2)
        hrVar += math.pow(s.hr, 2)
        rbiVar += math.pow(s.rbi, 2)
        sbVar += math.pow(s.sb, 2)
        avgVar += math.pow(s.avg, 2)
        obpVar += math.pow(s.obp, 2)
        hVar += math.pow(s.h, 2)
        doubleVar += math.pow(s.double, 2)
        tripleVar += math.pow(s.triple, 2)
        bbVar += math.pow(s.bb, 2)
        kVar += math.pow(s.k, 2)
        slgVar += math.pow(s.slg, 2)
        opsVar += math.pow(s.ops, 2)
    abTotalVar = abVar / (players - 1)
    rTotalVar = rVar / (players - 1)
    hrTotalVar = hrVar / (players - 1)
    rbiTotalVar = rbiVar / (players - 1)
    sbTotalVar = sbVar / (players - 1)
    avgTotalVar = avgVar / (players - 1)
    obpTotalVar = obpVar / (players - 1)
    hTotalVar = hVar / (players - 1)
    doubleTotalVar = doubleVar / (players - 1)
    tripleTotalVar = tripleVar / (players - 1)
    bbTotalVar = bbVar / (players - 1)
    kTotalVar = kVar / (players - 1)
    slgTotalVar = slgVar / (players - 1)
    opsTotalVar = opsVar / (players - 1)

    #are these numbers calculating correctly?
    batterVar = {"abTotalVar":abTotalVar, "rTotalVar":rTotalVar, "hrTotalVar":hrTotalVar, "rbiTotalVar":rbiTotalVar, "sbTotalVar":sbTotalVar, "avgTotalVar":avgTotalVar, "obpTotalVar":obpTotalVar, "hTotalVar":hTotalVar, "doubleTotalVar":doubleTotalVar, "tripleTotalVar":tripleTotalVar, "bbTotalVar":bbTotalVar, "kTotalVar":kTotalVar, "slgTotalVar":slgTotalVar, "opsTotalVar":opsTotalVar}

    batter = [batterAvg, batterVar]

    return batter
