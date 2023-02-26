import time
import numpy as np
import pandas as pd
from datetime import datetime
from binance.error import ClientError
from cert.myfuncs import *
from cert.myvars import logFile_base

endTime_datetime = datetime.now()
endTime = endTime_datetime.timestamp()*1000
endTime_sec = int(endTime_datetime.timestamp())*1000

class Prelim(): # REST API를 이용해서 할 수 있는 것들을 다 하는 곳. + 실시간 트레이더가 진행되기 전, 필요한 것들을 제공하는 함수까지
    def __init__(self, UMclient):
        self.client = UMclient
        self.symbol = "BTCUSDT"
        self.pre_kline = None
        self.pre_rvs = None
        self.listenKey = None

        now = datetime.now()
        nowMin = now.year, now.month, now.day, now.hour, now.minute-1
        self.endTime = dt2ms(*nowMin)

    '''
    <xxx_listenKey methods>
    - get new listenKey, or renew, close listenKey.

    <getData_XXX methods>
    - get data, which is not used as input of other Classes. Just for check data or backtest strategy.

    <getInfo_XXX methods>
    - get data, which is used as input of other Classes, like Prelim, Collector, Trader.
    '''

    def new_listenKey(self):
        listenKey = self.client.new_listen_key()["listenKey"]
        self.listenKey = listenKey
        return listenKey

    def close_listenKey(self):
        print(self.client.close_listen_key(self.listenKey))

    def renew_listenKey(self):
        print(self.client.renew_listen_key(self.listenKey))



    def getData_account(self):
        try:
            response = self.client.account(recvWindow=6000)
            assets = response["assets"]
            positions = response["positions"]

            for asset_info in assets:
                if asset_info["asset"]=="USDT":
                    asset_USDT = asset_info
            
            for position_info in positions:
                if position_info["symbol"]=="BTCUSDT":
                    position_BTCUSDT = position_info

            return asset_USDT, position_BTCUSDT

        except ClientError as error:
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
    '''
    ## 중요.
    getData_recentOHLCV와 getData_OHLCV가 거의 동일한 함수이므로, 이거를 통합할 생각을 해보자.
    '''
    def getData_OHLCV(self, interval, **kwargs):

        try:
            startTime = kwargs['startTime']
            endTime = kwargs['endTime']
        except:
            startTime = None
            endTime = None

        try:
            limit = kwargs['limit']
        except:
            limit = None


        print("OHLCV loading...")

        if startTime and endTime and limit:
            json_kline = self.client.klines(self.symbol, interval, startTime=startTime, endTime=endTime, limit=limit)
        elif not limit:
            json_kline = self.client.klines(self.symbol, interval, startTime=startTime, endTime=endTime)
        elif (not startTime) and (not endTime) and limit:
            if limit > 1500:
                print("limit should be under 1500. get_OHLCV function is not triggered.")
                return None
            else:
                json_kline = self.client.klines(self.symbol, interval, limit=limit)
        else:
            print("function got invalid parameters. get_OHLCV function is not triggered.")
            return None


        wss_columns = [
            'stream',
            'eventType',
            'eventTime',
            'startTime',
            'closeTime',
            'interval',
            'open',
            'high',
            'low',
            'close',
            'volume',
        ]

        rest_columns = [
            'OpenTime', 
            'Open', 
            'High', 
            'Low', 
            'Close', 
            'Volume', 
            'CloseTime', 
            'QuoteAssetVolume', 
            'NumOfTrades',
            'TakerBuyBaseAssetVolume', 
            'TakerBuyQuoteAssetVolume', 
            'Ignore'
        ]

        rename_columns = {
            "OpenTime":"startTime",
            "Open":"open",
            "High":"high",
            "Low":"low",
            "Close":"close",
            "Volume":"volume",
            "CloseTime":"closeTime"
        }

        df_kline = pd.DataFrame(json_kline, columns=rest_columns)
        df_kline['stream'] = f"kline{interval}"
        df_kline['eventType'] = "kline"
        df_kline['eventTime'] = int(time.time()*1000)
        df_kline['interval'] = interval
        df_kline.rename(columns=rename_columns, inplace=True)

        df_kline['startTime'] = df_kline['startTime'].astype(np.int64)
        df_kline['closeTime'] = df_kline['closeTime'].astype(np.int64)
        df_kline['open'] = df_kline['open'].astype(float)
        df_kline['high'] = df_kline['high'].astype(float)
        df_kline['low'] = df_kline['low'].astype(float)
        df_kline['close'] = df_kline['close'].astype(float)
        df_kline['volume'] = df_kline['volume'].astype(float)
        
        df_kline = df_kline[wss_columns]

        self.pre_kline = df_kline

        # for debugging.
        print("lastKline shape:", df_kline.shape)
        return df_kline


    def getData_rv(self, window):
        pre_kline = self.getData_OHLCV('1m', 480)
        sr_kline_close = pre_kline['Close'].astype(float)
        rvs = log_return(sr_kline_close).rolling(window=window).apply(realized_volatility)

        self.pre_rvs = rvs
        return rvs


    def getInfo_account(self, verbose=False): # information needed for realtime Trading.
        asset_USDT, position_BTCUSDT = self.getData_account()
        walletBalance, currentAsset = float(asset_USDT['walletBalance']), float(asset_USDT['availableBalance'])
        positionAmt, entryPrice = float(position_BTCUSDT['positionAmt']), float(position_BTCUSDT['entryPrice'])
        if verbose:
            print("- wallet balance           : ", walletBalance)
            print("- available balance        : ", currentAsset)
            print("- current position Amount  : ", positionAmt)
            print("- entry Price              : ", entryPrice)
        return walletBalance, currentAsset, positionAmt, entryPrice


    def getInfo_streams(self, streamSymbol, *streamKeys):
        '''
        Auto-generate streamValues(like "btcusdt@markPrice@1s") with streamKeys, and return streamDict.
        You can use this return dictionary as input of Trader instance.
        Must receive valid parameters, and valid parameters are presented below.

        - valid parameter form.
            streamSymbol = "btcusdt" (must be lowercase)
            streamKeys = [
                "markPrice1s",
                "aggTrade",
                "userData",
                ...
            ]

        - markPrice should have interval information at the last of key string. (1s or 3s)

        - available streamKeys list. (will be updated.)
          - "markPrice1s"   : "<symbol>@markPrice@1s"
          - "markPrice3s"   : "<symbol>@markPrice@3s"
          - "aggTrade"      : "<symbol>@aggTrade"
          - "userData"      : "<listenKey>"     (<listenKey> will be auto-generated by self.new_listenKey().)

        '''
        streamDict = dict()
        for key in streamKeys:
            if key == "markPrice1s":
                streamDict[key] = streamSymbol + "@markPrice@1s"
            elif key == "markPrice3s":
                streamDict[key] = streamSymbol + "@markPrice@3s"

            elif key == "kline1m":
                streamDict[key] = streamSymbol + "@kline_1m"
            elif key == "kline3m":
                streamDict[key] = streamSymbol + "@kline_3m"
            elif key == "kline5m":
                streamDict[key] = streamSymbol + "@kline_5m"
            elif key == "kline15m":
                streamDict[key] = streamSymbol + "@kline_15m"
            elif key == "kline30m":
                streamDict[key] = streamSymbol + "@kline_30m"

            elif key == "aggTrade":
                streamDict[key] = streamSymbol + "@aggTrade"
            elif key == "userData":
                if self.listenKey :
                    streamDict[key] = self.listenKey
                else:
                    self.new_listenKey()
                    streamDict[key] = self.listenKey
        print(streamDict) # for debugg.
        return streamDict


    def getInfo_trade(self, streamSymbol, *streamKeys): ## send to trader.
        walletBalance, currentAsset, positionAmt, entryPrice = self.getInfo_account()
        streamDict = self.getInfo_streams(streamSymbol, *streamKeys)
        return walletBalance, currentAsset, positionAmt, entryPrice, streamDict