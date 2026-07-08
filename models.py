from database import base
from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy.sql import func


class Message(base):
    __tablename__ = "messages"
    id = Column(Integer,primary_key=True,index=True)
    role = Column(String)
    session_id = Column(String)
    content = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    