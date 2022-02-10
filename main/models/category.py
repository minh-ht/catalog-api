from sqlalchemy import Column, Integer, ForeignKey, NVARCHAR, Text
from sqlalchemy.orm import relationship

from main.models.base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "category"

    name = Column(NVARCHAR(length=50), unique=True, nullable=False)
    description = Column(Text(length=5000))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("UserModel")
