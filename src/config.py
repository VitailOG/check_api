import os

from typing import Any
from typing import Literal

from pydantic import validator
from pydantic import PostgresDsn
from pydantic import BaseSettings


def _assemble_db_connection(v: str | None, values: dict[str, Any]) -> Any:
    if isinstance(v, str):
        return v

    return PostgresDsn.build(
        scheme="postgresql+psycopg",
        user=values.get("POSTGRES_USER"),
        password=values.get("POSTGRES_PASSWORD"),
        host=values.get("POSTGRES_SERVER"),
        path=f'/{values.get("POSTGRES_DB")}',
    )


class Settings(BaseSettings):

    class Config:
        env_file = os.getenv("CHECK_ENV")
        env_file_encoding = "utf-8"

    # Docs
    TITLE: str = "Check api"
    DESCRIPTION: str = "api для взаємодії із чеками"

    # Postgresql settings
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    # Postgresql test settings
    TEST_POSTGRES_SERVER: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str

    SQLALCHEMY_TEST_DATABASE_URI: PostgresDsn | None = None

    DEBUG: bool = True

    SECURITY_SECRET_KEY: str
    SECURITY_REFRESH_TOKEN_COOKIE_KEY: str
    SECURITY_ALGORITHM: Literal["HS256"]
    SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECURITY_REFRESH_TOKEN_EXPIRE_MINUTES: int

    SECURITY_ACCESS_TOKEN_URL: str = "api/v1/auth/create-token"
    SECURITY_REFRESH_TOKEN_URL: str = "api/v1/auth/refresh"

    # Cookie settings
    SECURITY_REFRESH_TOKEN_COOKIE_EXPIRES: int
    SECURITY_REFRESH_TOKEN_COOKIE_PATH: str = SECURITY_REFRESH_TOKEN_URL
    SECURITY_REFRESH_TOKEN_COOKIE_DOMAIN: str | None
    SECURITY_REFRESH_TOKEN_COOKIE_HTTPONLY: bool = True
    SECURITY_REFRESH_TOKEN_COOKIE_SECURE: bool = True
    SECURITY_REFRESH_TOKEN_COOKIE_SAMESITE: Literal["lax", "strict", "none"]

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        return _assemble_db_connection(v, values)

    @validator("SQLALCHEMY_TEST_DATABASE_URI", pre=True)
    def assemble_test_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        values = {
            "POSTGRES_USER": values["TEST_POSTGRES_USER"],
            "POSTGRES_PASSWORD": values["TEST_POSTGRES_PASSWORD"],
            "POSTGRES_SERVER": values["TEST_POSTGRES_SERVER"],
            "POSTGRES_DB": values["TEST_POSTGRES_DB"]
        }
        return _assemble_db_connection(v, values)


settings = Settings()
