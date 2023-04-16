import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from .models import PredictionModel

from classes.Enums.KlineIntervalsEnum import KlineIntervalsEnum
from classes.Predictions import Predictions
from classes.Enums.KlineIntervalsEnum import KlineIntervalsEnum
from classes.Enums.DirectionsEnum import Directions
from classes.Helpers.HelperMethods import HelperMethods


@util.close_old_connections
def delete_old_job_executions(max_age=86_400):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def predictionSchedulerBase(symbol: str, interval: KlineIntervalsEnum, sleepTime: int, stdevMultiplier: float):
    time.sleep(sleepTime)
    modelObjects = PredictionModel.objects.filter(symbol = symbol, interval = interval.value)
    if (modelObjects.count() == 0):
        firstPredictionModel = PredictionModel()
        firstPredictionModel.symbol = symbol
        firstPredictionModel.interval = interval.value
        firstPredictionModel.symbolClosePrice = 0
        firstPredictionModel.save()
        return
    
    lastPredictionModel = modelObjects.order_by('-createdTime')[0]
    lastClosePrice = lastPredictionModel.symbolClosePrice
    predictions = Predictions(symbol, interval, 50)
    stdev = predictions.indicators.stdev() * stdevMultiplier
    minLastClosePrice = lastClosePrice - stdev
    maxLastClosePrice = lastClosePrice + stdev
    patternsSummary, indicatorsSummary, summary = predictions.getAllPredictions()
    currentClosePrice = predictions.binance.lastClosePrice
    realDirection = Directions.NEUTRAL
    if (currentClosePrice < minLastClosePrice):
        realDirection = Directions.DOWN
    elif (currentClosePrice > maxLastClosePrice):
        realDirection = Directions.UP
    predictionModel = PredictionModel()
    predictionModel.symbol = symbol
    predictionModel.interval = interval.value
    predictionModel.createdTime = predictions.binance.lastDate
    predictionModel.symbolClosePrice = predictions.binance.lastClosePrice
    predictionModel.patternPrediction = patternsSummary.value
    predictionModel.indicatorPrediction = indicatorsSummary.value
    predictionModel.summaryPrediction = summary.value
    predictionModel.stdev = stdev
    predictionModel.save()
    lastPredictionModel.nextClosePrice = predictions.binance.lastClosePrice
    lastPredictionModel.realDirection = realDirection.value
    lastPredictionModel.patternPredictionIsSuccess = lastPredictionModel.patternPrediction == realDirection.value
    lastPredictionModel.indicatorPredictionIsSuccess = lastPredictionModel.indicatorPrediction == realDirection.value
    lastPredictionModel.summaryPredictionIsSuccess = lastPredictionModel.summaryPrediction == realDirection.value
    lastPredictionModel.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    schedulerDicts = HelperMethods.getAllVisibleSymbolsForScheduler()
    for sdict in schedulerDicts:
        scheduler.add_job(
            predictionSchedulerBase,
            "interval",
            args=[sdict["symbol"], KlineIntervalsEnum(sdict["interval"]), sdict["sleepTime"], sdict["stdevMultiplier"]],
            minutes=sdict["interval"],
            start_date=sdict["start_date"],
            id=sdict["id"],
            timezone="UTC",
            name=sdict["name"],
            jobstore='default',
            replace_existing=True)
    scheduler.start()
