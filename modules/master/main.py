from typing import Callable

from modules.master.call_event_handler import init_call_event_handler
from modules.master.external_event_sender import init_message_transfer_handler
from pipe import Pipe, Notification

notifyPipe: Pipe
log: Callable[[str], None]


def init_module(pipe: Pipe):
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "管理员")


def main(pipe: Pipe):
    init_module(pipe)
    init_message_transfer_handler(pipe)
    init_call_event_handler(pipe)

    log('启动！')
