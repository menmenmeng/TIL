import time
import logging
from binance.lib.utils import config_logging
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

from cert import binanceKey

API_KEY = binanceKey.API_KEY
SECRET_KEY = binanceKey.SECRET_KEY

config_logging(logging, logging.DEBUG)


def message_handler(message):
    print("1223")
    print(message)

client = UMFutures(API_KEY)
response = client.new_listen_key()

logging.info("Listen key : {}".format(response["listenKey"]))



ws_client = UMFuturesWebsocketClient()
ws_client.start()

ws_client.user_data(
    listen_key=response["listenKey"],
    id=1,
    callback=message_handler,
)

time.sleep(10)

logging.debug("closing ws connection")
ws_client.stop()