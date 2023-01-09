import asyncio
import websockets
import json
import requests
from cert import binanceKey
from cert import myvars

rest_test = myvars.rest_test
rest_base = myvars.rest_base
webs_test = myvars.webs_test
webs_base = myvars.webs_base

strmNm_aggTrade = "btcusdt@aggTrade"
strmNm_markPrice = "btcusdt@markPrice"




# START PART 1
# : Defining useful functions part for connecting websocket.


def get_streamName(symbol:str, event:str) -> str:
    
    '''
    get one stream name (or various streams' name.)
      These values will be used in get_url_streamPart, and get_params.
    
      Ex : func("btcusdt", "aggTrade") -> "btcusdt@aggTrade"
    '''
    
    streamName = symbol + "@" + event
    return streamName


def get_url_streamPart(*streamNames) -> str:

    '''
    get stream string which will be used in websocket connecting url.
      This function only be used to make websocket connecting url.
    
      Ex : func("btcusdt@aggTrade", "btcusdt@markPrice") -> "btcusdt@aggTrade/btcusdt@markPrice"
      Ex : func("btcusdt@aggTrade") -> "btcusdt@aggTrade"
      Ex : func() -> ValueError
    '''

    if len(streamNames)==1:
        return True, streamNames[0]
    elif len(streamNames)>1:
        return False, '/'.join(streamNames)
    else:
        raise ValueError("No stream value has been entered. Please enter valid value.")


def get_connecting_url(baseUrl:str, *streamNames):

    '''
    get final websocket connecting url.
      Websocket connecting url has the special input form below.
    
      1) <baseurl>/ws/<streamName>
      2) <baseurl>/stream?streams=<streamName1>/<streamName2>/<streamName3>/...
    
      To utilize this function, just enter baseUrl and streams:tuple that U got from func. get_streamNames.
    
      Ex : func("<baseUrl>", "btcusdt@aggTrade", "btcusdt@markPrice") -> "<baseUrl>/stream?streams=btcusdt@aggTrade/btcusdt@markPrice"
    '''

    single_flag, streamPart =  get_url_streamPart(*streamNames)
    if single_flag:
        url = baseUrl + '/ws/' + streamPart
    elif not single_flag:
        url = baseUrl + '/stream?streams=' + streamPart
    else:
        print('stream name not included, so return value is default baseUrl.')
        url = baseUrl

    return url


def get_stream_params(*streamNames):

    '''
    get params(streams) which will be loaded in websocket send_data.
    
      Ex : func("btcusdt@aggTrade", "btcusdt@markPrice") -> ["btcusdt@aggTrade", "btcusdt@markPrice"]
      Ex : func("btcusdt@aggTrade") -> "btcusdt@aggTrade"
    '''
    
    if len(streamNames)==1:
        return streamNames[0]
    elif len(streamNames)>1:
        return False, '/'.join(streamNames)
    else:
        raise ValueError("No stream value has been entered. Please enter valid value.")


# END PART 1
# : Defining useful functions part for connecting websocket.




# START PART 2
# : Connecting Websocket and receive data you want to browse.

# 1. Choose baseUrl from variables below.
baseUrl = webs_test
'''
  1) rest_test : testnet for REST
  2) webs_test : testnet for WSS
  3) webs_base : baseurl for WSS
'''

# 2. Get every stream name you want to recv data.
stream1 = get_streamName('btcusdt', 'aggTrade')
stream2 = get_streamName('btcusdt', 'markPrice')

# 3. Get param string (or list) you want to recv data.
param = get_stream_params(stream1, stream2)

# 4. Get final connection url.
connection_url = get_connecting_url(baseUrl, stream1, stream2)

# 5. Define function to connect websocket, and send params.
async def connect_recvdata(url, param):
    async with websockets.connect(url) as websocket:

        senddata = {"method":"SUBSCRIBE","params":param,"id":1}
        senddata = str(senddata)

        await websocket.send(senddata)

        while True:
            result = await websocket.recv()
            print(result)

# Run devil run
def run_part2():
    asyncio.run(connect_recvdata(connection_url, param))

# END PART 2
# : Connecting Websocket and receive data you want to browse.




# START PART 3 (not completed)
# : Connecting Websocket, receive data AND conduct buy/sell method.

# 1. Choose baseUrl from variables below. (REST)
baseUrl = rest_test
'''
  1) rest_test : testnet for REST
  2) rest_base : baseurl for REST
'''

# 2. Start user data stream.
url = baseUrl + "/fapi/v1/listenKey"
# listenKey_post_request = requests.post(url, params=)





# 1. Choose baseUrl from variables below.
baseUrl = webs_test
'''
  1) rest_test : testnet for REST
  2) webs_test : testnet for WSS
  3) webs_base : baseurl for WSS
'''

# 2. Get every stream name you want to recv data.
stream1 = get_streamName('btcusdt', 'aggTrade')
stream2 = get_streamName('btcusdt', 'markPrice')

# 3. Get param string (or list) you want to recv data.
param = get_stream_params(stream1, stream2)

# 4. Get final connection url.
connection_url = get_connecting_url(baseUrl, stream1, stream2)

# 5. Define function to connect websocket, and send params.
async def connect(url, param):
    async with websockets.connect(url) as websocket:

        senddata = {"method":"SUBSCRIBE","params":param,"id":1}
        senddata = str(senddata)

        await websocket.send(senddata)

        while True:
            result = await websocket.recv()
            print(result)

# Run devil run
asyncio.run(connect(connection_url, param))

# END PART 3 (not completed)
# : Connecting Websocket, receive data AND conduct buy/sell method.




# Conducting Part
if __name__=="__main__":
    run_part2()
    
