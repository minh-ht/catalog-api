from pydantic import BaseModel, Extra


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        extra = Extra.forbid
        error_msg_templates = {
            "value_error.any_str.max_length": " exceeds max length ({limit_value})",
        }
