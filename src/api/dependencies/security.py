from pydantic import ValidationError
from jose import JWTError
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import SecurityScopes
from fastapi.security import HTTPAuthorizationCredentials

from src.lib.tokenizer import decode
from src.api.dependencies.db import get_repository
from src.repositories.user import UserRepository


async def get_current_user(
    security_scopes: SecurityScopes,
    token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer()),
    user: UserRepository = Depends(get_repository(UserRepository))
) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "authenticate_value"},
    )

    try:
        payload = decode(token.credentials)

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        role = await user.get_by_username(username)

        if role is None:
            raise credentials_exception

    except (JWTError, ValidationError):
        raise credentials_exception

    return role.username
