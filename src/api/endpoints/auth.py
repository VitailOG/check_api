from fastapi import APIRouter
from fastapi import Cookie
from fastapi import Depends
from fastapi import HTTPException
from jose import JWTError
from starlette import status
from starlette.responses import Response

from src.api.dependencies.db import get_repository
from src.api.schemas.user import TokenResponseSchema
from src.api.schemas.user import UserSchema
from src.config import settings
from src.lib.security import verify_password
from src.lib.tokenizer import create_user_tokens
from src.lib.tokenizer import decode
from src.repositories.user import UserRepository
from src.lib.oauth2 import OAuth2PasswordRequestForm

router = APIRouter()


def set_refresh_token_cookie(response: Response, token: str):
    response.set_cookie(
        key=settings.SECURITY_REFRESH_TOKEN_COOKIE_KEY,
        value=token,
        expires=settings.SECURITY_REFRESH_TOKEN_COOKIE_EXPIRES,
        path=settings.SECURITY_REFRESH_TOKEN_COOKIE_PATH,
        domain=settings.SECURITY_REFRESH_TOKEN_COOKIE_DOMAIN,
        httponly=settings.SECURITY_REFRESH_TOKEN_COOKIE_HTTPONLY,
        secure=settings.SECURITY_REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.SECURITY_REFRESH_TOKEN_COOKIE_SAMESITE,
    )


@router.post("/sign-up", response_model=TokenResponseSchema, status_code=status.HTTP_201_CREATED)
async def sign_up(
    response: Response,
    request: UserSchema,
    user: UserRepository = Depends(get_repository(UserRepository))
):
    """
    Реєстрація користувача
    <details>
    <summary>Докладніше</summary>

    **Параметри**

    - **name**: (str) Ім'я користувача
    - **username**: (str) Логін користувача
    - **password**: (str) Пароль користувача

    <details>
    <summary>Приклад</summary>
    ```python
    {
      "name": "ФОП Джонсонюк Борис",
      "username": "boris",
      "password": "boris1234"
    }
    ```
    </details>
    """
    await user.create(request)
    tokens = create_user_tokens(request.username)

    set_refresh_token_cookie(response, tokens.refresh_token)

    return {
        "access_token": tokens.access_token, "token_type": "bearer"
    }


@router.post("/create-token", response_model=TokenResponseSchema)
async def create_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user: UserRepository = Depends(get_repository(UserRepository)),
):
    """
    Авторизація
    <details>
    <summary>Докладніше</summary>

    **Параметри**

    - **username**: (str) Логін користувача
    - **password**: (str) Пароль користувача

    <details>
    <summary>Приклад</summary>
    ```python
    username = "boris"
    ```
    ```python
    password = "boris1234"
    ```
    </details>
    """
    role = await user.get_by_username(form_data.username)

    if role is None or not verify_password(form_data.password, role.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    tokens = create_user_tokens(form_data.username)

    set_refresh_token_cookie(response, tokens.refresh_token)

    return {"access_token": tokens.access_token, "token_type": "bearer"}


@router.post("/refresh", name="auth:refresh")
async def refresh(response: Response, token: str | None = Cookie(None)):
    """
    Оновлення токена, береться із cookie, тому не обов'язково напряму заповняти
    <details>
    <summary>Докладніше</summary>

    **Параметри**

    - **token**: (str, optional) Refresh token

    <details>
    <summary>Приклад</summary>
    ```python
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSld"
    ```
    </details>
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = decode(token)

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    tokens = create_user_tokens(username)

    set_refresh_token_cookie(response, tokens.refresh_token)

    return {"access_token": tokens.access_token, "token_type": "bearer"}
