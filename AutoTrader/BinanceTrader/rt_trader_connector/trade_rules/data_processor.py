import numpy as np
import pandas as pd
import pprint

class DataCollector():
    def __init__(self, current_asset, listenKey, **streams):
        self.current_asset = current_asset
        self.listenKey = listenKey
        self.streams = streams
        self.df_store = dict() # keys : markPriceUpdate, aggTrade, ...
        self.df_cut_th = {
            'aggTrade':400,
            'markPrice':1000,
            'kline':1000,
        }

        self.current_amt = 0
        self.entry_price = None


    def _only_user_stream(self):
        return not bool(self.streams)

    def _message_handler(self, message):
        # print('message type:', type(message)) # dictionary.
        print("# message : ")
        print(message)

    '''
    def _user_data_message_handler(self, message):
        self._user_data_processor(message)
        profit, profit_ratio, profit_wo_extraFee = self._user_data_check_loss_profit(message)
        print("# message : ", message)
        # pprint(message)
        print("## profit : \t", profit)
        print("## prof_ratio : \t", profit_ratio)
        print("## prof_woFee : \t", profit_wo_extraFee)
    '''

    def data_stream_proc(self, message):    
        stream_has_only_user_data = self._only_user_stream()

        try:
            _ = message['e']
        except:
            try:
                _ = message['data']['e']
            except:
                return
            
        if stream_has_only_user_data:       # only user data stream.
            eventType = message['e']
            event = message
            streamType = "USER_DATA"
        else:                               # multiple streams.
            eventType = message['data']['e']
            event = message['data']
            streamType = message['stream']
            if streamType==self.listenKey:
                streamType = "USER_DATA"

        if streamType=="USER_DATA":
            print(message)
            if eventType=="ACCOUNT_UPDATE":
                self._check_account_update(message)

        self.data_df_update(streamType, eventType, event)

                
    def data_df_update(self, streamType, eventType, event):

        try:                # check original dataframe
            df_data = self.df_store[eventType]
        except:
            df_data = pd.DataFrame()

        one_event_df = pd.DataFrame(event, index=[0])
        concat_df = pd.concat([df_data, one_event_df], axis=0)
        concat_df['streamType'] = streamType
        concat_df.reset_index(drop=True, inplace=True)

        try:                # check whether the dataframe is too long
            concat_df = concat_df[len(concat_df)-self.cut_th[eventType]:]
        except:
            pass
        
        self.df_store[eventType] = concat_df


    def _check_account_update(self, message):
        for data in message['a']['B']:
            if data['a']=='USDT':
                balance_USDT = data
            elif data['a']=='BUSD':
                balance_BUSD = data
        
        for data in message['a']['P']:
            if data['s']=='BTCUSDT' and data['ps']=='BOTH':
                position_BOTH = data
            elif data['s']=='BTCUSDT' and data['ps']=='LONG':
                position_LONG = data
            elif data['s']=='BTCUSDT' and data['ps']=='SHORT':
                position_SHORT = data
        
        self.current_amt = float(position_BOTH['pa'])
        self.entry_price = float(position_BOTH['ep'])
        
        return balance_USDT, position_BOTH

        # for One-way mode.
        # profit = self.current_asset - balance_USDT['wb']
        # profit_ratio = profit/balance_USDT['wb']
        # profit_wo_extraFee = balance_USDT['bc']

        # self.current_asset = balance_USDT['wb']
        # return profit, profit_ratio, profit_wo_extraFee

    '''
    def _user_data_check_order_update(self, message):
        eventTime = message['E']
        transactionTime = message['T']
        data = message['o']
        return eventTime, transactionTime, data

    def _user_data_processor(self, message):
        if message['e'] == "ORDER_TRADE_UPDATE":
            return self._user_data_check_order_update(message)

        elif message['e'] == "ACCOUNT_UPDATE":
            return self._user_data_check_loss_profit(message)

class UserStreamData():
    def __init__(self, listenKey, current_asset): # listenKey, current_Asset should be updated by another function.



    def check_loss_profit(self, message):
        for data in message['a']['B']:
            if data['a']=='USDT':
                balance_USDT = data
            elif data['a']=='BUSD':
                balance_BUSD = data
        
        for data in message['a']['P']:
            if data['s']=='BTCUSDT' and data['ps']=='BOTH':
                position_BOTH = data
            elif data['s']=='BTCUSDT' and data['ps']=='LONG':
                position_LONG = data
            elif data['s']=='BTCUSDT' and data['ps']=='SHORT':
                position_SHORT = data

        # for One-way mode.
        profit = self.current_asset - balance_USDT['wb']
        profit_ratio = profit/balance_USDT['wb']
        profit_wo_extraFee = balance_USDT['bc']

        self.current_asset = balance_USDT['wb']
        return profit, profit_ratio, profit_wo_extraFee


    def check_order_update(self, message):
        eventTime = message['E']
        transactionTime = message['T']
        data = message['o']
        return eventTime, transactionTime, data


    def _user_data_processor(self, message):
        if message['e'] == "ORDER_TRADE_UPDATE":
            return self.check_order_update(message)

        elif message['e'] == "ACCOUNT_UPDATE":
            return self.check_loss_profit(message)
    '''