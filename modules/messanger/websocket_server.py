import asyncio
from typing import Callable

import websockets


def run_websocket_server(
        host: str,
        port: int,
        on_connected: Callable[[], None],
        on_receive: Callable[[any], None]
) -> None:
    async def echo(websocket: websockets.WebSocketServerProtocol):
        on_connected()
        async for message in websocket:
            on_receive(message)

    async def websocket_main():
        async with websockets.serve(echo, host, port):
            await asyncio.Future()

    asyncio.run(websocket_main())
