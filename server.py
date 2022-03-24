import asyncio
import websockets

import logging as logger


# Constants
HOST = 'localhost'
PORT = 8000

# create handler for each connection
async def handler(websocket, path):
    data = await websocket.recv()

    reply = f"Data recieved as:  {data}!"

    await websocket.send(reply)


logger.info(f'Starting websocket server on {HOST}:{PORT}')
start_server = websockets.serve(handler, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
