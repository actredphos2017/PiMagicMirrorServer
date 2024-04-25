import random
import time
from typing import Callable

from pipe import Pipe, Notification

notifyPipe: Pipe
log: Callable


def init_module(pipe: Pipe):
    # 模块初始化
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "人脸识别")


def demo():
    time.sleep(1)
    faceid = str(random.randint(0, 99))
    # 环境发生变化
    notifyPipe.send("ENVIRONMENT_ACTIVE")
    time.sleep(2)
    # 识别到人脸
    notifyPipe.send("FACE_ENTER", {"faceid": faceid})

    time.sleep(5)
    # 人脸离开
    notifyPipe.send("FACE_LEAVE")
    time.sleep(10)
    # 环境安静
    notifyPipe.send("ENVIRONMENT_SILENT")


def main(pipe: Pipe):
    init_module(pipe)
    log('启动！')

    # 主代码从这里开始

    # 示例
    # while True:
    #     demo()
    notifyPipe.send("ENVIRONMENT_ACTIVE")
