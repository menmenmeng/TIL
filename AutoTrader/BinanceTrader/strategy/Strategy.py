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


# def get_MA(dataDf, window, CloseName='Close'):
#     return dataDf[CloseName].astype(np.float64).rolling(window).mean()

# def get_std(dataDf, window, CloseName='Close'):
#     return dataDf[CloseName].astype(np.float64).rolling(window).std()


class Strategy():
    def __init__(self, using_indices=4):
        # How many data will you use?
        self.using_indices = using_indices

        # save your conditions.
        self.long_conditions = []
        self.short_conditions = []
        self.clear_conditions = []

        # more deeper (not essential)
        ## take Profit conditions
        self.takeProfit_long_conditions = []
        self.takeProfit_short_conditions = []
        ## stop Loss conditions
        self.stopLoss_long_conditions = []
        self.stopLoss_short_conditions = []

        # Moving Average lists
        self.ma = dict()
        
        # StdDev lists
        self.std = dict()

    # methods for making indicators.
    def get_MA(self, window, closePrice):
        indicator = closePrice.astype(np.float64).rolling(window).mean()
        self.ma[f'MA{window}'] = indicator
        return indicator

    def get_std(self, window, closePrice):
        indicator = closePrice.astype(np.float64).rolling(window).std()
        self.std[f'std{window}'] = indicator
        return indicator

    # 어떻게 만들지 이건....
    def get_own_indicator(self, **kwargs):
        window = kwargs['window']
        closePrice = kwargs['closePrice']
        volume = kwargs['volume']

    def add_condition(self, LSC, index):
        # if index exceeded using_indices, add index automatically.
        if index>=self.using_indices:
            print("index modified.")
            self.using_indices = index
        
        if LSC=='long':
            condition = None
            self.long_conditions.append(condition)
        elif LSC=='short':
            condition = None
            self.short_conditions.append(condition)
        elif LSC=='clear':
            condition = None
            self.clear_conditions.append(condition)
        
    
