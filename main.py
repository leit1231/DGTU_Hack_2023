import asyncio
import datetime
import random
import websockets

# async def show_time(websocket, q):
#     while True:
#         message = datetime.datetime.utcnow().isoformat() + "Z"
#         await websocket.send(message)
#         await asyncio.sleep(random.random() * 2 + 1)
#
# async def main():
#     async with websockets.serve(show_time, "localhost", 5678):
#         await asyncio.Future()  # run forever
#
# if __name__ == "__main__":
#     asyncio.run(main())


all_clients = []
async def send_message(message: str):
    for client in all_clients:
        await client.send(message)
async def new_client_connected(client_socket: websockets.WebSocketClientProtocol, path: str):
    print("pod")
    all_clients.append(client_socket)
    while True:
        new_message = await client_socket.recv()
        print("New message from a client:", new_message)
        await send_message(message=new_message)

async def start_server():
    await websockets.serve(new_client_connected, 'localhost', 12345)



if __name__=='__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(start_server())
    event_loop.run_forever()



