from sqlalchemy import NVARCHAR, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from main.models.base import Base


class CategoryModel(Base):
    __tablename__ = "category"

    name = Column(NVARCHAR(length=50), unique=True, nullable=False)
    description = Column(Text(length=5000))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("UserModel")
    items = relationship("ItemModel", back_populates="category", cascade="all, delete")
