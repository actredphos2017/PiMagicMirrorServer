from __future__ import annotations

import threading
import time
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
            handler: Callable[[Event, any], None] = lambda _, __: None,
            receive_all: bool = False
    ):
        self.receive_all = receive_all
        self.flag = flag
        self.notify = handler


class Pipe:
    def __init__(self, maxsize=1000):
        self.msgQueue = Queue(maxsize=maxsize)
        self.subscribers: list[Subscriber] = []
        self.lock = threading.Lock()
        self.lock.acquire()

    def hold(self) -> None:
        while True:
            notification: Event = self.msgQueue.get()
            if notification.flag == "__DISPATCHER_MAIN__":
                fun = notification.data.get("function")
                if fun is not None:
                    fun()
                self.lock.release()
            else:
                for subscriber in [s for s in self.subscribers if (s.receive_all or s.flag == notification.flag)]:
                    threading.Thread(target=lambda: subscriber.notify(notification, self)).start()

    def send(self, flag: str, msg: dict | None = None) -> None:
        self.msgQueue.put(Event(flag, msg))

    def run_on_main_thread(self, function: Callable[[], None]):
        self.send("__DISPATCHER_MAIN__", {"function": function})
        self.lock.acquire()

    def subscribe(self, subscriber: Subscriber) -> bool:
        if subscriber in self.subscribers:
            return False
        self.subscribers.append(subscriber)
        return True

    def on(self, flag: str, handler: Callable[[Event, Pipe], None]) -> Subscriber:
        subscriber = Subscriber(flag, handler)
        self.subscribers.append(subscriber)
        return subscriber

    def remove_subscriber(self, subscriber: Subscriber):
        self.subscribers.remove(subscriber)


class Notification:

    @staticmethod
    def create_notifier(pipe: Pipe, sender: str) -> Callable:
        def notify(*msg: any, seq: str = " ") -> None:
            pipe.send("LOG", {
                "sender": sender,
                "msg": seq.join(str(m) for m in msg)
            })

        return notify


if __name__ == '__main__':
    # Pipe 使用例子（事件驱动的并发编程）
    test_pipe = Pipe()

    # 当管道内出现标志为 HELLO 的事件时，打印事件数据
    test_subscriber = test_pipe.on("HELLO", lambda event, _: print(event.data))


    def work():
        # 创建一个任务，该任务每秒发送标志为 HELLO 与 WORLD 的事件
        while True:
            time.sleep(1)
            test_pipe.send("HELLO", {"text": "Hello"})
            test_pipe.send("WORLD", {"text": "World"})


    def subscriber_switcher():
        # 创建一个任务，该任务在 5.5 秒后将刚刚创建的关注者删除，并添加监听 WORLD 的关注者
        time.sleep(5.5)
        test_pipe.remove_subscriber(test_subscriber)
        test_pipe.on("WORLD", lambda event, _: print(event.data))


    # 创建两个线程，分别执行上面创建的任务
    threading.Thread(target=work).start()
    threading.Thread(target=subscriber_switcher).start()

    # 管道开始工作
    test_pipe.hold()
