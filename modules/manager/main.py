import time
from typing import Callable

from orm import Session, UserInfo
from pipe import Pipe, Notification, Subscriber, Event

notifyPipe: Pipe
log: Callable[[str], None]


def init_module(pipe: Pipe):
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "MANAGER")


def handle_user_enter(event: Event):
    faceid = event.msg['faceid']
    with Session() as session:
        user = session.query(UserInfo).get(faceid)
        while user is None:
            session.add(UserInfo(faceid=faceid))
            session.commit()
            log("新用户创建: {}".format(faceid))
            user = session.query(UserInfo).get(faceid)
        log("用户进入: {}@{}".format(user.nickname, faceid))


def main(pipe: Pipe):
    init_module(pipe)
    log('管理员模块启动！')
    notifyPipe.subscribe(Subscriber("FACE_ENTER", handle_user_enter))
