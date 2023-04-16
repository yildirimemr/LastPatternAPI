import pandas as pd
import pandas_ta as ta
from math import isnan
from .Helpers.HelperMethods import HelperMethods
from .Enums.ClosePriceEnum import ClosePricePosition


class Indicators:
    def __init__(self, df) -> None:
        self.klinesDf = HelperMethods.toNumeric(df)

    def bbands(self, addDate=False):
        bbands = self.klinesDf.ta.bbands(length=20)
        if addDate:
            dates = []
            for i in range(len(bbands)):
                dates.append(self.klinesDf["date"][i])
            bbands["date"] = dates
        return bbands

    def bbd(self) -> ClosePricePosition:
        bbands = self.bbands()
        currentclosePriceDf = self.klinesDf.iloc[-1:]
        currentUpperBand = bbands["BBU_20_2.0"].iloc[-1]
        currentlowerBand = bbands["BBL_20_2.0"].iloc[-1]
        currentMiddleBand = bbands["BBM_20_2.0"].iloc[-1]
        currentclosePrice = currentclosePriceDf["close"].iloc[-1]

        bbw = (currentUpperBand - currentlowerBand) / \
            currentMiddleBand  # for volatility

        dU = HelperMethods.zeroValueCorrection(
            currentclosePrice - currentUpperBand)
        dL = HelperMethods.zeroValueCorrection(
            currentclosePrice - currentlowerBand)

        position = ClosePricePosition.MIDDLE
        ratio = dL / dU  # for Volatility

        if dU > 0 and dL > 0:
            position = ClosePricePosition.ABOVE
        elif dU < 0 and dL < 0:
            position = ClosePricePosition.BELOW

        return position, bbw

    def rsi(self) -> float:
        """
        if returned value less than 30, price can raise and
        if returned value bigger than 70, price can down
        """
        rsi = self.klinesDf.ta.rsi()
        return rsi.iloc[-1]

    def cci(self) -> float:
        """
        if returned value less than -100, price can raise and
        if returned value bigger than +100, price can down
        """
        cci = self.klinesDf.ta.cci()
        return cci.iloc[-1]

    def stoch(self) -> float:
        """
        if returned value less than 20, price can raise and
        if returned value bigger than 80, price can down
        """
        stoch = self.klinesDf.ta.stoch()
        return stoch["STOCHk_14_3_3"].iloc[-1]

    def stochrsi(self) -> float:
        """
        if returned value less than 20, price can raise and
        if returned value bigger than 80, price can down
        """
        stochrsi = self.klinesDf.ta.stochrsi()
        return stochrsi["STOCHRSIk_14_14_3_3"].iloc[-1]

    def willr(self) -> float:
        """
        if returned value bigger than -20, price can down and
        if returned value less than -80, price can raise
        """
        willr = self.klinesDf.ta.willr()
        return willr.iloc[-1]

    def stdev(self, length=20) -> float:
        stdev = self.klinesDf.ta.stdev(length=length)
        return stdev.iloc[-1]

    # def adx(self) -> float:
    #     """
    #     ADX values of 20 or higher indicate that the market is trending,
    #     and for any reading less than 20, the market is viewed as “directionless” or consolidated
    #     """
    #     adx = self.klinesDf.ta.adx()
    #     return adx["ADX_14"].iloc[-1]
