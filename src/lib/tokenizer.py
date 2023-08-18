from typing import NamedTuple
from datetime import datetime
from datetime import timedelta

from jose import jwt

from src.config import settings


class TokenResponse(NamedTuple):
    access_token: str
    refresh_token: str


def create_token(data: dict, expires_delta: timedelta) -> str:
    data_copy = data.copy()

    expire = datetime.utcnow() + expires_delta
    data_copy.update({"exp": expire})

    encoded = jwt.encode(
        data_copy, settings.SECURITY_SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM
    )

    return encoded


def create_user_tokens(username: str) -> TokenResponse:
    access_token_expires = timedelta(
        minutes=settings.SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    refresh_token_expires = timedelta(
        minutes=settings.SECURITY_REFRESH_TOKEN_EXPIRE_MINUTES
    )

    access_token = create_token({"sub": username}, access_token_expires)

    refresh_token = create_token({"sub": username}, refresh_token_expires)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


def decode(token: str) -> dict[str, str]:
    return jwt.decode(
        token, settings.SECURITY_SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM]
    )
