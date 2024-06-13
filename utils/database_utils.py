from __future__ import annotations

from utils.orm import *
from utils.pipe import Pipe


def get_face_id() -> str | None:
    return RuntimeCache.get("AVAILABLE_FACE_ID")


def get_userdata(faceid: str) -> dict | None:
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            return None
        return json.loads(target_column.one().setting)


def set_userdata(faceid: str, setting: dict, pipe: Pipe | None = None):
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            raise Exception("User Not Found!")
        target_column.update({
            UserInfo.setting: json.dumps(setting)
        })
        session.commit()
        if pipe is not None:
            pipe.send("USERDATA_UPDATE", {"face_id": faceid})


def get_nickname(faceid: str):
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            return None
        return target_column.one().nickname


def set_nickname(faceid: str, nickname: str, pipe: Pipe | None = None):
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            raise Exception("User Not Found!")
        target_column.update({
            UserInfo.nickname: nickname
        })
        session.commit()
        if pipe is not None:
            pipe.send("USERDATA_UPDATE", {"face_id": faceid})
