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

class BackTester():
    def __init__(self, asset=1000, maxLimit=1000): # default asset : 1000 dollars
        # vars for long position
        self.long_amount = 0
        self.long_meanPrice = 0
        self.long_flag = False
        # vars for short position
        self.short_amount = 0
        self.short_meanPrice = 0
        self.short_flag = False
        # vars for base asset
        self.asset = asset
        self.PRINCIPAL = asset # constant
        self.maxLimit = maxLimit
        # var for busted (when did you bust?)
        self.bustedIndex = 0

    def _get_tradeAmount(self, tradePrice):
        tradeAmount = round(self.maxLimit/tradePrice/2, 4)
        return tradeAmount

    def set_long(self, tradePrice):
        tradeAmount = self._get_tradeAmount(tradePrice)
        self.maxLimit -= tradeAmount * tradePrice
        self.long_meanPrice = (self.long_meanPrice*self.long_amount + tradePrice*tradeAmount)/(self.long_amount + tradeAmount) # 이거 맞아?
        self.long_amount += tradeAmount
        self.long_flag = True
        return

    def set_short(self, tradePrice):
        tradeAmount = self._get_tradeAmount(tradePrice)
        self.maxLimit -= tradeAmount * tradePrice
        self.short_meanPrice = (self.short_meanPrice*self.short_amount + tradePrice*tradeAmount)/(self.short_amount + tradeAmount)
        self.short_amount += tradeAmount
        self.short_flag = True
        return

    def set_clear(self, tradePrice):
        self.asset -= self.short_amount * (tradePrice - self.short_meanPrice)
        self.asset += self.long_amount * (tradePrice - self.long_meanPrice)
        self.short_amount = self.long_amount = self.short_meanPrice = self.long_meanPrice = 0
        self.long_flag = self.short_flag = False
        self.maxLimit = self.asset
        return

    def check_asset_positive(self, tradePrice):
        tmpAsset = self.asset - (self.short_amount * (tradePrice - self.short_meanPrice))
        tmpAsset = self.asset + (self.long_amount * (tradePrice - self.long_meanPrice))
        if tmpAsset < 0:
            return False
        else:
            return True

    def get_log(self, index, stateTxt):
        print(f'#########################')
        print(f'## index {index}, {stateTxt}')
        print(f'#########################')

        if stateTxt != 'Busted':
            print(f'long amount:{self.long_amount}')
            print(f'long meanPrice:{self.long_meanPrice}')
            print(f'short amount:{self.short_amount}')
            print(f'short meanPrice:{self.short_meanPrice}')
            print(f'asset:{self.asset}')
            print(f'maxLimit:{self.maxLimit}')
            self.bustedIndex = index

    def get_current_return(self, index):
        print(f'**current return : {self.asset/self.PRINCIPAL*100}%')
        return self.asset / self.PRINCIPAL

    def get_commission(self):
        pass