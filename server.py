import asyncio
import websockets

from ServerStatusHelper import ServerStatusHelper

ss = ServerStatusHelper()

# Constants
HOST = 'localhost'
PORT = 8000
INFO_CONNECTED = '{name} connected.'
INFO_DISCONNECTED = '{name} disconnected.'
def info_con(name):
    return INFO_CONNECTED.replace('{name}', str(name))
def info_discon(name):
    return INFO_DISCONNECTED.replace('{name}', str(name))


# Dynamic
connected = set()


# Add JSON support for chat
async def update_server_status():
    while True:
        api_response = ss.update()
        websockets.broadcast(connected, f'[SERVER_STATUS]: {"online" if api_response["online"] else "offline"}<br>{"<br>".join(api_response["motd"]["html"])}')

        await asyncio.sleep(10)

####
async def broadcast():
    while True:
        # websockets.broadcast(connected, '[SERVER]: woof constantly!')
        await asyncio.sleep(10)


# create handler for each connection
async def handler(websocket, path):
    # Register.
    connected.add(websocket)
    name = websocket.remote_address[1]

    print(info_con(name))
    print(f'Current Connections: {[i.remote_address[1] for i in connected]}')

    websockets.broadcast(connected, info_con(name))

    try:
        async for msg in websocket:
            msg = msg.strip()
            if msg in ('Connection established', ''):
                pass
            elif msg == 'ping':
                await websocket.send('[SERVER]: Pong!')
            else:
                websockets.broadcast(connected, f'[{name}]: {msg}')
    finally:
        print(info_discon(name))
        websockets.broadcast(connected, info_discon(name))
        connected.remove(websocket)


if __name__ == '__main__':
    # SETUP
    asyncio.get_event_loop().create_task(update_server_status())
    asyncio.get_event_loop().create_task(broadcast())

    print(f'Starting websocket server on ws://{HOST}:{PORT}')
    start_server = websockets.serve(handler, HOST, PORT)

    print('Running event loop..')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
