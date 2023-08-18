import pytest

from httpx import AsyncClient
from starlette import status

from src.lib.tokenizer import create_user_tokens
from src.api.schemas.check import CheckResponseSchema


pytestmark = [pytest.mark.asyncio]


@pytest.fixture
def token(user_data: dict[str, str]):
    token = create_user_tokens(user_data['username'])
    return token.access_token


async def test_create_check(token: str, aclient: AsyncClient):
    data = {
        "products": [
            {
                "name": "Phone",
                "price": 200,
                "quantity": 1
            }
        ],
        "payment": {
            "type": "cash",
            "amount": 1000
        }
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = await aclient.post('/check/create', json=data, headers=headers)

    assert res.status_code == status.HTTP_201_CREATED
    assert CheckResponseSchema(**res.json())


@pytest.mark.parametrize(
    "params,count",
    [
        (
            {
                "limit": None,
                "offset": None,
                "filters": [
                    {
                        "field": "rest",
                        "op": "eq",
                        "value": 1000
                    }
                ]
            },
            0
        ),
        (
            {
                "limit": None,
                "offset": None,
                "filters": [
                    {
                        "field": "rest",
                        "op": "lt",
                        "value": 1000
                    }
                ]
            },
            1
        ),
    ]
)
async def test_check_filter(token: str, aclient: AsyncClient, params, count):
    headers = {"Authorization": f"Bearer {token}"}
    res = await aclient.post('/check/list', json=params, headers=headers)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == count


async def test_retrieve(token: str, aclient: AsyncClient):
    d = {
        "limit": None,
        "offset": None,
        "filters": None
    }
    headers = {"Authorization": f"Bearer {token}"}

    res = await aclient.get('/check/retrieve/1')

    assert res.status_code == status.HTTP_200_OK
    assert "boris" in res.text
    assert "800.0" in res.text
