from itertools import compress
import numpy as np
import pandas as pd
import pandas_ta as ta
from typing import Sequence, Union
from .Binance import Binance
from .Constants.Constants import Constants
from .Indicators import Indicators
from .Enums.KlineIntervalsEnum import KlineIntervalsEnum
from .Enums.ClosePriceEnum import ClosePricePosition
from .Enums.DirectionsEnum import Directions


class Predictions:
    def __init__(self, symbol: str, timeInterval: KlineIntervalsEnum, backTrace: int) -> None:
        self.binance = Binance(symbol)
        self.date, self.klines = self.binance.getKlines(
            timeInterval, backTrace)
        self.indicators = Indicators(self.klines)

    def getAllPredictions(self):
        patterns, patternsSummary = self.getPatternPredictions()
        indicators, indicatorsSummary = self.getIndicatorPredictions()
        sumOfPredictions = patternsSummary.value + indicatorsSummary.value
        summary = Directions.NEUTRAL
        if sumOfPredictions > 0:
            summary = Directions.UP
        elif sumOfPredictions < 0:
            summary = Directions.DOWN
        return patternsSummary, indicatorsSummary, summary

    def getPatternPredictions(self, patternName: Union[str, Sequence[str]] = "all"):
        df = self.klines.ta.cdl_pattern(name=patternName).iloc[[-1]]
        candle_names = list(df.columns)
        candle_rankings = Constants.getCandleRankings()
        df['candlestick_pattern'] = np.nan
        df['candlestick_match_count'] = np.nan
        for index, row in df.iterrows():
            # no pattern found
            if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
                df.loc[index, 'candlestick_pattern'] = "NO_PATTERN"
                df.loc[index, 'candlestick_match_count'] = 0
            # single pattern found
            elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
                # bull pattern 100 or 200
                if any(row[candle_names].values > 0):
                    pattern = list(compress(row[candle_names].keys(
                    ), row[candle_names].values != 0))[0] + '_Bull'
                    df.loc[index, 'candlestick_pattern'] = pattern
                    df.loc[index, 'candlestick_match_count'] = 1
                # bear pattern -100 or -200
                else:
                    pattern = list(compress(row[candle_names].keys(
                    ), row[candle_names].values != 0))[0] + '_Bear'
                    df.loc[index, 'candlestick_pattern'] = pattern
                    df.loc[index, 'candlestick_match_count'] = 1
            # multiple patterns matched -- select best performance
            else:
                # filter out pattern names from bool list of values
                patterns = list(
                    compress(row[candle_names].keys(), row[candle_names].values != 0))
                container = []
                for pattern in patterns:
                    if row[pattern] > 0:
                        container.append(pattern + '_Bull')
                    else:
                        container.append(pattern + '_Bear')
                rank_list = [candle_rankings[p]
                             for p in container if (p in candle_rankings)]
                if len(rank_list) == len(container):
                    rank_index_best = rank_list.index(min(rank_list))
                    df.loc[index, 'candlestick_pattern'] = container[rank_index_best]
                    df.loc[index, 'candlestick_match_count'] = len(container)
        # clean up candle columns
        df.drop(candle_names, axis=1, inplace=True)
        summary = self._patternsSummary(df)
        return df, summary

    def getIndicatorPredictions(self):
        position, bbw = self.indicators.bbd()
        rsi = self.indicators.rsi()
        cci = self.indicators.cci()
        stoch = self.indicators.stoch()
        stochrsi = self.indicators.stochrsi()
        willr = self.indicators.willr()

        indicatorPredictions = {
            "bbd": self._bbdPrediction(position),
            "rsi": self._rsiPrediction(rsi),
            "cci": self._cciPrediction(cci),
            "stoch": self._stochAndStochRsiPrediction(stoch),
            "stochrsi": self._stochAndStochRsiPrediction(stochrsi),
            "willr": self._willrPrediction(willr)
        }
        summary = self._indicatorsSummary(indicatorPredictions)
        return indicatorPredictions, summary

    def _bbdPrediction(self, position: ClosePricePosition) -> Directions:
        direction = Directions.NEUTRAL
        if (position == ClosePricePosition.BELOW):
            direction = Directions.UP
        elif (position == ClosePricePosition.ABOVE):
            direction == Directions.DOWN
        return direction

    def _rsiPrediction(self, rsiValue: float) -> Directions:
        direction = Directions.NEUTRAL
        if (rsiValue <= 10.0):
            direction = Directions.HIGHLYUP
        elif (rsiValue <= 30.0):
            direction = Directions.UP
        elif (rsiValue >= 90.0):
            direction = Directions.HIGHLYDOWN
        elif (rsiValue >= 70.0):
            direction = Directions.DOWN
        return direction

    def _cciPrediction(self, cciValue: float) -> Directions:
        direction = Directions.NEUTRAL
        if (cciValue <= -200.0):
            direction = Directions.HIGHLYUP
        elif (cciValue <= -100.0):
            direction = Directions.UP
        elif (cciValue >= 200.0):
            direction = Directions.HIGHLYDOWN
        elif (cciValue >= 100.0):
            direction = Directions.DOWN
        return direction

    def _stochAndStochRsiPrediction(self, stochValue: float) -> Directions:
        direction = Directions.NEUTRAL
        if (stochValue <= 10.0):
            direction = Directions.HIGHLYUP
        elif (stochValue <= 20.0):
            direction = Directions.UP
        elif (stochValue >= 90.0):
            direction = Directions.HIGHLYDOWN
        elif (stochValue >= 80.0):
            direction = Directions.DOWN
        return direction

    def _willrPrediction(self, willrValue: float) -> Directions:
        direction = Directions.NEUTRAL
        if (willrValue >= -10.0):
            direction = Directions.HIGHLYDOWN
        elif (willrValue >= -20):
            direction = Directions.DOWN
        elif (willrValue <= -90.0):
            direction = Directions.HIGHLYUP
        elif (willrValue <= -80.0):
            direction = Directions.UP
        return direction

    def _indicatorsSummary(self, indicatorPredictions: dict) -> Directions:
        values = []
        for indicatorPrediction in indicatorPredictions.values():
            values.append(indicatorPrediction.value)

        valuesSum = sum(values)

        direction = Directions.NEUTRAL
        if (valuesSum > 0):
            direction = Directions.UP
        elif (valuesSum < 0):
            direction = Directions.DOWN
        return direction

    def _patternsSummary(self, patternsDf) -> Directions:
        #candlestick_match_count will be used for highlyup or highlydown in future
        bullDf = patternsDf.loc[patternsDf['candlestick_pattern'].astype(str).str.contains('Bull', na = False)]
        bearDf = patternsDf.loc[patternsDf['candlestick_pattern'].astype(str).str.contains('Bear', na = False)]
        direction = Directions.NEUTRAL
        if bullDf.shape[0] > bearDf.shape[0]:
            direction = Directions.UP
        elif bearDf.shape[0] > bullDf.shape[0]:
            direction = Directions.DOWN
        return direction
