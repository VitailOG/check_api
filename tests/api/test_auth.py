import operator as op

import pytest

from httpx import AsyncClient
from starlette import status


pytestmark = [pytest.mark.asyncio]


@pytest.mark.parametrize(
    "expected_status,contains,key",
    [
        (status.HTTP_201_CREATED, op.contains, "access_token"),
        (status.HTTP_409_CONFLICT, op.contains, "errors"),
    ]
)
async def test_sign_up(
    user_data: dict[str, str],
    aclient: AsyncClient,
    expected_status: int,
    contains: callable,
    key: str
):
    res = await aclient.post('/auth/sign-up', json=user_data)
    assert res.status_code == expected_status
    assert contains(res.json(), key)


async def test_create_token(user_data: dict[str, str], aclient: AsyncClient):
    del user_data['name']
    res = await aclient.post('/auth/create-token', data=user_data)

    assert res.status_code == status.HTTP_200_OK
    assert "token_type" in res.json()
    assert "access_token" in res.json()
    assert any([_ for _ in res.cookies if "token" == _])


async def test_refresh_token(user_data: dict[str, str], aclient: AsyncClient):
    del user_data['name']
    res_create = await aclient.post('/auth/create-token', data=user_data)
    res_refresh = await aclient.post('/auth/refresh', cookies={"token": res_create.cookies['token']})

    assert res_refresh.status_code == status.HTTP_200_OK
