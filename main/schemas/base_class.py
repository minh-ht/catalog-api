from pydantic import BaseModel


class ORMEnabledBase(BaseModel):
    class Config:
        orm_mode = True
