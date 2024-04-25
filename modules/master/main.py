from typing import Callable

from modules.master.functional_event import init_functional_event_handler
from modules.master.transmission_event import init_transmission_event_handler
from pipe import Pipe, Notification

notifyPipe: Pipe
log: Callable[[str], None]


def init_module(pipe: Pipe):
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "管理员")


def main(pipe: Pipe):
    init_module(pipe)
    init_transmission_event_handler(pipe)
    init_functional_event_handler(pipe)

    log('启动！')
