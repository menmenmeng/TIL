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


myStrg.add_andCondition('Close', 'LB', '>', list(range(10, 15)))
myStrg.add_andCondition('Close', 'LB', '<', list(range(3, 8)))
myStrg.add_andCondition('Volume', 25000, '<', list(range(10, 20)))
myStrg.add_andCondition('ER', 'ERmean', '<', list(range(10, 20)))
myStrg.add_condition('long')

myStrg.add_andCondition('Close', 'UB', '<', list(range(10, 15)))
myStrg.add_andCondition('Close', 'UB', '>', list(range(3, 8)))
myStrg.add_andCondition('Volume', 25000, '>', list(range(10, 20)))
myStrg.add_andCondition('ER', 'ERmean', '>', list(range(10, 20)))
myStrg.add_condition('short')

myStrg.add_andCondition('Close', 'MA', '<', 5)
myStrg.add_andCondition('Close', 'MA', '>', 2)
myStrg.add_andCondition('_long_flag', True, '==', 0)
myStrg.add_condition('clear')

myStrg.add_andCondition('Close', '_long_meanPrice', '<', 0, func2=lambda x:x*0.97)
myStrg.add_andCondition('_long_flag', True, '==', 0)
myStrg.add_condition('clear')

myStrg.add_andCondition('Close', 'MA', '>', 5)
myStrg.add_andCondition('Close', 'MA', '<', 2)
myStrg.add_andCondition('_short_flag', True, '==', 0)
myStrg.add_condition('clear')

myStrg.add_andCondition('Close', '_short_meanPrice', '>', 0, func2=lambda x:x*1.03)
myStrg.add_andCondition('_short_flag', True, '==', 0)
myStrg.add_condition('clear')

# backtest
tester.backtest_tmp(myStrg, backdata)