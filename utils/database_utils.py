from __future__ import annotations

from utils.orm import *


def get_face_id() -> str | None:
    return LocalStorage.get("AVAILABLE_FACE_ID")


def get_settings(faceid: str):
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            return None
        return CustomSetting.from_dict(json.loads(target_column.one().setting))


def set_settings(faceid: str, setting: CustomSetting):
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            raise Exception("User Not Found!")
        target_column.update({
            UserInfo.setting: json.dumps(setting.__dict__())
        })
        session.commit()


def get_nickname(faceid: str):
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            return None
        return CustomSetting.from_dict(json.loads(target_column.one().nickname))


def set_nickname(faceid: str, nickname: str):
    with Session() as session:
        target_column = session.query(UserInfo).filter_by(faceid=faceid)
        if target_column.count() == 0:
            raise Exception("User Not Found!")
        target_column.update({
            UserInfo.nickname: nickname
        })
        session.commit()
