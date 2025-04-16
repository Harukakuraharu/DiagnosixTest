from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.functional_validators import AfterValidator

import models


def validate_password(password: str) -> str:
    assert len(password) >= 8, f"{password} is short"
    assert password.isalnum(), f"{password} must contain numbers and letters"
    return password


Password = Annotated[str, AfterValidator(validate_password)]


class User(BaseModel):
    email: EmailStr
    role: models.UserRole
    name: str


class UserResponse(User):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserCreate(User):
    password: Password


class Token(BaseModel):
    access_token: str


class UserLogin(BaseModel):
    email: str
    password: str
