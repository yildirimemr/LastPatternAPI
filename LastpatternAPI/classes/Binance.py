import os
from binance import Client
from datetime import datetime
import pandas as pd
from .Enums.KlineIntervalsEnum import KlineIntervalsEnum


class Binance:
    def __init__(self, symbol) -> None:
        self.apiKey = os.getenv("BINANCE_APIKEY")
        self.apiSecret = os.getenv("BINANCE_APISECRET")
        self.symbol = symbol
        self.lastClosePrice = None
        self.lastDate = None

    @staticmethod
    def _getIntervalAndString(interval, backtrack):
        multiplier = backtrack
        if interval == KlineIntervalsEnum.FIVEMINUTES:
            clientInterval = Client.KLINE_INTERVAL_5MINUTE
            intervalStr = f"{5 * multiplier} minute ago UTC"
        elif interval == KlineIntervalsEnum.FIFTEENMINUTES:
            clientInterval = Client.KLINE_INTERVAL_15MINUTE
            intervalStr = f"{15 * multiplier} minute ago UTC"
        elif interval == KlineIntervalsEnum.ONEHOUR:
            clientInterval = Client.KLINE_INTERVAL_1HOUR
            intervalStr = f"{1 * multiplier} hour ago UTC"
        elif interval == KlineIntervalsEnum.FOURHOURS:
            clientInterval = Client.KLINE_INTERVAL_4HOUR
            intervalStr = f"{4 * multiplier} hour ago UTC"
        elif interval == KlineIntervalsEnum.ONEDAY:
            clientInterval = Client.KLINE_INTERVAL_1DAY
            intervalStr = f"{1 * multiplier} day ago UTC"
        elif interval == KlineIntervalsEnum.THREEDAY:
            clientInterval = Client.KLINE_INTERVAL_3DAY
            intervalStr = f"{3 * multiplier} day ago UTC"
        elif interval == KlineIntervalsEnum.ONEWEEK:
            clientInterval = Client.KLINE_INTERVAL_1WEEK
            intervalStr = f"{1 * multiplier} week ago UTC"
        return clientInterval, intervalStr

    def getKlines(self, interval, backtrack):
        clientInterval, intervalStr = self._getIntervalAndString(
            interval, backtrack)
        client = Client(self.apiKey, self.apiSecret)
        rawKlines = client.get_historical_klines(
            self.symbol, clientInterval, intervalStr)
        date = datetime.strptime(datetime.utcfromtimestamp(
            float(rawKlines[-1][0]) / 1000).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        klines = []
        for i in range(backtrack - 1):
            klines.append([rawKlines[i][1], rawKlines[i][2],
                          rawKlines[i][3], rawKlines[i][4]])

        data = {"open": [], "high": [], "low": [], "close": []}
        for i in klines:
            data["open"].append(i[0])
            data["high"].append(i[1])
            data["low"].append(i[2])
            data["close"].append(i[3])
        df = pd.DataFrame(data)

        self.lastDate = date
        self.lastClosePrice = float(data["close"][-1])

        return date, df
