from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base


class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime)


Base = declarative_base(cls=BaseModel)
