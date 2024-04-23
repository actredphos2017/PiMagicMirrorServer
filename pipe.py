from datetime import datetime
from queue import Queue
from typing import Callable


class Event:
    def __init__(self, flag: str, msg_data: dict | None = None):
        if msg_data is None:
            msg_data = {}
        self.flag = flag
        self.data = msg_data
        self.stamp = datetime.now()


class Subscriber:
    def __init__(
            self,
            flag: str = "",
            handler: Callable[[Event], None] = lambda _: None,
            receive_all: bool = False
    ):
        self.receive_all = receive_all
        self.flag = flag
        self.notify = handler


class Pipe:
    def __init__(self, maxsize=1000):
        self.msgQueue = Queue(maxsize=maxsize)
        self.subscribers: list[Subscriber] = []

    def hold(self) -> None:
        while True:
            notification: Event = self.msgQueue.get()
            for subscriber in [s for s in self.subscribers if (s.receive_all or s.flag == notification.flag)]:
                subscriber.notify(notification)

    def send(self, flag: str, msg: dict | None = None) -> None:
        self.msgQueue.put(Event(flag, msg))

    def subscribe(self, subscriber: Subscriber) -> bool:
        if subscriber in self.subscribers:
            return False
        self.subscribers.append(subscriber)
        return True

    def on(self, flag: str, handler: Callable[[Event], None]) -> None:
        self.subscribers.append(Subscriber(flag, handler))


class Notification:
    def __init__(self, sender: str, msg: str):
        self.flag = sender
        self.msg = msg
        self.stamp = datetime.now()

    @staticmethod
    def create_notifier(pipe: Pipe, sender: str) -> Callable[[str], None]:
        def notify(msg: str) -> None:
            pipe.send("LOG", {
                "sender": sender,
                "msg": msg
            })

        return notify
