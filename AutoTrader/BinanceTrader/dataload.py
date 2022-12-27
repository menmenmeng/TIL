import asyncio
import websockets
import json

testBaseUrl_rest = "https://testnet.binancefuture.com"
testBaseUrl_wsk = "wss://stream.binancefuture.com"
wsBaseUrl = "wss://fstream.binance.com/ws/btcusdt@aggTrade" # 수정해야 함..

strmNm_aggTrade = "btcusdt@aggTrade"
strmNm_markPrice = "btcusdt@markPrice"

async def connect():
    async with websockets.connect(wsBaseUrl) as websocket:

        senddata = '{"method":"SUBSCRIBE","params":["btcusdt@aggTrade"],"id":1}'

        await websocket.send(senddata)

        while True:
            result = await websocket.recv()
            print(result)

asyncio.run(connect())