from pydantic import constr

from main.schemas.base import BaseSchema


class CategoryBaseSchema(BaseSchema):
    name: constr(min_length=1, max_length=50)


class CategoryBatchResponseSchema(CategoryBaseSchema):
    id: int


class CategorySchema(CategoryBaseSchema):
    description: constr(min_length=1, max_length=5000)


class CategoryCreationRequestSchema(CategorySchema):
    pass


class CategoryResponseSchema(CategorySchema):
    pass
