from __future__ import annotations

import asyncio
import json
from typing import Callable

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
    log = Notification.create_notifier(pipe, "MESSANGER")


def handle_receive(msg: str, _):
    try:
        event = json.loads(msg)
        log("WEBSOCKET RECE <-", event['event'])
        notifyPipe.send("EXTERNAL_RECEIVE", event)
    except:
        log("Websocket RECE <- EXCEPTIONALLY", msg)


def handle_send(event: Event, _):
    try:
        log("WEBSOCKET SEND ->", event.data['event'])
        asyncio.run(websocket_server.broadcast(json.dumps(event.data)))
    except:
        log("Websocket SEND X> EXCEPTIONALLY", json.dumps(event.data))


def main(pipe: Pipe):
    init_module(pipe)
    log('START!')

    notifyPipe.on("EXTERNAL_SEND", handle_send)

    websocket_server.run_websocket_server(
        host="localhost",
        port=8083,
        on_connected=lambda: log("WEBSOCKET OPEN!"),
        on_receive=handle_receive,
        on_disconnect=lambda: log("WEBSOCKET CLOSE!"),
        on_error=lambda e: log("ERROR OCCURRED:", e)
    )
