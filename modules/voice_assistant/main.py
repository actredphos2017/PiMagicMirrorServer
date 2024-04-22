import time
from typing import Callable

from pipe import Pipe, Notification

notifyPipe: Pipe
log: Callable[[str], None]


def init_module(pipe: Pipe):
    # 模块初始化
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "ASSISTANT")


def main(pipe: Pipe):
    init_module(pipe)
    log('语音助手模块启动！')

    # 主代码
    while True:
        time.sleep(3)
        log('Hello World')
