from __future__ import annotations

import json
from typing import Callable

import bluetooth


class BluetoothSocketWrapper:
    def __init__(self, client_socket: bluetooth.BluetoothSocket, address: tuple[str, int]):
        self.client_socket = client_socket
        self.address = address
        self.close_handlers: list[Callable[[BluetoothSocketWrapper], None]] = []
        self.error_handlers: list[Callable[[BluetoothSocketWrapper, Exception], None]] = []
        self.subscribers: dict[str, list[Callable[[BluetoothSocketWrapper, any], None]]] = {}
        self.any_subscribers: list[Callable[[BluetoothSocketWrapper, str, any], None]] = []

    # client_socket.recv(1024) is json string likes {"flag": "EVENT_NAME", "data": {...}}
    def on(self, flag: str, handler: Callable[[BluetoothSocketWrapper, any], None]):
        if flag in self.subscribers:
            self.subscribers[flag].append(handler)
        else:
            self.subscribers[flag] = [handler]

    def on_close(self, handler: Callable[[BluetoothSocketWrapper], None]):
        self.close_handlers.append(handler)

    def on_error(self, handler: Callable[[BluetoothSocketWrapper, Exception], None]):
        self.error_handlers.append(handler)

    def on_any(self, handler: Callable[[BluetoothSocketWrapper, str, any], None]):
        self.any_subscribers.append(handler)

    def send(self, flag: str, data: any):
        self.client_socket.send(json.dumps({"flag": flag, "data": data}))

    def close(self):
        self.client_socket.close()

    def hold(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    continue

                try:
                    message = json.loads(data)
                    flag = message.get("flag")
                    data = message.get("data")

                    if flag in self.subscribers:
                        for handler in self.subscribers[flag]:
                            handler(self, data)

                    for handler in self.any_subscribers:
                        handler(self, flag, data)

                except json.JSONDecodeError as e:
                    for handler in self.error_handlers:
                        handler(self, e)
                    break

        except Exception as e:
            for handler in self.error_handlers:
                handler(self, e)
        finally:
            try:
                self.client_socket.close()
            except:
                pass
            for handler in self.close_handlers:
                handler(self)
