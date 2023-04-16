from typing import List
from .models import PredictionModel
from classes.Enums.KlineIntervalsEnum import KlineIntervalsEnum


def getPrediction(symbol: str, interval: KlineIntervalsEnum, count: int) -> dict:
    if (count <= 0):
        return None
    symbolPredictions = PredictionModel.objects.filter(
        symbol=symbol, interval=interval.value).order_by('-createdTime')[:count]
    predictionDict = {
        "symbol": symbol,
        "interval": interval.value,
        "prediction": symbolPredictions
    }
    return predictionDict


def getPredictions(symbols: List[str], intervals: List[KlineIntervalsEnum], count: int) -> List[dict]:
    if (count <= 0):
        return None
    predictions = []
    for symbol in symbols:
        for interval in intervals:
            symbolPredictionDict = getPrediction(symbol, interval, count)
            predictions.append(symbolPredictionDict)
    return predictions


def getStatistic(symbol: str, interval: KlineIntervalsEnum, predictionType: str, count: int) -> dict:
    if (count <= 0):
        return None
    symbolPredictions = PredictionModel.objects.filter(
        symbol=symbol, interval=interval.value, ).order_by('-createdTime')[:count]
    successValues = list(
        symbolPredictions.values_list(f"{predictionType}IsSuccess", flat=True))
    successCount = 0
    unsuccessCount = 0
    for successValue in successValues:
        if successValue:
            successCount += 1
        else:
            unsuccessCount += 1
    result = {
        "symbol": symbol,
        "interval": interval.value,
        "predictionType": predictionType,
        "numOfSuccess": successCount,
        "numOfUnsuccess": unsuccessCount,
        "percentageOfSuccess": (successCount / count) * 100,
        "percentageOfUnsuccess": (unsuccessCount / count) * 100,
    }
    return result


def getStatistics(symbols: List[str], intervals: List[KlineIntervalsEnum], predictionTypes: List[str], count: int) -> List[dict]:
    if (count <= 0):
        return None
    statisticList = []
    for symbol in symbols:
        for interval in intervals:
            for predictionType in predictionTypes:
                statistic = getStatistic(
                    symbol, interval, predictionType, count)
                statisticList.append(statistic)
    return statisticList
