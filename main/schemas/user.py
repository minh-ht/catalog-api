from pydantic import BaseModel, constr, EmailStr, validator


class UserAuth(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=50)

    @validator("password")
    def password_validator(cls, password_string):
        msg = "Password must have at least 6 characters, " \
              "including at least one lowercase letter, " \
              "one uppercase letter, one digit."
        contain_upper = False
        contain_lower = False
        contain_digit = False
        if len(password_string) < 6:
            raise ValueError(msg)
        for character in password_string:
            if character.isupper():
                contain_upper = True
            elif character.islower():
                contain_lower = True
            elif character.isdigit():
                contain_digit = True
        valid = contain_upper and contain_lower and contain_digit
        if not valid:
            raise ValueError(msg)
        return password_string


class UserCreate(UserAuth):
    full_name: constr(min_length=1, max_length=50)
