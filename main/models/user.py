from sqlalchemy import Column, VARCHAR, NVARCHAR

from main.models.base import Base


class UserModel(Base):
    __tablename__ = "user"

    full_name = Column(NVARCHAR(length=50), nullable=False)
    email = Column(VARCHAR(length=320), unique=True, nullable=False)
    hashed_password = Column(VARCHAR(length=72), nullable=False)
