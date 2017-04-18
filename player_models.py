"""Creating player models"""

class Batter(object):
    """The Batter Model"""
    # Descriptive Properties
    name = ""
    team = ""
    pos = ""
    # last_modified =
    category = ""
    # Raw Stat Properties
    atbats = 0
    runs = 0
    hrs = 0
    rbis = 0
    sbs = 0
    avg = 0.000
    ops = 0.000
    # Initial zScore Properties
    zScoreR = 0.000
    zScoreHr = 0.000
    zScoreRbi = 0.000
    zScoreSb = 0.000
    zScoreAvg = 0.000
    zScoreOps = 0.000
    # Weighted (Multiplied by AB) Properties
    weightedR = 0.000
    weightedHr = 0.000
    weightedRbi = 0.000
    weightedSb = 0.000
    weightedAvg = 0.000
    weightedOps = 0.000
    # Weighted and RezScored Properties
    weightedZscoreR = 0.000
    weightedZscoreHr = 0.000
    weightedZscoreRbi = 0.000
    weightedZscoreSb = 0.000
    weightedZscoreAvg = 0.000
    weightedZscoreOps = 0.000
    # Values
    fvaaz = 0.00
    dollarValue = 0.00

    def __init__(self, name, team, pos, category, atbats=0, runs=0, hrs=0, rbis=0, sbs=0, avg=0.000, ops=0.000):
        # Descriptive Properties
        self.name = str(name)
        self.team = str(team)
        self.pos = str(pos)
        # self.last_modified = last_modified
        self.category = str(category)
        # Raw Stat Properties
        self.atbats = int(atbats if atbats != None else 0)
        self.runs = int(runs if runs != None else 0)
        self.hrs = int(hrs if hrs != None else 0)
        self.rbis = int(rbis if rbis != None else 0)
        self.sbs = int(sbs if sbs != None else 0)
        self.avg = float(avg if avg != None else 0)
        self.ops = float(ops if ops != None else 0)

    # def make_batter(name, age, major):
    #     batter = Batter(name, age, major)
    #     return batter



