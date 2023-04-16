import time
import pandas as pd
from classes.Enums.KlineIntervalsEnum import KlineIntervalsEnum
from classes.Constants.Constants import Constants


class HelperMethods:

    @staticmethod
    def toNumeric(oldDf):
        pd.options.mode.chained_assignment = None
        oldDf["open"] = pd.to_numeric(oldDf["open"], errors='coerce')
        oldDf["high"] = pd.to_numeric(oldDf["high"], errors='coerce')
        oldDf["low"] = pd.to_numeric(oldDf["low"], errors='coerce')
        oldDf["close"] = pd.to_numeric(oldDf["close"], errors='coerce')
        return oldDf

    @staticmethod
    def zeroValueCorrection(value):
        if value == 0:
            return value + 0.00000001
        return value

    @staticmethod
    def klinesEnumToSleepTime(kline: KlineIntervalsEnum) -> int:
        if (kline == KlineIntervalsEnum.FIVEMINUTES):
            return 5
        elif (kline == KlineIntervalsEnum.FIFTEENMINUTES):
            return 25
        elif (kline == KlineIntervalsEnum.ONEHOUR):
            return 45
        elif (kline == KlineIntervalsEnum.FOURHOURS):
            return 65
        elif (kline == KlineIntervalsEnum.ONEDAY):
            return 85
        else:
            return 105

    @staticmethod
    def klinesEnumToStdevMultiplier(kline: KlineIntervalsEnum) -> float:
        if (kline == KlineIntervalsEnum.FIVEMINUTES or kline == KlineIntervalsEnum.FIFTEENMINUTES):
            return (1/8)
        elif (kline == KlineIntervalsEnum.ONEHOUR or kline == KlineIntervalsEnum.FOURHOURS):
            return (1/4)
        elif (kline == KlineIntervalsEnum.ONEDAY):
            return (3/4)
        else:
            return 1.00

    @staticmethod
    def getAllVisibleSymbols():
        symbolsDict = Constants.getAllSymbols()
        symbols = []
        for symbolDict in symbolsDict:
            if symbolDict["visibility"]:
                symbols.append(symbolDict["symbol"])
        return symbols

    @staticmethod
    def getAllKlineIntervalValues():
        klinesIntervals = []
        for kline in KlineIntervalsEnum:
            klinesIntervals.append(kline.value)
        return klinesIntervals

    @staticmethod
    def getAllVisibleSymbolsForScheduler():
        symbolsDict = Constants.getAllSymbols()
        schedulerList = []
        for symbolDict in symbolsDict:
            if symbolDict["visibility"]:
                for kline in KlineIntervalsEnum:
                    schedulerDict = {}
                    schedulerDict["symbol"] = symbolDict["symbol"]
                    schedulerDict["interval"] = kline.value
                    schedulerDict["start_date"] = "2021-11-30 00:00:00"
                    schedulerDict["id"] = f"{symbolDict['symbol']}-{kline.value}"
                    schedulerDict["name"] = f"{symbolDict['symbol']}-{kline.value}-scheduler"
                    schedulerDict["sleepTime"] = HelperMethods.klinesEnumToSleepTime(
                        kline)
                    schedulerDict["stdevMultiplier"] = HelperMethods.klinesEnumToStdevMultiplier(
                        kline)
                    schedulerList.append(schedulerDict)
        return schedulerList
