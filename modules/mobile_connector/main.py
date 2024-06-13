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

default_addr = "B8:27:EB:8B:93:33"
default_port = 1

service_uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"


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

    advertise_retry_count = 0

    while True:
        try:
            server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

            server_sock.bind(("", bluetooth.PORT_ANY))
            server_sock.listen(10)

            port = server_sock.getsockname()[1]
            addr = bluetooth.read_local_bdaddr()[0]

            bluetooth.advertise_service(
                server_sock,
                "MagicMirrorServer",
                service_id=service_uuid,
                service_classes=[service_uuid, bluetooth.SERIAL_PORT_CLASS],
                profiles=[bluetooth.SERIAL_PORT_PROFILE]
            )
            advertise_retry_count = 0

            log("OPEN Bluetooth Advertise Service!")
            log(f"Local Address: {addr} Port: {port} Service UUID: {service_uuid}")
            notifyPipe.send("BLUETOOTH_ADVERTISE_OPEN", {
                "addr": addr,
                "port": port,
                "uuid": service_uuid,
            })

            while True:
                client_sock, address = server_sock.accept()
                log("Client Connection Open:", address)
                threading.Thread(target=lambda: handle_accept(client_sock, address)).start()

        except Exception as e:
            log("RFCOMM Service Meet Exception:", e)
            log("Temporary Send Default Advertise configuration!")
            notifyPipe.send("BLUETOOTH_ADVERTISE_OPEN", {
                "addr": default_addr,
                "port": default_port,
                "uuid": service_uuid,
            })

            if str(e).startswith("[Errno 100]"):
                raise Exception("System bluetooth is not open! Module stop!")
            elif str(e).startswith("[Errno 13]"):

                raise Exception("Please run this program with 'sudo'!")
            elif str(e).startswith("[Errno 111]") or str(e).startswith("[Errno 2]"):
                raise Exception("Edit /lib/systemd/system/bluetooth.service and set "
                                "\"ExecStart=/usr/lib/bluetooth/bluetoothd -E -C\", then restart the system. (If "
                                "\"ExecStart\" is not existed, please insert it into [Service])")

            elif advertise_retry_count >= 10:
                raise Exception("Too many advertise retry! Module stop!")
            log("Wait For Restart...")
            advertise_retry_count += 1
            time.sleep(1)
            continue
