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

    def __init__(self, name, team, pos, category, atbats, runs, hrs, rbis, sbs, avg, ops):
        # Descriptive Properties
        self.name = name
        self.team = team
        self.pos = pos
        # self.last_modified = last_modified
        self.category = category
        # Raw Stat Properties
        self.atbats = atbats
        self.runs = runs
        self.hrs = hrs
        self.rbis = rbis
        self.sbs = sbs
        self.avg = avg
        self.ops = ops

    # def make_batter(name, age, major):
    #     batter = Batter(name, age, major)
    #     return batter



