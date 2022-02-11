from pydantic import constr

from main.schemas.base import ORMBaseSchema


class ItemBaseSchema(ORMBaseSchema):
    description: constr(min_length=1, max_length=5000)


class ItemSchema(ItemBaseSchema):
    name: constr(min_length=1, max_length=50)


class ItemCreationRequestSchema(ItemSchema):
    pass


class ItemUpdateRequestSchema(ItemBaseSchema):
    pass


class ItemResponseSchema(ItemSchema):
    pass
