import numpy as np
import pandas as pd


# need to be modified.
class BackDataLoader():
    def __init__(self, symbol='BTCUSDT'):
        self.backdata = None
        self.symbol = symbol

    def get_backdata(self, umFuturesClient, interval, **others):
        self.client = umFuturesClient
        self.intervalNumber = int(interval[:-1]) # 1, 3, 5, 15, 30, 1h, ... 에서 숫자만 가져오기.
        self.intervalUnit = interval[-1]  # m, h 정도만 있으면 될 듯.
        
        startTime = others['startTime']

        try:
            limit = others['limit']
        except:
            pass

        try:
            endTime = others['endTime']
        except:
            pass

        columns = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'NumOfTrades',
                   'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore']

        # limit이 문제 없을 때.
        if limit and limit<=1500:
            kwargs = dict()
            kwargs['startTime'] = startTime
            kwargs['limit'] = limit
            df = self.get_data_chunk(interval, **kwargs)
            return df

        elif limit and limit>1500:
            df = pd.DataFrame()
            for chunk_id in range(limit//1500):
                if chunk_id < limit//1500-1:
                    loadLimit = 1500
                    tmp_df = self.get_data_chunk(interval, startTime=startTime, limit=loadLimit)

                    df = pd.concat([df, tmp_df], axis=0, ignore_index=True)
                    if self.intervalUnit == 'm':
                        startTime = int(startTime + self.intervalNumber*loadLimit*60*1000)
                    elif self.intervalUnit == 'h':
                        startTime = int(startTime + self.intervalNumber*loadLimit*60*60*1000)
                    
                else:
                    loadLimit = limit - (limit//1500)*1500
                    tmp_df = self.get_data_chunk(interval, startTime=startTime, limit=loadLimit)
                    df = pd.concat([df, tmp_df], axis=0, ignore_index=True)
            
            return df

        # elif endTime and endTime > startTime:
        #     timedelta = endTime - startTime
        #     if timedelta <= 

    
    # binance client Instance가 있어야 함.
    def get_data_chunk(self, interval, **kwargs): # symbol은 필요 없음, interval, startTime, endTime, limit만 있으면 된다.
        rawbackdata = self.client.klines(self.symbol, interval, **kwargs)
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