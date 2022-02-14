from sqlalchemy import NVARCHAR, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from main.models.base import Base


class ItemModel(Base):
    __tablename__ = "item"

    name = Column(NVARCHAR(length=50), unique=True, nullable=False)
    description = Column(Text(length=5000))
    category_id = Column(Integer, ForeignKey("category.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("UserModel")
    category = relationship("CategoryModel", back_populates="items")
