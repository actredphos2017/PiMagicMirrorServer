from typing import Callable

from modules.messanger.websocket_server import run_websocket_server
from pipe import Pipe, Notification

notifyPipe: Pipe
log: Callable[[str], None]


def on_connected():
    log(f"Websocket 已连接！")


def receive_handler(msg: any):
    log(f"Websocket 收到消息: {msg}")


def main(pipe: Pipe):
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "MESSANGER")
    log('信使模块启动！')
    run_websocket_server(
        host="localhost",
        port=8083,
        on_connected=on_connected,
        on_receive=receive_handler
    )
