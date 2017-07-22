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
    keeper = 0.00
    # FA Status
    isFA = False

    def __init__(self, name, team, pos, category, atbats=0, runs=0, hrs=0, rbis=0,
                 sbs=0, avg=0.000, ops=0.000):
        # Descriptive Properties
        self.name = str(name)
        self.team = str(team)
        self.pos = str(pos).split(",")
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

    def __getitem__(self, name):
        return self.__dict__[name]

    # def get_dollar_value(self):
    #     """Return dollar value of player"""
    #     return self.dollarValue

class Pitcher(object):
    """The Pitcher Model"""
    # Descriptive Properties
    name = ""
    team = ""
    pos = ""
    is_sp = False
    # last_modified =
    category = ""
    # Raw Stat Properties
    ips = 0.0
    wins = 0
    svs = 0
    sos = 0
    era = 0
    whip = 0.000
    kip = 0.000
    # Initial zScore Properties
    zScoreW = 0.000
    zScoreSv = 0.000
    zScoreK = 0.000
    zScoreEra = 0.000
    zScoreWhip = 0.000
    # Weighted (Multiplied by AB) Properties
    weightedW = 0.000
    weightedSv = 0.000
    weightedK = 0.000
    weightedEra = 0.000
    weightedWhip = 0.000
    # Weighted and RezScored Properties
    weightedZscoreW = 0.000
    weightedZscoreSv = 0.000
    weightedZscoreK = 0.000
    weightedZscoreEra = 0.000
    weightedZscoreWhip = 0.000
    # Values
    fvaaz = 0.00
    dollarValue = 0.00
    keeper = 0.00
    # FA Status
    isFA = False

    def __init__(self, name, team, pos, category, ips=0, wins=0, svs=0, sos=0,
                 era=0.000, whip=0.000):
        # Descriptive Properties
        self.name = str(name)
        self.team = str(team)
        self.pos = str(pos).split(",")
        # self.last_modified = last_modified
        self.category = str(category)
        # Raw Stat Properties
        self.ips = float(ips if ips != None else 0.0)
        self.wins = int(wins if wins != None else 0)
        self.svs = int(svs if svs != None else 0)
        self.sos = int(sos if sos != None else 0)
        self.era = float(era if era != None else 0.0)
        self.whip = float(whip if whip != None else 0.0)
        self.kip = float(sos) / float(ips) if sos != None and ips != None else 0.0
        # SP Status
        self.is_sp = (False if 'SP' not in str(pos) or int(svs) > 0 or
                      float(wins) / float(ips) < 0.05 else True)

    def __getitem__(self, name):
        return self.__dict__[name]

    # def get_dollar_value(self):
    #     """Return dollar value of player"""
    #     return self.dollarValue
