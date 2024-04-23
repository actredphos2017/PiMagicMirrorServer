import asyncio
import json
from typing import Callable

import websockets

import modules.messanger.websocket_server as websocket_server
from pipe import Pipe, Notification, Event

notifyPipe: Pipe
log: Callable


def external_event(event: str, data: dict | None = None):
    if data is None:
        data = {}
    return {
        "event": event,
        "data": data
    }


def init_module(pipe: Pipe):
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "MESSANGER")


def handle_receive(msg: str, _):
    try:
        event = json.loads(msg)
        log("Websocket 收到事件:", event['event'])
        notifyPipe.send("RECEIVE_EXTERNAL", event)
    except:
        log("Websocket 收到异常消息:", msg)


def handle_send(event: Event):
    try:
        asyncio.run(websocket_server.broadcast(json.dumps(event.data)))
    except websockets.exceptions.ConnectionClosed:
        pass


def main(pipe: Pipe):
    init_module(pipe)
    log('信使模块启动！')

    notifyPipe.on("SEND_EXTERNAL", handle_send)

    websocket_server.run_websocket_server(
        host="localhost",
        port=8083,
        on_connected=lambda: log(f"Websocket 已连接！"),
        on_receive=handle_receive,
        on_disconnect=lambda: log("连接已关闭"),
        on_error=lambda e: log(f"发生异常", e)
    )
