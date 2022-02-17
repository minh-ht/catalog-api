from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_onupdate=func.now())


Base = declarative_base(cls=BaseModel)
