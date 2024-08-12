from sqlalchemy import Column, String, Text, JSON, Integer, TIMESTAMP, DateTime, Float, Boolean,text
from sqlalchemy.sql import func

from SQLService.Conn import Base


class User(Base):
    __tablename__ = 'user'
    username = Column(String(20), primary_key=True)
    password = Column(String(20), nullable=False)
    name = Column(String(100))
    email = Column(String(100))
    count = Column(Integer, server_default='0', nullable=False)
    creationtime = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20))
    itemName = Column(String(255))
    companyName = Column(String(255))
    companyTime = Column(TIMESTAMP)
    companyMoney = Column(Integer)
    companyScope = Column(Text)
    companyIntro = Column(Text)
    companyFile = Column(String(100))
    creationTime = Column(TIMESTAMP, default=func.current_timestamp())

class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    type = Column(String(20))
    input = Column(JSON)
    output = Column(Text)
    state = Column(Boolean, default=True)
    time = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)