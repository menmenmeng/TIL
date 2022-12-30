import asyncio
import websockets

async def accept(websocket, path):
    while True:
        data_rcv = websocket.recv() # client에게서 data를 받아옴
        print("received_data = ", data_rcv)
        await websocket.send("websocket_server send data = ", data_rcv)

# 웹소켓 서버 만들기.
websoc_svr = websockets.serve(accept, "localhost", 3000)
websoc_svr
# waiting
asyncio.run(websoc_svr)