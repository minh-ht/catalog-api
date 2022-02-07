from pydantic import BaseModel, constr, validator


class CategoryBase(BaseModel):
    name: constr(min_length=1)

    @validator("name")
    def name_validator(cls, name_string):
        msg = "Category name exceeds max length (50)"
        if len(name_string) > 50:
            raise ValueError(msg)
        return name_string

    class Config:
        orm_mode = True


class CategoryBatchResponseSchema(CategoryBase):
    id: int


class CategorySchema(CategoryBase):
    description: constr(min_length=1)

    @validator("description")
    def name_validator(cls, description_string):
        msg = "Category description exceeds max length (5000)"
        if len(description_string) > 5000:
            raise ValueError(msg)
        return description_string


class CategoryCreationRequestSchema(CategorySchema):
    pass


class CategoryResponseSchema(CategorySchema):
    pass
