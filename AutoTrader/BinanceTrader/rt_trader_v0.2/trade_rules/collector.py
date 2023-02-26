import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from datetime import datetime
from cert.myvars import logFile_base


class Collector():
    '''
    Get raw message from websocket connection, and transform it to pd.DataFrame and return it.
    '''
    def __init__(self, **streamDict):
        self.streamDict = streamDict
        self.streamDict_inverse = {v: k for k, v in streamDict.items()}

        self.rowDict = None
        self.rowDF = None
        self.DataFrame = None
        

    def getEventType(self, message):
        '''
        Assume that live websocket client has multiple streams.
        Assume that markPrice stream and listenKey stream are always included.

        - messages have "stream" key and the value of "stream" key are like :
            - "btcusdt@markPrice@1s"
            - "btcusdt@aggTrade"
            - "<listenKey>"
            - ... else.
        - messages have "data" key, and in "data" value, there is "e" key which has the information of Event Type. The value of event type are like:
            - "markPriceUpdate"
            - "aggTrade"
            - "ORDER_TRADE_UPDATE"
            - "ACCOUNT_UPDATE"
            - ...

        - streamKey example
            - "markPrice1s"
            - "markPrice3s"
            - "aggTrade"
            - "userData"
            - ...
        - eventType example
            - same as message['data']['e']
        '''

        try:
            streamValue = message['stream']
            streamKey = self.streamDict_inverse[streamValue]
            eventType = message['data']['e']
        except:
            print("message : \n", message)
            streamKey = None
            eventType = None

        return streamKey, eventType


    def getDataFrame(self, message):
        '''
        This method should be executed in Final callback function.
        Every time websocket receives message, collector instances will update their <self.DataFrame>.
        After execute this, <self.DataFrame> should be saved into some other variable outside instance.
        '''

        row_dict = self.getRowDictFromMessage(message)
        row_df = pd.DataFrame(row_dict, index=[0])
        # print(row_df) # only for kline..
        self.DataFrame = pd.concat([self.DataFrame, row_df], axis=0)
        self.DataFrame.reset_index(drop=True, inplace=True)
        self.cutDataFrame(100)
        return self.DataFrame
 

    def getRowDictFromMessage(self, message):
        '''
        Transform message to row_dict and return row_dict.
        Every Collector should implement this method.
        row_dict will be used in <self.getDataFrame> method.
        '''

        raise NotImplementedError


    def cutDataFrame(self, cutthr):
        try:
            rowNum = self.DataFrame.shape[0]
        except:
            rowNum = 0
        if rowNum > cutthr:
            self.DataFrame = self.DataFrame[-cutthr:]
            self.DataFrame.reset_index(drop=True, inplace=True)


class MarkPriceCollector(Collector):
    def __init__(self, **streamDict):
        super().__init__(**streamDict)
        self.eventTime = 0
        self.currentPrice = 0
        self.startTime = None


    def getRowDictFromMessage(self, message):
        streamKey, eventType = self.getEventType(message)
        data = message['data']

        row_dict = dict(
            stream = streamKey,
            eventType = eventType,

            eventTime = data['E'],
            markPrice = float(data['p']),
            indexPrice = float(data['i']),
        )
        
        self.eventTime = data['E']
        self.currentPrice = float(data['p'])
        return row_dict



class __KlineCollector(Collector):
    def __init__(self, lastKlines, **streamDict):
        super().__init__(**streamDict)
        self.eventTime = 0
        self.open = 0
        self.close = 0
        self.high = 0
        self.low = 0
        self.volume = 0

        self.startTime = None
        self._former_row = None
        self._current_row = None
        self.DataFrame = lastKlines


    def getDataFrame(self, message):
        '''
        This method should be executed in Final callback function.
        Every time websocket receives message, collector instances will update their <self.DataFrame>.
        After execute this, <self.DataFrame> should be saved into some other variable outside instance.
        '''

        row_dict = self.getRowDictFromMessage(message)
        if row_dict == None:
            return self.DataFrame
        else:
            row_df = pd.DataFrame(row_dict, index=[0])
            self.DataFrame = pd.concat([self.DataFrame, row_df], axis=0)
            self.DataFrame.reset_index(drop=True, inplace=True)
            print("Kline updated.")
            print(self.DataFrame)
            return self.DataFrame


    def getRowDictFromMessage(self, message):
        streamKey, eventType = self.getEventType(message)
        data = message['data']
        kline = data['k']

        row_dict = dict(
            stream = streamKey,
            eventType = eventType,

            eventTime = int(data['E']),
            startTime = int(kline['t']),
            closeTime = int(kline['T']),
            interval = str(kline['i']),
            open = float(kline['o']),
            high = float(kline['h']),
            low = float(kline['l']),
            close = float(kline['c']),
            volume = float(kline['v'])
        )

        self.eventTime = row_dict['eventTime']
        self.open = row_dict['open']
        self.high = row_dict['high']
        self.low = row_dict['low']
        self.close = row_dict['close']
        self.volume = row_dict['volume']

        self._former_row = self._current_row
        self._current_row = row_dict

        if self._former_row == None:
            return

        if self._former_row['startTime'] == self._current_row['startTime']:
            return self._former_row

        else:
            return self._former_row



class RealTimeKlineCollector(Collector):
    def __init__(self, **streamDict):
        super().__init__(**streamDict)
        self.closeTime = 0
        self.open = 0
        self.close = 0
        self.high = 0
        self.low = 0
        self.volume = 0

    def getRowDictFromMessage(self, message):
        streamKey, eventType = self.getEventType(message)
        data = message['data']
        kline = data['k']

        row_dict = dict(
            stream = streamKey,
            eventType = eventType,

            eventTime = int(data['E']),
            startTime = int(kline['t']),
            closeTime = int(kline['T']),
            interval = str(kline['i']),
            open = float(kline['o']),
            high = float(kline['h']),
            low = float(kline['l']),
            close = float(kline['c']),
            volume = float(kline['v'])
        )


        self.closeTime = int(kline['t'])
        self.open = float(kline['o'])
        self.close = float(kline['c'])
        self.high = float(kline['h'])
        self.low = float(kline['l'])
        self.volume = float(kline['v'])

        print(row_dict.values())
        return row_dict



class KlineCollector(RealTimeKlineCollector):
    def __init__(self, lastKlines, **streamDict):
        super().__init__(**streamDict)
        self.DataFrame = lastKlines


    def getDataFrame(self, message):
        '''
        This method should be executed in Final callback function.
        Every time websocket receives message, collector instances will update their <self.DataFrame>.
        After execute this, <self.DataFrame> should be saved into some other variable outside instance.
        '''

        row_dict = self.getRowDictFromMessage(message)
        row_df = pd.DataFrame(row_dict, index=[0])
        # print(row_df) # only for kline..
        if int(row_df[0:]['startTime']) == int(self.DataFrame[-1:]['startTime']):
            self.DataFrame[-1:] = row_df
        else:
            self.DataFrame = pd.concat([self.DataFrame, row_df], axis=0)
            print("kline updated.")
            print(self.DataFrame) # This code prints dataframe which didnt reset index yet. Do not hesitate.

        self.DataFrame.reset_index(drop=True, inplace=True)

        self.cutDataFrame(100)
        return self.DataFrame



class OrderUpdateCollector(Collector):
    def __init__(self, **streamDict):
        super().__init__(**streamDict)


    def getRowDictFromMessage(self, message):
        streamKey, eventType = self.getEventType(message)
        data = message['data']
        orderData = data['o']
        self.realizedProfit = 0

        '''
        Not mandatory params by condition.
        '''
        try:
            N = orderData['N']
        except:
            N = None

        try:
            n = float(orderData['n'])
        except:
            n = None

        try:
            cp = orderData['cp']
        except:
            cp = None

        try:
            AP = float(orderData['AP'])
        except:
            AP = None

        try:
            cr = float(orderData['cr'])
        except:
            cr = None
        '''
        Not mandatory params by condition END.
        '''

        row_dict = dict(
            stream = streamKey,
            eventType = eventType,

            eventTime = data['E'],
            symbol = orderData['s'],
            side = orderData['S'],
            orderType = orderData['o'],
            originQuantity = float(orderData['q']),
            originPrice = float(orderData['p']),
            averagePrice = float(orderData['ap']),
            stopPrice = float(orderData['sp']),
            execType = orderData['x'],
            orderStatus = orderData['X'],
            orderLastFilledQuantity = float(orderData['i']),
            commisionAsset = N,
            commision = n,
            stopPriceWorkingType = orderData['wt'],
            originOrderType = orderData['ot'],
            position = orderData['ps'],
            isCloseAll = cp,
            activationPrice = AP,
            callbackRate = cr,
            realizedProfit = float(orderData['rp']),
        )
        today = datetime.now().strftime('%y%m%d')
        now = datetime.now().strftime('%H:%M:%S')
        with open(f'{logFile_base}OrderUpdate_{today}.txt', 'a') as f:
            string = str(now) + str(row_dict) + '\n'
            f.write(string)

        self.realizedProfit += float(orderData['rp'])
        return row_dict



class AccountUpdateCollector(Collector):
    def __init__(self, current_asset, **streamDict):
        super().__init__(**streamDict)
        self.currentAmt = 0
        self.entryPrice = 0
        self.currentAsset = current_asset
        self.balanceChange = 0
        self.eventTime = int(time.time()*1000)


    def _getDataFromMessage(self, message):
        '''
        Account Update message has too many keys and values.
        This concealed method will help user to transform message to row_dict more easily.

        If someone wants to use balance_BUSD, position_LONG, position_SHORT,
        modify return values of this method and 3rd line of method <self.getRowDictFromMessage>.
        '''

        for data in message['data']['a']['B']:
            if data['a']=='USDT':
                balance_USDT = data
            elif data['a']=='BUSD':
                balance_BUSD = data
        
        for data in message['data']['a']['P']:
            if data['s']=='BTCUSDT' and data['ps']=='BOTH':
                position_BOTH = data
            elif data['s']=='BTCUSDT' and data['ps']=='LONG':
                position_LONG = data
            elif data['s']=='BTCUSDT' and data['ps']=='SHORT':
                position_SHORT = data
        
        return balance_USDT, position_BOTH


    def getRowDictFromMessage(self, message):
        streamKey, eventType = self.getEventType(message)
        data = message['data']
        balance_USDT, position_BOTH = self._getDataFromMessage(message)

        row_dict = dict(
            stream = streamKey,
            eventType = eventType,

            eventTime = data['E'],
            currentAsset = float(balance_USDT['wb']),
            balanceChange = float(balance_USDT['bc']),

            symbol = position_BOTH['s'],
            positionAmt = float(position_BOTH['pa']),
            entryPrice = float(position_BOTH['ep']),
            unrealizedPnL = float(position_BOTH['up']),
            positionSide = position_BOTH['ps'],
        )

        self.eventTime = int(data['E'])
        self.balanceChange += float(balance_USDT['bc'])
        self.currentAmt = float(position_BOTH['pa'])
        self.entryPrice = float(position_BOTH['ep'])
        self.currentAsset = float(balance_USDT['wb'])

        ####
        today = datetime.now().strftime('%y%m%d')
        now = datetime.now().strftime('%H:%M:%S')
        with open(f'{logFile_base}AccountUpdate_{today}.txt', 'a') as f:
            string = str(now) + str(row_dict) + '\n'
            f.write(string)

        return row_dict