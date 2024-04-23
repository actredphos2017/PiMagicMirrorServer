import json
from typing import Callable

from modules.messanger.main import external_event
from orm import Session, UserInfo
from pipe import Pipe, Notification, Event

notifyPipe: Pipe
log: Callable[[str], None]


def init_module(pipe: Pipe):
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "管理员")


def handle_user_enter(event: Event):
    faceid = event.data['faceid']
    with Session() as session:
        user: UserInfo = session.query(UserInfo).get(faceid)
        while user is None:
            session.add(UserInfo(faceid=faceid))
            session.commit()
            log("新用户创建: {}".format(faceid))
            user = session.query(UserInfo).get(faceid)
        log("用户进入: {}@{}".format(user.nickname, faceid))
        notifyPipe.send("SEND_EXTERNAL", external_event("WAKE", {
            "faceid": faceid,
            "setting": json.loads(user.setting),
            "nickname": user.nickname,
            "create_time": user.create_time.isoformat(),
        }))


def handle_user_leave(_: Event):
    notifyPipe.send("SEND_EXTERNAL", external_event("SLEEP"))


def transfer_only(event: Event):
    notifyPipe.send("SEND_EXTERNAL", external_event(event.flag, event.data))


def main(pipe: Pipe):
    init_module(pipe)

    notifyPipe.on("FACE_ENTER", handle_user_enter)
    notifyPipe.on("FACE_LEAVE", handle_user_leave)

    notifyPipe.on("ASSISTANT_BEGIN", transfer_only)
    notifyPipe.on("ASSISTANT_ASK", transfer_only)
    notifyPipe.on("ASSISTANT_ANSWER", transfer_only)
    notifyPipe.on("ASSISTANT_CLOSE", transfer_only)

    log('启动！')
