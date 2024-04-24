import asyncio
import json
from typing import Callable

import websockets

import utils.websocket_server as websocket_server
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
    log = Notification.create_notifier(pipe, "连接信使")


def handle_receive(msg: str, _):
    try:
        event = json.loads(msg)
        log("Websocket 收到事件:", event['event'])
        notifyPipe.send("EXTERNAL_RECEIVE", event)
    except:
        log("Websocket 收到异常消息:", msg)


def handle_send(event: Event, _):
    try:
        log("Websocket 发送事件:", event.data['event'])
        asyncio.run(websocket_server.broadcast(json.dumps(event.data)))
    except:
        log("Websocket 已阻止异常事件发送:", json.dumps(event.data))


def main(pipe: Pipe):
    init_module(pipe)
    log('启动！')

    notifyPipe.on("EXTERNAL_SEND", handle_send)

    websocket_server.run_websocket_server(
        host="localhost",
        port=8083,
        on_connected=lambda: log(f"Websocket 已连接！"),
        on_receive=handle_receive,
        on_disconnect=lambda: log("Websocket 连接断开！"),
        on_error=lambda e: log(f"发生异常", e)
    )
