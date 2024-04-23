import random
import time
from typing import Callable

from pipe import Pipe, Notification, Event

notifyPipe: Pipe
log: Callable


def init_module(pipe: Pipe):
    # 模块初始化
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "人脸识别")


def main(pipe: Pipe):
    init_module(pipe)
    log('启动！')

    # 主代码从这里开始

    # 示例
    while True:
        time.sleep(3)
        faceid = str(random.randint(0, 99))
        log("模拟人脸进入，人脸 ID:", faceid)
        notifyPipe.send("FACE_ENTER", {"faceid": faceid})

        time.sleep(5)
        log("模拟人脸离开")
        notifyPipe.send("FACE_LEAVE")
