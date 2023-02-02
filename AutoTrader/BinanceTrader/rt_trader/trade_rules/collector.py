import numpy as np
import pandas as pd


class Collector():
    '''
    Get raw message from websocket connection, and transform it to pd.DataFrame and return it.
    '''
    def __init__(self, **streamDict):
        self.streamDict = streamDict
        self.streamDict_inverse = {v: k for k, v in streamDict}

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
        self.DataFrame = pd.concat([self.DataFrame, row_df], axis=0)
        self.DataFrame.reset_index(drop=True, inplace=True)
        return self.DataFrame
 

    def getRowDictFromMessage(self, message):
        '''
        Transform message to row_dict and return row_dict.
        Every Collector should implement this method.
        row_dict will be used in <self.getDataFrame> method.
        '''

        raise NotImplementedError



class MarkPriceCollector(Collector):
    def __init__(self, **streamDict):
        super().__init__(**streamDict)
        self.currentPrice = 0


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

        self.currentPrice = float(data['p'])
        return row_dict



class OrderUpdateCollector(Collector):
    def __init__(self, **streamDict):
        super().__init__(**streamDict)


    def getRowDictFromMessage(self, message):
        streamKey, eventType = self.getEventType(message)
        data = message['data']
        orderData = data['o']

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
            orderLastFilledQ = float(orderData['i']),
            commisionAsset = orderData['N'],
            commision = float(orderData['n']),
            stopPriceWorkingType = orderData['wt'],
            originOrderType = orderData['ot'],
            position = orderData['ps'],
            isCloseAll = orderData['cp'],
            activationPrice = float(orderData['AP']),
            callbackRate = float(orderData['cr']),
            realizedProfit = float(orderData['rp']),
        )
        
        return row_dict



class AccountUpdateCollector(Collector):
    def __init__(self, current_asset, **streamDict):
        super().__init__(**streamDict)
        self.currentAmt = 0
        self.entryPrice = 0
        self.currentAsset = current_asset


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

        self.currentAmt = float(position_BOTH['pa'])
        self.entryPrice = float(position_BOTH['ep'])
        self.currentAsset = float(balance_USDT['wb'])
        return row_dict