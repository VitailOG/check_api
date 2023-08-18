from typing import Literal

from pydantic import BaseModel
from pydantic import validator

from src.lib.security import get_password_hash


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: Literal["bearer"]  # noqa

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    name: str
    username: str
    password: str

    hash_password = validator("password")(lambda cls, v: get_password_hash(v))
