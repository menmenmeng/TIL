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
from cert.myvars import logFile_base
from trade_rules.prelim import Prelim
from trade_rules.callback import Callback

sec = float(input("How much time you want to execute trader? (in second) : "))

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


'''
Defining futures client instances.
First one is REST API instance,
Second one is WSS API instance.

# REST API instance example

1. realnet

um_futures_client = UMFutures(key=API_KEY, secret=SECRET_KEY)
my_client = UMFuturesWebsocketClient()


2. testnet

um_futures_client = UMFutures(key=TEST_API_KEY, secret=TEST_SECRET_KEY, base_url=futures_testnet)
my_client = UMFuturesWebsocketClient(stream_url=futures_websocket_testnet)

# example end.
'''
um_futures_client = UMFutures(key=API_KEY, secret=SECRET_KEY)
my_client = UMFuturesWebsocketClient()


'''
Do things before websocket runs. By Using Prelim,
1. Get current account infos.
2. Get streamDict (for Callback class's input)
3. Get past few kline rows (for Callback class's input)
And make stream lists, because wss subscribing needs parameter of stream list.
'''
prelim = Prelim(um_futures_client)
walletBalance, currentAsset, positionAmt, entryPrice, streamDict = prelim.getInfo_trade("btcusdt", 'kline1m', 'userData')
lastKlines = prelim.getData_OHLCV("1m", limit=500)
stream = list(streamDict.values())

with open(f'{logFile_base}accountInfo.txt', 'a') as f:
    today = datetime.now().strftime('%y%m%d')
    now = datetime.now().strftime('%H:%M:%S')
    f.write(f"time:{today}, {now} \t")
    f.write(f"walletBalance:{walletBalance}, currentAsset:{currentAsset},  positionAmt:{positionAmt}, entryPrice:{entryPrice} \n")

'''
Defining callback instance.
config logging, and subscribe websocket.
'''
callbackExecuter = Callback(
    um_futures_client,
    walletBalance,
    currentAsset, 
    positionAmt,
    entryPrice,
    lastKlines, 
    **streamDict)  # Key와 Value가 더 잘 구분되게 수정 필요함. 

config_logging(logging, logging.DEBUG)

my_client.start()

my_client.live_subscribe(
    stream=stream,
    id=1,
    callback=callbackExecuter.callback,
)

try:
    time.sleep(sec)

except KeyboardInterrupt:
    print(callbackExecuter.klineCollector.DataFrame)
    my_client.stop()


logging.debug("closing ws connection")
print(callbackExecuter.klineCollector.DataFrame)
my_client.stop()