import numpy as np
import pandas as pd

listenKey = '!! listenKey should be imported. '

class UserStreamData():
    def __init__(self, listenKey, current_asset): # listenKey, current_Asset should be updated by another function.
        self.listenKey = listenKey
        self.current_asset = current_asset


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


    def user_data_processor(self, message):
        if message['e'] == "ORDER_TRADE_UPDATE":
            return self.check_order_update(message)

        elif message['e'] == "ACCOUNT_UPDATE":
            return self.check_loss_profit(message)