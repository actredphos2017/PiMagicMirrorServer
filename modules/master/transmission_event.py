import json

from modules.messanger.main import external_event
from orm import Session, UserInfo, LocalStorage
from pipe import Event, Pipe


def handle_user_enter(event: Event, pipe: Pipe):
    faceid = event.data['faceid']
    with Session() as session:
        user: UserInfo = session.query(UserInfo).get(faceid)
        while user is None:
            session.add(UserInfo(faceid=faceid))
            session.commit()
            user = session.query(UserInfo).get(faceid)
        pipe.send("EXTERNAL_SEND", external_event("FACE_ENTER", {
            "faceid": faceid,
            "setting": json.loads(user.setting),
            "nickname": user.nickname,
            "create_time": user.create_time.isoformat(),
        }))


def handle_external_event(event: Event, pipe: Pipe):
    pipe.send(event.data['event'], event.data.get('data'))


def transfer_only(event: Event, pipe: Pipe):
    pipe.send("EXTERNAL_SEND", external_event(event.flag, event.data))


def handle_environment_active(event: Event, pipe: Pipe):
    LocalStorage.set("environment", "active")
    pipe.send("EXTERNAL_SEND", external_event(event.flag, event.data))


def handle_environment_silent(event: Event, pipe: Pipe):
    LocalStorage.set("environment", "silent")
    pipe.send("EXTERNAL_SEND", external_event(event.flag, event.data))


def init_transmission_event_handler(pipe: Pipe):
    # SEND
    pipe.on("ENVIRONMENT_ACTIVE", handle_environment_active)
    pipe.on("ENVIRONMENT_SILENT", handle_environment_silent)
    pipe.on("FACE_ENTER", handle_user_enter)
    pipe.on("FACE_LEAVE", transfer_only)

    pipe.on("ASSISTANT_BEGIN", transfer_only)
    pipe.on("ASSISTANT_ASK_VOLUME", transfer_only)
    pipe.on("ASSISTANT_ASK", transfer_only)
    pipe.on("ASSISTANT_ANSWER", transfer_only)
    pipe.on("ASSISTANT_WAITING", transfer_only)
    pipe.on("ASSISTANT_CLOSE", transfer_only)

    pipe.on("WEATHER_UPDATE", transfer_only)

    # RECEIVE
    pipe.on("EXTERNAL_RECEIVE", handle_external_event)
