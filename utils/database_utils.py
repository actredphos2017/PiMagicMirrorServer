from __future__ import annotations

from utils.orm import *


def get_face_id() -> str | None:
    return RuntimeCache.get("AVAILABLE_FACE_ID")


def get_userdata(faceid: str) -> dict | None:
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            return None
        return json.loads(target_column.one().setting)


def set_userdata(faceid: str, setting: dict):
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            raise Exception("User Not Found!")
        target_column.update({
            UserInfo.setting: json.dumps(setting)
        })
        session.commit()


def get_nickname(faceid: str):
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            return None
        return target_column.one().nickname


def set_nickname(faceid: str, nickname: str):
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            raise Exception("User Not Found!")
        target_column.update({
            UserInfo.nickname: nickname
        })
        session.commit()

    