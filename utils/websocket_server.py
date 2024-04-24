import asyncio
from typing import Callable

import websockets

connection_pool: set[websockets.WebSocketServerProtocol] = set()


async def broadcast(msg: str):
    for connection in connection_pool:
        try:
            await connection.send(msg)
        except websockets.exceptions.ConnectionClosed:
            continue


def run_websocket_server(
        host: str,
        port: int,
        on_connected: Callable[[], None],
        on_receive: Callable[[str, websockets.WebSocketServerProtocol], None],
        on_disconnect: Callable[[], None],
        on_error: Callable[[Exception], None],
) -> None:
    async def echo(websocket: websockets.WebSocketServerProtocol):
        on_connected()
        connection_pool.add(websocket)
        try:
            async for message in websocket:
                on_receive(message, websocket)
        except Exception as e:
            on_error(e)
        finally:
            on_disconnect()
            connection_pool.remove(websocket)

    async def websocket_main():
        async with websockets.serve(echo, host, port):
            await asyncio.Future()

    asyncio.run(websocket_main())
