from sqlalchemy import Column, DateTime, Integer, ForeignKey, NVARCHAR, Text

from main.models.base_class import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR(length=50), unique=True, nullable=False)
    description = Column(Text(length=5000))
    category_id = Column(Integer, ForeignKey("category.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    created = Column(DateTime)
    updated = Column(DateTime)
