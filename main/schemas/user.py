from pydantic import EmailStr, constr, validator

from main.schemas.base import BaseSchema


class UserAuthenticationRequestSchema(BaseSchema):
    email: EmailStr
    password: constr(min_length=6, max_length=50)

    @validator("password")
    def password_validator(cls, password_string):
        error_message = (
            "Password must have at least 6 characters, "
            "including at least one lowercase letter, "
            "one uppercase letter, one digit."
        )
        contain_upper = False
        contain_lower = False
        contain_digit = False
        for character in password_string:
            if character.isupper():
                contain_upper = True
            elif character.islower():
                contain_lower = True
            elif character.isdigit():
                contain_digit = True
        is_password_valid = contain_upper and contain_lower and contain_digit
        if not is_password_valid:
            raise ValueError(error_message)
        return password_string


class UserCreationRequestSchema(UserAuthenticationRequestSchema):
    full_name: constr(min_length=1, max_length=50)
