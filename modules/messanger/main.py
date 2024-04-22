from modules.messanger.websocket_server import run_websocket_server
from pipe import Pipe

notifyPipe: Pipe

moduleFlag = "MESSANGER"


def on_connected():
    notifyPipe.send(moduleFlag, f"Websocket Connection Established!")


def receive_handler(msg: any):
    notifyPipe.send(moduleFlag, f"Receive: {msg}")


def main(pipe: Pipe):
    global notifyPipe
    notifyPipe = pipe
    notifyPipe.send(moduleFlag, 'MESSANGER START!')
    run_websocket_server(
        host="localhost",
        port=8083,
        on_connected=on_connected,
        on_receive=receive_handler
    )
