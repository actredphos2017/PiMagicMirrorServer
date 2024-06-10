from __future__ import annotations

import os
import threading
import time
from typing import Callable

import bluetooth

from utils.define_module import define_module
from modules.mobile_connector.bluetooth_socket_wrapper import BluetoothSocketWrapper
from utils.pipe import Pipe, Notification

notifyPipe: Pipe
log: Callable

service_uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
bluetooth_port = 1


def run_sys_cmd(cmd: str):
    return os.popen(cmd).read().strip()


def handle_accept(client_socket: bluetooth.BluetoothSocket, address):
    handler = BluetoothSocketWrapper(client_socket, address)
    handler.on_any(lambda h, flag, data: log("Receive", flag, data))
    handler.on_close(lambda h: log("Client Connection Close:", h.address))
    handler.on_error(lambda h, e: log("Client Connection Meet Error:", e))
    handler.hold()


@define_module("MOBILE")
def main(pipe: Pipe):
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "MOBILE")
    log("START!")

    global service_uuid

    init_cmds = [
        "bluetoothctl power on",
        "bluetoothctl discoverable on"
    ]

    for cmd in init_cmds:
        log(f"Output of System Command \"{cmd}\":", run_sys_cmd(cmd))

    while True:
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        server_sock.bind(("", bluetooth.PORT_ANY))
        server_sock.listen(10)

        port = server_sock.getsockname()[1]
        addr = bluetooth.read_local_bdaddr()[0]

        try:
            bluetooth.advertise_service(
                server_sock,
                "MagicMirrorServer",
                service_id=service_uuid,
                service_classes=[service_uuid, bluetooth.SERIAL_PORT_CLASS],
                profiles=[bluetooth.SERIAL_PORT_PROFILE]
            )
        except Exception as e:
            log("Advertise Failed! Exception Track:", e)
            log("STOP! Wait For Restart...")
            time.sleep(1)
            continue

        log("OPEN Bluetooth Advertise Service!")
        log(f"Local Address: {addr} Port: {port} Service UUID: {service_uuid}")

        try:
            while True:
                client_sock, address = server_sock.accept()
                log("Client Connection Open:", address)
                threading.Thread(target=lambda: handle_accept(client_sock, address)).start()
        except Exception as e:
            server_sock.close()
            log("MEET ERROR", e)
            log("STOP! Wait For Restart...")
            time.sleep(1)
