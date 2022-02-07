from pydantic import constr

from main.schemas.base import ORMEnabledBase


class CategoryBase(ORMEnabledBase):
    name: constr(min_length=1, max_length=50)


class CategoryBatchResponseSchema(CategoryBase):
    id: int


class CategorySchema(CategoryBase):
    description: constr(min_length=1, max_length=5000)


class CategoryCreationRequestSchema(CategorySchema):
    pass


class CategoryResponseSchema(CategorySchema):
    pass
