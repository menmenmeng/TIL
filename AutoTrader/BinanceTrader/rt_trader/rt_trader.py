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
from trade_rules.collector import MarkPriceCollector, OrderUpdateCollector, AccountUpdateCollector
# from trade_rules.conditional import Something
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




prelim = Prelim(um_futures_client)
SYMBOL = "btcusdt"
current_asset, positionAmt, entryPrice, streamDict = prelim.getInfo_trade(SYMBOL, 'markPrice1s', 'userData')

## make stream lists
stream = list(streamDict.values())

# defining stream data collector
trader = Callback(um_futures_client, current_asset, current_amt=0, **streamDict)  # Key와 Value가 더 잘 구분되게 수정 필요함. 
# **로 들어가는거는 dictionary로 들어가도 괜찮나?? 실험좀해보자. --> **는 dictionary를 unpack하겠다는 뜻이다. 
# unpack의 의미가 있으므로, dictionary를 넣고 싶으면 unpack된 상태로 넣어야함.
# *중요* streamDict에서 markPrice..의 key는 'markPrice1s'이다. 그러나, 내가 처음 Callback class를 만들 때는 key가 'markPrice'여야 되도록 만들었었음. 그래서 그걸 고쳐야 함.
# END

# websocket start
config_logging(logging, logging.DEBUG)

my_client.start()

my_client.live_subscribe(
    stream=stream,
    id=1,
    callback=trader.callback,
)
try:
    time.sleep(15)
except KeyboardInterrupt:
    my_client.stop()

logging.debug("closing ws connection")
my_client.stop()