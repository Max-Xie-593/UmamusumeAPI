from enum import Enum

class Obtained(Enum):
    GACHA = "gacha"
    LIMITED_QUEST = "limited_quest"
    MAIN_STORY = "main_story"
    PROMO = "promo"
    SHOP = "shop"
    STORY_EVENT = "story_event"

class Aptitude(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

class TypeElement(Enum):
    BTW = "btw"
    CHA = "cha"
    COR = "cor"
    DBF = "dbf"
    DIR = "dir"
    F_C = "f_c"
    F_S = "f_s"
    LDR = "ldr"
    LNG = "lng"
    L_0 = "l_0"
    L_1 = "l_1"
    L_2 = "l_2"
    L_3 = "l_3"
    MED = "med"
    MIL = "mil"
    NAC = "nac"
    RUN = "run"
    SHO = "sho"
    SLO = "slo"
    STR = "str"
    TUR = "tur"

class SupportCardType(Enum):
    FRIEND = "friend"
    GROUP = "group"
    GUTS = "guts"
    INTELLIGENCE = "intelligence"
    POWER = "power"
    SPEED = "speed"
    STAMINA = "stamina"

class Symbol(Enum):
    LEVEL = "level"
    NONE = "none"
    PERCENT = "percent"

class DidNotExist(Enum):
    PRE_2_5_TH_ANNI = "pre_2_5th_anni"
    PRE_NAR = "pre_nar"

class UnreleasedServer(Enum):
    EN = "en"
    KO = "ko"
    ZH_TW = "zh_tw"

class Location(Enum):
    CORNER = "corner"
    DOWNHILL = "downhill"
    FINAL_CORNER = "final_corner"
    FINAL_STRAIGHT = "final_straight"
    STRAIGHT = "straight"
    UNKNOWN = "unknown"
    UPHILL = "uphill"

class TEnum(Enum):
    RS = "rs" # Race Stats
    SK = "sk" # Skills