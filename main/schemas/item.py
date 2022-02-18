from typing import List

from pydantic import constr

from main.schemas.base import BaseSchema


class ItemBaseSchema(BaseSchema):
    description: constr(min_length=1, max_length=5000)


class ItemSchema(ItemBaseSchema):
    name: constr(min_length=1, max_length=50)


class ItemCreationRequestSchema(ItemSchema):
    pass


class ItemUpdateRequestSchema(ItemBaseSchema):
    pass


class ItemResponseSchema(ItemSchema):
    pass


class ItemBatchResponseSchema(BaseSchema):
    total_number_of_items: int
    items_per_page: int = 20
    items: List[ItemResponseSchema]
