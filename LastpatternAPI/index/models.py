from django.db import models

class PredictionModel(models.Model):
    symbol = models.CharField(max_length=30, null=True, blank=True)
    interval = models.IntegerField(null=True, blank=True)
    createdTime = models.DateTimeField(auto_now_add=True, blank=True)
    symbolClosePrice = models.FloatField(null=True, blank=True)
    nextClosePrice = models.FloatField(null=True, blank=True)
    patternPrediction = models.IntegerField(null=True, blank=True)
    indicatorPrediction = models.IntegerField(null=True, blank=True)
    summaryPrediction = models.IntegerField(null=True, blank=True)
    realDirection = models.CharField(max_length=30, null=True, blank=True)
    patternPredictionIsSuccess = models.BooleanField(null=True, blank=True)
    indicatorPredictionIsSuccess = models.BooleanField(null=True, blank=True)
    summaryPredictionIsSuccess = models.BooleanField(null=True, blank=True)
    stdev = models.FloatField(null=True, blank=True)

class StartPredictionScheduler(models.Model):
    dummy = models.CharField(max_length=25, null=True, blank=True)

