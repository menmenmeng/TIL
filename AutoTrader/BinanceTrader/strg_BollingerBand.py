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


# Do not change codes above.

# build Strategy
'''
볼린저 밴드 전략 : 볼린저 upperband, lowerband, 중간선, 75%선, 25%선을 만들어서
그거에 따라서 롱/숏 전략을 취한다.
'''
tester = BackTester()

window_MA = 20
window_ER = 10
backdata['MA'] = tester.get_MA(window_MA, backdata['Close'])
backdata['std'] = tester.get_std(window_MA, backdata['Close'])
backdata['UB'] = backdata['MA'] + 2 * backdata['std']
backdata['U75'] = backdata['MA'] + backdata['std']
backdata['LB'] = backdata['MA'] - 2 * backdata['std']
backdata['L25'] = backdata['MA'] - backdata['std']
backdata['ER'] = backdata['Close'].diff(window_ER).abs()/backdata['Close'].diff().abs().rolling(window_ER).sum()

backdata['ERmean'] = backdata['ER'].mean()*1.5

myStrg = StrategyArchive(19, 0) # i-4, i-3, i-2, i-1, i

'''
횡보장에서 Close가 LB를 터치했다가 되돌아 올 경우, 롱 포지션
Close가 MA를 터치하면, 청산(TakeProfit)
Close가 meanPrice * 97% 아래가 되면 청산(StopLoss)

횡보장에서 Close가 UB를 터치했다가 되돌아 올 경우, 숏 포지션
Close가 MA를 터치하면, 청산(TakeProfit)
Close가 meanPrice * 103% 위가 되면 청산(StopLoss)

횡보장인지 아닌지는 어떻게 판단하는가?
Kaufman의 Efficiency ratio: 절대값(현재가-n일 전 종가)/최근 n일간 합(절대값(종가-전일종가)) 가 작고
거래량이 작을 때, 횡보한다고 말하기로.


'''

myStrg.add_andCondition('Close', 'LB', '>', list(range(10, 15)))
myStrg.add_andCondition('Close', 'LB', '<', list(range(3, 8)))
myStrg.add_andCondition('Volume', 25000, '<', list(range(10, 20)))
myStrg.add_andCondition('ER', 'ERmean', '<', list(range(10, 20)))
myStrg.add_Condition('long')

myStrg.add_andCondition('Close', 'UB', '<', list(range(10, 15)))
myStrg.add_andCondition('Close', 'UB', '>', list(range(3, 8)))
myStrg.add_andCondition('Volume', 25000, '>', list(range(10, 20)))
myStrg.add_andCondition('ER', 'ERmean', '>', list(range(10, 20)))
myStrg.add_Condition('short')

myStrg.add_andCondition('Close', 'MA', '<', 5)
myStrg.add_andCondition('Close', 'MA', '>', 2)
myStrg.add_andCondition('_long_flag', True, '==', 0)
myStrg.add_Condition('clear')

myStrg.add_andCondition('Close', '_long_meanPrice', '<', 0, func2=lambda x:x*0.97)
myStrg.add_andCondition('_long_flag', True, '==', 0)
myStrg.add_Condition('clear')

myStrg.add_andCondition('Close', 'MA', '>', 5)
myStrg.add_andCondition('Close', 'MA', '<', 2)
myStrg.add_andCondition('_short_flag', True, '==', 0)
myStrg.add_Condition('clear')

myStrg.add_andCondition('Close', '_short_meanPrice', '>', 0, func2=lambda x:x*1.03)
myStrg.add_andCondition('_short_flag', True, '==', 0)
myStrg.add_Condition('clear')

# backtest
tester.backtest_tmp(myStrg, backdata)