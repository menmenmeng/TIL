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

# my own library
from backTester.BackTester import BackTester
from backTester.GenBackData import BackData
from strategyArchive.StrategyArchive import StrategyArchive

# visualization
import matplotlib.pyplot as plt
import seaborn as sns


# data loading
backdata = pd.read_pickle('C:\\TIL\\AutoTrader\\BinanceTrader\\backdata.pkl')

# data loading : for real
'''
# data loading
client = UMFutures()
# backdata 가져오기 (간격 : 5m)
# 2022-08-21 18:30:00 ~ 2022-10-09 09:25:00
first_openTime = 1665156600000 # 2022, 10, 8, 0, 30
df1 = BackData().get_backdata(client, '5m', startTime=first_openTime, limit=1500)
df2 = BackData().get_backdata(client, '5m', startTime=first_openTime-5*1500*60*1000, limit=1500)
df3 = BackData().get_backdata(client, '5m', startTime=first_openTime-2*5*1500*60*1000, limit=1500)
df4 = BackData().get_backdata(client, '5m', startTime=first_openTime-3*5*1500*60*1000, limit=1500)
df5 = BackData().get_backdata(client, '5m', startTime=first_openTime-4*5*1500*60*1000, limit=1500)
df6 = BackData().get_backdata(client, '5m', startTime=first_openTime-5*5*1500*60*1000, limit=1500)
df7 = BackData().get_backdata(client, '5m', startTime=first_openTime-6*5*1500*60*1000, limit=1500)
df8 = BackData().get_backdata(client, '5m', startTime=first_openTime-7*5*1500*60*1000, limit=1500)
df9 = BackData().get_backdata(client, '5m', startTime=first_openTime-8*5*1500*60*1000, limit=1500)
df10 = BackData().get_backdata(client, '5m', startTime=first_openTime-9*5*1500*60*1000, limit=1500)

backdata = pd.concat([df10, df9, df8, df7, df6, df5, df4, df3, df2, df1], axis=0)
backdata.reset_index(inplace=True, drop=True)
'''

# build Strategy
tester = BackTester()

backdata['MA1'] = tester.get_MA(10, backdata['Close'])
backdata['MA2'] = tester.get_MA(30, backdata['Close'])

myStrg = StrategyArchive(3, 0) # i-4, i-3, i-2, i-1, i

myStrg.add_andCondition('MA1', 'MA2', '<', 3)
myStrg.add_andCondition('MA1', 'MA2', '>', 2, func1=lambda x:x*0.9999)
myStrg.add_andCondition('MA1', 'MA2', '>', 1, func1=lambda x:x*0.9998)
myStrg.add_andCondition('MA1', 'MA2', '>', 0, func1=lambda x:x*0.9997)
myStrg.add_condition('long')

myStrg.add_andCondition('MA1', 'MA2', '>', 3)
myStrg.add_andCondition('MA1', 'MA2', '<', 2, func1=lambda x:x*1.0001)
myStrg.add_andCondition('MA1', 'MA2', '<', 1, func1=lambda x:x*1.0002)
myStrg.add_andCondition('MA1', 'MA2', '<', 0, func1=lambda x:x*1.0003)
myStrg.add_condition('short')

myStrg.add_andCondition('MA1', 'MA2', '<', 3)
myStrg.add_andCondition('MA1', 'MA2', '>', 2, func1=lambda x:x*0.9999)
myStrg.add_andCondition('MA1', 'MA2', '>', 1, func1=lambda x:x*0.9998)
myStrg.add_andCondition('MA1', 'MA2', '>', 0, func1=lambda x:x*0.9997)
myStrg.add_andCondition('_short_amount', 0, '>', 0)
myStrg.add_condition('clear')

myStrg.add_andCondition('MA1', 'MA2', '>', 3)
myStrg.add_andCondition('MA1', 'MA2', '<', 2, func1=lambda x:x*1.0001)
myStrg.add_andCondition('MA1', 'MA2', '<', 1, func1=lambda x:x*1.0002)
myStrg.add_andCondition('MA1', 'MA2', '<', 0, func1=lambda x:x*1.0003)
myStrg.add_andCondition('_long_amount', 0, '>', 0)
myStrg.add_condition('clear')

# backtest
tester.backtest_tmp(myStrg, backdata)