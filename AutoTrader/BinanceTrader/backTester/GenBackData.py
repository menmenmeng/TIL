import time
import requests
import numpy as np
import pandas as pd
import logging
import datetime
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.lib.utils import config_logging

# where API KEY stored.(USE YOUR OWN KEY)
from cert import binanceKey

# visualization
import matplotlib.pyplot as plt
import seaborn as sns

# need to be modified.
class BackData():
    def __init__(self):
        self.backdata = None

    # binance client Instance가 있어야 함.
    def get_backdata(self, client, interval, **kwargs): # symbol은 필요 없음, interval, startTime, endTime, limit만 있으면 된다.
        rawbackdata = client.klines('BTCUSDT', interval, **kwargs)
        columns = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'NumOfTrades',
                'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore']
        backdatadf = pd.DataFrame(rawbackdata, columns=columns)
        backdatadf['OpenTime'] = backdatadf['OpenTime'].astype("datetime64[ms]")
        backdatadf['CloseTime'] = backdatadf['CloseTime'].astype("datetime64[ms]")
        backdatadf[['Open', 'High', 'Low', 'Close', 'Volume', 'QuoteAssetVolume', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume']] = backdatadf[['Open', 'High', 'Low', 'Close', 'Volume', 'QuoteAssetVolume', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume']].astype('float64')
        backdatadf.drop(['Ignore'], axis=1, inplace=True)
        self.backdata = backdatadf
        return backdatadf

    # backdata와 window, Close(종가)의 이름을 주면 MA{window}의 열을 반환하는 것
    # 반환된 열을 Df에 추가할 수도 있고, 새로 만들 수도 있고...
    # 열을 변환하는 경우에는 항상 반환은 열로 되도록 하기.
    def get_MA(self, dataDf, window, CloseName='Close'):
        return dataDf[CloseName].astype(np.float64).rolling(window).mean()

    def get_std(self, dataDf, window, CloseName='Close'):
        return dataDf[CloseName].astype(np.float64).rolling(window).std()

    # Series 여러 개를 합쳐서 하나의 Df로 병합하는 함수
    def concat_Series(self, *series):
        return pd.concat(series, axis=1)


# client = UMFutures()
# client.depth("BTCUSDT", **{"limit": 5})