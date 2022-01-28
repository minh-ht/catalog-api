from sqlalchemy import Column, DateTime, Integer, VARCHAR, NVARCHAR

from main.models.base_class import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(NVARCHAR(length=50), nullable=False)
    email = Column(VARCHAR(length=320), unique=True, nullable=False)
    hashed_password = Column(VARCHAR(length=72), nullable=False)
    created = Column(DateTime)
    updated = Column(DateTime)
