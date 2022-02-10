from sqlalchemy import Column, VARCHAR, NVARCHAR

from main.models.base_model import Base


class UserModel(Base):
    full_name = Column(NVARCHAR(length=50), nullable=False)
    email = Column(VARCHAR(length=320), unique=True, nullable=False)
    hashed_password = Column(VARCHAR(length=72), nullable=False)
