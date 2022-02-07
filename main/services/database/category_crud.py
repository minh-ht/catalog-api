from typing import List

from sqlalchemy.orm import Session

from main.models.category import Category
from main.schemas.category import CategoryBatchResponseSchema


def get_category_by_id(session: Session, category_id: str) -> Category:
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    return category


def get_category_by_name(session: Session, name: str) -> Category:
    category = session.query(Category).filter_by(name=name).one_or_none()
    return category


def get_categories(session: Session) -> List[CategoryBatchResponseSchema]:
    categories = session.query(Category).all()
    return categories


def create_category(session: Session, name, description, user_id: int) -> None:
    category = Category(
        name=name,
        description=description,
        user_id=user_id
    )
    session.add(category)
    session.commit()


def delete_category(session: Session, category: Category) -> None:
    session.delete(category)
    session.commit()
