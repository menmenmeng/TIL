import time
import requests
import numpy as np
import pandas as pd
import logging
from datetime import datetime
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.lib.utils import config_logging

# where API KEY stored.(USE YOUR OWN KEY)
from cert import binanceKey

# my own library
from backTester.BackTester import BackTester
from backTester.BackDataLoader import BackDataLoader
from conditionGenerator.ConditionGenerator import ConditionGenerator

# visualization
import matplotlib.pyplot as plt
import seaborn as sns


from itertools import product
import multiprocessing

# data loading


params = {
    'windowMA':[10, 15, 20, 25],
    'windowER':[10, 15, 20, 25],
    # 'c_std':[1.5, 1.65, 1.8, 2, 2.15],
    'c_ERmean':[1.75, 2],
    'pastFirst':[8, 10],
    'pastLast':[13, 15],
    'nowFirst':[1, 3],
    'nowLast':[4, 6],
    'th_Volume':[20000, 30000],
    'volFirst':[7, 11],
    'volLast':[14, 18]

}


items = list(params.values())
keys = list(params.keys())
prods = list(product(*items))
print(len(prods))

resultNum = 4
combIndexStorer = [-1]*resultNum
paramStorer = [0]*resultNum
max_n_results = [1]*resultNum

for combIndex, comb in enumerate(prods):
    print('combIndex: ', combIndex, end=' ')
    param = dict()
    for key, value in zip(keys, comb):
        param[key] = value
        # 요기서부터 집어넣는다.
    # print(param, end=' ')
    tester = BackTester()
    # print(id(tester), end='')
    backdata = pd.read_pickle('C:\\TIL\\AutoTrader\\BinanceTrader\\backdata.pkl')

    window_MA = param['windowMA']
    window_ER = param['windowER']
    backdata['MA'] = tester.get_MA(window_MA, backdata['Close'])
    backdata['std'] = tester.get_std(window_MA, backdata['Close'])
    backdata['UB'] = backdata['MA'] + 2 * backdata['std']
    backdata['U75'] = backdata['MA'] + backdata['std']
    backdata['LB'] = backdata['MA'] - 2 * backdata['std']
    backdata['L25'] = backdata['MA'] - backdata['std']
    backdata['ER'] = backdata['Close'].diff(window_ER).abs()/backdata['Close'].diff().abs().rolling(window_ER).sum()

    backdata['ERmean'] = backdata['ER'].mean()*param['c_ERmean']

    myStrg = ConditionGenerator(19, 0) # i-4, i-3, i-2, i-1, i


    myStrg.add_andCondition('Close', 'LB', '>', [param['pastFirst'], param['pastLast']])
    myStrg.add_andCondition('Close', 'LB', '<', [param['nowFirst'], param['nowLast']])
    myStrg.add_andCondition('Volume', param['th_Volume'], '<', [param['volFirst'], param['volLast']])
    myStrg.add_andCondition('ER', 'ERmean', '<', [param['volFirst'], param['volLast']])
    myStrg.add_condition('long')

    myStrg.add_andCondition('Close', 'UB', '<', [param['pastFirst'], param['pastLast']])
    myStrg.add_andCondition('Close', 'UB', '>', [param['nowFirst'], param['nowLast']])
    myStrg.add_andCondition('Volume', param['th_Volume'], '>', [param['volFirst'], param['volLast']])
    myStrg.add_andCondition('ER', 'ERmean', '>', [param['volFirst'], param['volLast']])
    myStrg.add_condition('short')

    myStrg.add_andCondition('Close', 'MA', '<', [3, 5])
    myStrg.add_andCondition('Close', 'MA', '>', [0, 2])
    myStrg.add_andCondition('_long_flag', True, '==', 0)
    myStrg.add_condition('clear')

    myStrg.add_andCondition('Close', '_long_meanPrice', '<', 0, func2=lambda x:x*(1-0.03))
    myStrg.add_andCondition('_long_flag', True, '==', 0)
    myStrg.add_condition('clear')

    myStrg.add_andCondition('Close', 'MA', '>', [3, 5])
    myStrg.add_andCondition('Close', 'MA', '<', [0, 2])
    myStrg.add_andCondition('_short_flag', True, '==', 0)
    myStrg.add_condition('clear')

    myStrg.add_andCondition('Close', '_short_meanPrice', '>', 0, func2=lambda x:x*(1+0.03))
    myStrg.add_andCondition('_short_flag', True, '==', 0)
    myStrg.add_condition('clear')

    # backtest
    tester.backtest_tmp(myStrg, backdata, printLog=False)

    r = tester.finalReturn
    for resIdx in range(resultNum):
        if r > max_n_results[resIdx]:
            try:
                max_n_results = max_n_results[:resIdx] + [r] + max_n_results[resIdx:resultNum-1]
                combIndexStorer = combIndexStorer[:resIdx] + [combIndex] + combIndexStorer[resIdx:resultNum-1]
                paramStorer = paramStorer[:resIdx] + [comb] + paramStorer[resIdx:resultNum-1]
            except:
                max_n_results = [r] + max_n_results[resIdx:resultNum-1]
                combIndexStorer = [combIndex] + combIndexStorer[resIdx:resultNum-1]
                paramStorer = [comb] + paramStorer[resIdx:resultNum-1]

    print(', Return:', r)

with open('BB_GridSearch_params.txt', 'a') as f:
    f.write(str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))+'\n'+'-'*20)
    f.write('Keys:'+str(keys))
    for idx, res, param in zip(combIndexStorer, max_n_results, paramStorer):
        f.write('Index'+str(idx)+' - Return - '+str(res)+' - Param '+str(param))
