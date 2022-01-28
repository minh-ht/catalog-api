from sqlalchemy import Column, DateTime, Integer, ForeignKey, NVARCHAR, Text

from main.models.base_class import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR(length=50), unique=True, nullable=False)
    description = Column(Text(length=5000))
    user_id = Column(Integer, ForeignKey("user.id"))
    created = Column(DateTime)
    updated = Column(DateTime)
