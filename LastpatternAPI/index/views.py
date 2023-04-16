from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializer import PredictionModelSerializer
import index.helpers as helpers

from classes.Api.BaseResponse import BaseResponse
from rest_framework.permissions import IsAdminUser
from classes.Enums.KlineIntervalsEnum import KlineIntervalsEnum


@api_view(["GET"])
@permission_classes([IsAdminUser])
def startWorkers(request):
    from .scheduler import start
    start()


@api_view(["GET"])
def getPrediction(request):
    try:
        requestData = request.query_params
        count = int(requestData['count'])
        if count <= 0:
            raise Exception("Count cannot be less than or equal to zero!")
        symbol = requestData['symbol']
        interval = int(requestData['interval'])

        symbolPredictions = helpers.getPrediction(
            symbol, KlineIntervalsEnum(interval), count)
        symbolPredictionsSerializer = PredictionModelSerializer(
            symbolPredictions["prediction"], many=True)

        response = BaseResponse(True, "", symbolPredictionsSerializer.data)

        return Response(response.toDict())

    except Exception as e:
        response = BaseResponse(False, str(e), None)
        return Response(response.toDict())


@api_view(["GET"])
def getPredictions(request):
    try:
        requestData = request.query_params
        count = int(requestData['count'])
        if count <= 0:
            raise Exception("Count cannot be less than or equal to zero!")
        symbols = requestData.getlist("symbols[]")
        intervals = [KlineIntervalsEnum(int(i))
                     for i in requestData.getlist("intervals[]")]
        predictions = helpers.getPredictions(symbols, intervals, count)
        result = [PredictionModelSerializer(
            i["prediction"], many=True).data for i in predictions]
        response = BaseResponse(True, "", result)
        return Response(response.toDict())
    except Exception as e:
        response = BaseResponse(False, str(e), None)
        return Response(response.toDict())


@api_view(["GET"])
def getStatistic(request):
    try:
        requestData = request.query_params
        count = int(requestData['count'])
        if count <= 0:
            raise Exception("Count cannot be less than or equal to zero!")
        symbol = requestData['symbol']
        interval = int(requestData['interval'])
        predictionType = requestData['predictionType']
        result = helpers.getStatistic(
            symbol, KlineIntervalsEnum(interval), predictionType, count)
        response = BaseResponse(True, "", result)
        return Response(response.toDict())
    except Exception as e:
        response = BaseResponse(False, str(e), None)
        return Response(response.toDict())


@api_view(["GET"])
def getStatistics(request):
    try:
        requestData = request.query_params
        count = int(requestData['count'])
        if count <= 0:
            raise Exception("Count cannot be less than or equal to zero!")
        symbols = requestData.getlist("symbols[]")
        intervals = [KlineIntervalsEnum(int(i))
                     for i in requestData.getlist("intervals[]")]
        predictionTypes = requestData.getlist("predictionTypes[]")
        result = helpers.getStatistics(
            symbols, intervals, predictionTypes, count)
        response = BaseResponse(True, "", result)
        return Response(response.toDict())
    except Exception as e:
        response = BaseResponse(False, str(e), None)
        return Response(response.toDict())
