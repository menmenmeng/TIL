import time
import logging
from binance.lib.utils import config_logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.um_futures import UMFutures
from binance.error import ClientError

import matplotlib.pyplot as plt
import seaborn as sns

from cert import binanceKey
from cert import test_binanceKey
from cert.myfuncs import *
from trade_rules.prelim import Prelim
from trade_rules.callback import Callback


'''
import API Key and SECRET KEY.
First one is for REAL Net,
Second one is for TEST Net.
Third variables are base_urls. Each are REST testnet base_url, and WSS testnet base_url.
(RealNet base_url is not needed, b/c the default value is its url.)
'''
API_KEY = binanceKey.API_KEY
SECRET_KEY = binanceKey.SECRET_KEY

TEST_API_KEY = test_binanceKey.API_KEY
TEST_SECRET_KEY = test_binanceKey.SECRET_KEY

futures_testnet = test_binanceKey.futures_testnet
futures_websocket_testnet = test_binanceKey.futures_websocket_testnet


um_futures_client = UMFutures(key=API_KEY, secret=SECRET_KEY)

prelim = Prelim(um_futures_client)
walletBalance, currentAsset, positionAmt, entryPrice, streamDict = prelim.getInfo_trade("btcusdt", 'kline1m', 'userData')

print(walletBalance, currentAsset, positionAmt, entryPrice, streamDict)