from enum import Enum


class KlineIntervalsEnum(Enum):
    FIVEMINUTES = 5
    FIFTEENMINUTES = 15
    ONEHOUR = 60
    FOURHOURS = 60 * 4
    ONEDAY = 24 * 60
    # Three Days and One Week can be implement
    # THREEDAY = 3 * 24 * 60
    # ONEWEEK = 7 * 24 * 60
