from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.custom import CustomSetting

engine = create_engine('sqlite:///magic_mirror.sqlite3')
Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'user_info'
    faceid = Column(String, primary_key=True)
    nickname = Column(String, default="Guest")
    create_time = Column(DateTime, default=datetime.now)
    setting = Column(Text, default=json.dumps(
        CustomSetting.default().__dict__()))


class KeyValuePairStorage(Base):
    __tablename__ = "storage"
    key = Column(String, primary_key=True)
    value = Column(Text, nullable=True, default=None)


Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)


class LocalStorage:
    @staticmethod
    def get(key: str) -> str | None:
        with Session() as session:
            instance: KeyValuePairStorage | None = session.query(
                KeyValuePairStorage).get(key)
            if instance is None:
                return None
            return instance.value

    @staticmethod
    def set(key: str, value: str) -> None:
        with Session() as session:
            target_column = session.query(
                KeyValuePairStorage).filter_by(key=key)
            if target_column.count() == 0:
                session.add(KeyValuePairStorage(key=key, value=value))
            else:
                target_column.update({KeyValuePairStorage.value: value})
            session.commit()

    @staticmethod
    def remove(key: str) -> None:
        with Session() as session:
            target_column = session.query(
                KeyValuePairStorage).filter_by(key=key)
            if target_column.count() != 0:
                target_column.delete()
                session.commit()
