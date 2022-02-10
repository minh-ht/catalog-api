from pydantic import BaseModel


class BaseClass(BaseModel):
    class Config:
        orm_mode = True
