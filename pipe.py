from datetime import datetime
from queue import Queue
from typing import Callable


class Notification:
    def __init__(self, flag: str, msg: any):
        self.flag = flag
        self.msg = msg
        self.stamp = datetime.now()


class Subscriber:
    def __init__(self, flag: str, handler: Callable[[Notification], None]):
        self.flag = flag
        self.handler = handler

    def notify(self, notification: Notification):
        self.handler(notification)


class Pipe:
    def __init__(self, logger: Callable[[Notification], None], maxsize=1000):
        self.msgQueue = Queue(maxsize=maxsize)
        self.subscribers: list[Subscriber] = []
        self.logger = logger

    def hold(self):
        while True:
            notification: Notification = self.msgQueue.get()
            self.logger(notification)
            for subscriber in [s for s in self.subscribers if s.flag == notification.flag]:
                subscriber.handler(notification)

    def notify(self, notification: Notification):
        self.msgQueue.put(notification)

    def send(self, flag: str, msg: any):
        self.notify(Notification(flag, msg))

    def subscribe(self, listener: Subscriber):
        self.subscribers.append(listener)
