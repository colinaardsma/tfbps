from enum import Enum

class BatterPOS(Enum):
    "C" = 2
    "1B" = 3
    "2B" = 4
    "SS" = 6
    "3B" = 5
    "LF" = 7
    "CF" = 8
    "RF" = 9
    "MI" = 10
    "CI" = 11
    "IF" = 12
    "OF" = 13
    "Util" = 14

class PitcherPOS(Enum):
    "SP" = 1
    "RP" = 2
    "P" = 3
    "CL" = 4