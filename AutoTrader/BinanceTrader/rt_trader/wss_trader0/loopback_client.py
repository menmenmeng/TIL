import asyncio
import websockets

async def my_connect():
    async with websockets.connect("ws://localhost:3000") as websocket:
        for i in range(1, 100, 1):
            await websocket.send(f"i = {i}\t Hi, I'm client")
            data_rcv = await websocket.recv()
            print("data received from server : ", data_rcv)


# connect to server
asyncio.get_event_loop().run_until_complete(my_connect())