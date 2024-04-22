from datetime import datetime
from queue import Queue
from typing import Callable


class Notification:
    def __init__(self, flag: str, msg: any):
        self.flag = flag
        self.msg = msg
        self.stamp = datetime.now()


class Subscriber:
    def __init__(
            self,
            flag: str = "",
            handler: Callable[[Notification], None] = lambda _: None,
            receive_all: bool = False
    ):
        self.receive_all = receive_all
        self.flag = flag
        self.notify = handler


class Pipe:
    def __init__(self, logger: Callable[[Notification], None], maxsize=1000):
        self.msgQueue = Queue(maxsize=maxsize)
        self.subscribers: list[Subscriber] = []
        self.logger = logger

    def hold(self) -> None:
        while True:
            notification: Notification = self.msgQueue.get()
            self.logger(notification)
            for subscriber in [s for s in self.subscribers if (s.receive_all or s.flag == notification.flag)]:
                subscriber.notify(notification)

    def notify(self, notification: Notification) -> None:
        self.msgQueue.put(notification)

    def send(self, flag: str, msg: any) -> None:
        self.notify(Notification(flag, msg))

    def subscribe(self, subscriber: Subscriber) -> bool:
        if subscriber in self.subscribers:
            return False
        self.subscribers.append(subscriber)
        return True

    def on(self, flag: str, handler: Callable[[Notification], None]) -> None:
        self.subscribers.append(Subscriber(flag, handler))
