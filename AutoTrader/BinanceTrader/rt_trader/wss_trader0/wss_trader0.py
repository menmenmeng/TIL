# trader using ONLY markPrice.
import asyncio
import websockets
import json
import requests
from pprint import pprint

import sys
sys.path.append("C:/TIL/AutoTrader/BinanceTrader/rt_trader/")

from cert import binanceKey
from cert import myvars
from cert import myfuncs
from cert.wss_myfuncs import *

from trade import *

# strategy file
from cert import wss_indicators

rest_test = myvars.rest_test
rest_base = myvars.rest_base
webs_test = myvars.webs_test
webs_base = myvars.webs_base


# 1. Choose baseUrl from variables below.
baseUrl = webs_test
'''
  1) rest_test : testnet for REST
  2) webs_test : testnet for WSS
  3) webs_base : baseurl for WSS
'''

# 2. Get every stream name you want to recv data.
# * I will ONLY use markPrice, to place order.
# * moving average and bollinger band.
stream1 = get_streamName('btcusdt', 'markPrice')
stream2 = get_streamName('btcusdt', 'aggTrade')
stream3 = get_streamName('btcusdt', 'depth10')

# 3. Get param string (or list) you want to recv data.
param = get_stream_params(stream1, stream2)

# 4. Get final connection url.
connection_url = get_connecting_url(baseUrl, stream1, stream2)

account_info()

# 5. Define function to connect websocket, and send params.
async def connect_data(url, param):
    async with websockets.connect(url) as websocket:

        senddata = {"method":"SUBSCRIBE","params":param,"id":1}
        senddata = str(senddata)

        await websocket.send(senddata)

        # create strategy.
        bb = wss_indicators.BB()

        while True:
            result = await websocket.recv()
            result_json = json.loads(result)

            # different part start.
            try :
                result_stream = result_json["stream"]
            except:
                print(result, "printing this.")
                continue

    
            
            if result_stream==stream1: # markPrice
                
                

                print("# Stream Name: ", stream1)
                bb.markPrice_2_BB(result_json["data"], 5)
                
                flag_buy = False
                flag_sell = False

                if bb.assess_buy():
                    print("buy flag true")
                    flag_buy = True
                elif bb.assess_sell():
                    print("sell flag true")
                    flag_sell = True

                # Buy
                if flag_buy:
                    account_info()
                    buy(result_json['data']['i'], 0.01) # 230113 이게 float이 아니라 sequence인가 봄. type 확인 필요함
                    flag_buy = False
    
                elif flag_sell:
                    account_info()
                    sell(result_json['data']['i'], 0.01)
                    flag_sell = False



                pprint(bb.markPrice_df)




                # pprint(result_json["data"])

            elif result_stream==stream2: # markPrice
                # print("# Stream Name: ", stream3)
                # pprint(result_json["data"])
                pass

            elif result_stream==stream3: # depth10
                # print("# Stream Name: ", stream3)
                # pprint(result_json["data"])
                pass

            

# Run devil run
def run_part3():
    asyncio.run(connect_data(connection_url, param))

# END PART 3 (not completed)
# : Connecting Websocket, receive data AND conduct buy/sell method.




# Conducting Part
if __name__=="__main__":
    run_part3()