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
    setting = Column(Text, default=json.dumps(CustomSetting.default().__dict__()))


class KeyValuePairStorage(Base):
    __tablename__ = "storage"
    key = Column(String, primary_key=True)
    value = Column(Text, nullable=True, default=None)


Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
