from pydantic import BaseModel, Extra


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        extra = Extra.forbid
