from typing import Self

from pydantic import Field, BaseModel, EmailStr, field_validator, model_validator

from schemas.base import DateTime


class BaseUser(BaseModel):
    email: EmailStr = Field(..., examples=['john_doe@gmail.com'])
    first_name: str | None = Field(None, examples=["John"])
    last_name: str | None = Field(None, examples=["Doe"])


class UserCreate(BaseUser):
    password: str = Field(...,
                          description=(
                              "Password must be at least 8 characters long and meet the following criteria:\n"
                              "- At least one numeral (0-9)\n"
                              "- At least one uppercase letter (A-Z)\n"
                              "- At least one lowercase letter (a-z)\n"
                              "- At least one special character (e.g., !@#$%^&*(),.?\":{}|<>)."
                          ),
                          min_length=8,
                          examples=['P@ssword1'])  # todo: validator
    confirm_password: str = Field(...,
                                  description="Must be the same as the password.",
                                  examples=['P@ssword1'])

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if (
                not any(char.isdigit() for char in password) or
                not any(char.islower() for char in password) or
                not any(char.isupper() for char in password) or
                not any(char in "!@#$%^&*()_+" for char in password)
        ):
            raise ValueError('Password must contain at least one uppercase letter, '
                             'one lowercase letter, one digit, and one special character.')
        return password

    @model_validator(mode='after')
    def verify_password_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('Password and confirm password do not match.')
        return self


class UserInDBBase(BaseUser):
    id: str | None = Field(None)
    is_active: bool = Field(False)
    is_superuser: bool = Field(False)

    class Config:
        orm_mod = True


class UserInDB(UserInDBBase, DateTime):
    password: str


class UserRead(UserInDBBase):
    ...
