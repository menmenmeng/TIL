import time
import logging
from binance.lib.utils import config_logging
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

from cert import binanceKey

#### KeyboardInterrupt
import signal
import sys
import time
import threading

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
forever = threading.Event()
forever.wait()

####


API_KEY = binanceKey.API_KEY
SECRET_KEY = binanceKey.SECRET_KEY

config_logging(logging, logging.DEBUG)


def message_handler(message):
    try:
        t += 1
        print(message)
        print(t)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

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

# except KeyboardInterrupt:
#     print("KeyboardInterrupt")
#     ws_client.stop()