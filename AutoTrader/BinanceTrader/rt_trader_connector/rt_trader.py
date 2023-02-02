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
from trade_rules.trade_prelim import DataPrelim
from trade_rules.trade_callback import Callback



# import API KEY and SECRET KEY
## realnet (base_url is realnet default)
API_KEY = binanceKey.API_KEY
SECRET_KEY = binanceKey.SECRET_KEY
## testnet
key = test_binanceKey.API_KEY
secret = test_binanceKey.SECRET_KEY
## testnet base_urls (for test trading, stream_url = futures_websocket_testnet and base_url = futures_testnet)
futures_testnet = test_binanceKey.futures_testnet
futures_websocket_testnet = test_binanceKey.futures_websocket_testnet
# END


# defining futures client
um_futures_client = UMFutures(key=key, secret=secret, base_url=futures_testnet) # testnet
my_client = UMFuturesWebsocketClient(stream_url=futures_websocket_testnet) # testnet
# END




predata = DataPrelim(um_futures_client)

listenKey = predata.new_listenKey()
asset_USDT, position_BTCUSDT = predata.get_account()
current_asset = float(asset_USDT['walletBalance'])
positionAmt, entryPrice = float(position_BTCUSDT['positionAmt']), float(position_BTCUSDT['entryPrice'])





# defining websocket streams
## parameters.
SYMBOL = "btcusdt"
p_aggTrade = dict()
p_markPrice = dict(
    speed=1,
)
p_kline = dict(
    interval='2h'
)
## make each streams
aggTrade_stream = f"{SYMBOL}@aggTrade"
markPrice_stream = f"{SYMBOL}@markPrice@{p_markPrice['speed']}s"
kline_stream = f"{SYMBOL}@kline_{p_kline['interval']}"
listenKey = listenKey

## make stream lists
stream = [
    # aggTrade_stream,
    markPrice_stream,
    # kline_stream,
    listenKey,
]
# END



def message_handler(message):
    with open("streamDataExample.txt", 'a') as f:
        f.write(str(message))
        f.write('\n')
    print(message)

# defining stream data collector

trader = Callback(um_futures_client, current_asset, current_amt=0, listenKey=listenKey, markPrice=markPrice_stream)
# END

# websocket start
config_logging(logging, logging.DEBUG)

my_client.start()

my_client.live_subscribe(
    stream=stream,
    id=1,
    callback=message_handler,
)
try:
    time.sleep(40)
except KeyboardInterrupt:
    my_client.stop()

logging.debug("closing ws connection")
my_client.stop()