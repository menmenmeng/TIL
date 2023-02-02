import numpy as np
import pandas as pd
from datetime import datetime
from binance.error import ClientError
from cert.myfuncs import *

endTime_datetime = datetime.now()
endTime = endTime_datetime.timestamp()*1000
endTime_sec = int(endTime_datetime.timestamp())*1000

class DataPrelim():
    def __init__(self, UMclient):
        self.client = UMclient
        self.symbol = "BTCUSDT"
        self.pre_kline = None
        self.pre_rvs = None


    def new_listenKey(self):
        listenKey = self.client.new_listen_key()["listenKey"]
        return listenKey


    def get_account(self):
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
    

    def prelim_kline(self, interval, limit):
        json_kline = self.client.klines(self.symbol, interval, limit=limit)

        columns = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'NumOfTrades',
                'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore']

        df_kline = pd.DataFrame(json_kline, columns=columns)
        df_kline['OpenTime'] = df_kline['OpenTime'].astype("datetime64[ms]")
        df_kline['CloseTime'] = df_kline['CloseTime'].astype("datetime64[ms]")
        df_kline[['Open', 'High', 'Low', 'Close', 'Volume', 'QuoteAssetVolume', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume']] = df_kline[['Open', 'High', 'Low', 'Close', 'Volume', 'QuoteAssetVolume', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume']].astype('float64')
        df_kline.drop(['Ignore'], axis=1, inplace=True)

        self.pre_kline = df_kline
        return df_kline


    def prelim_volatility(self, window):
        sr_kline_close = self.pre_kline['Close']
        rvs = log_return(sr_kline_close).rolling(window=window).apply(realized_volatility)

        self.pre_rvs = rvs
        return rvs

