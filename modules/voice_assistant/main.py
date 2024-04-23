import time
from typing import Callable

from pipe import Pipe, Notification

notifyPipe: Pipe
log: Callable


def init_module(pipe: Pipe):
    # 模块初始化
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "语音助手")


def main(pipe: Pipe):
    init_module(pipe)
    log('启动！')

    # 主代码从这里开始
    while True:
        time.sleep(3)
        log('Hello World')
