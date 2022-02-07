from sqlalchemy import Column, Integer, ForeignKey, NVARCHAR, Text

from main.models.base_class import Base


class Category(Base):
    name = Column(NVARCHAR(length=50), unique=True, nullable=False)
    description = Column(Text(length=5000))
    user_id = Column(Integer, ForeignKey("user.id"))
