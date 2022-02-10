from sqlalchemy import Column, Integer, ForeignKey, NVARCHAR, Text
from sqlalchemy.orm import relationship

from main.models.base_model import Base


class ItemModel(Base):
    __tablename__ = "item"

    name = Column(NVARCHAR(length=50), unique=True, nullable=False)
    description = Column(Text(length=5000))
    category_id = Column(Integer, ForeignKey("category.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("UserModel")
    category = relationship("CategoryModel")
