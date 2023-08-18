from fastapi import APIRouter
from fastapi import Depends
from fastapi import Security
from fastapi import responses
from starlette import status

from src.api.dependencies.db import get_repository
from src.api.dependencies.security import get_current_user
from src.api.schemas.check import CheckResponseSchema
from src.api.schemas.check import CheckSchema
from src.api.schemas.check import FilterSchema
from src.api.schemas.check import QueryParamsSchema
from src.lib.printer import Printer
from src.repositories.check import CheckRepository

router = APIRouter()


@router.post("/create", response_model=CheckResponseSchema, status_code=status.HTTP_201_CREATED)
async def create(
    check_in: CheckSchema,
    repo: CheckRepository = Depends(get_repository(CheckRepository)),
    user: str = Security(get_current_user)
):
    """
    Створення чека
    <details>
    <summary>Докладніше</summary>

    **Параметри**

    - products: (list[dict]) список структур
        + **name**: (str) Назва товара
        + **price**: (decimal) Ціна
        + **quantity**: (int) Кількість
    - payment: (dict) структура
        + **type**: (str) Тип оплати
        + **amount**: (decimal) Сума

    <details>
    <summary>Приклад</summary>
    ```python
       {
          "products": [
            {
              "name": "Phone",
              "price": 200,
              "quantity": 2
            }
          ],
          "payment": {
            "type": "cash",
            "amount": 1000
          }
      }
    ```
    </details>
    """
    check = await repo.create(check_in, user)
    return {
        "id": check.id,
        "created_at": check.created_at,
        "rest": check_in.rest,
        "total": check_in.total,
        **check_in.dict()
    }


@router.post(
    "/list",
    response_model=list[CheckResponseSchema]
)
async def read(
    request: QueryParamsSchema,
    repo: CheckRepository = Depends(get_repository(CheckRepository)),
    user: str = Security(get_current_user)
):
    """
    Перегляд чеків для користувача
    <details>
    <summary>Докладніше</summary>

    **Параметри**

    - **limit**: (int) Ліміт
    - **offset**: (int) З якого елемента

    - filters: (list[dict]) список структур
        + **field**: (str) Назва колонки
        + **op**: (str) Оператор
        + **value**: (int, str, Decimal) Значення

    <details>
    <summary>Приклад</summary>
    ```python
       {
          "limit": 10,
          "offset": 0,
          "filters": [
            {
              "field": "rest",
              "op": "gt",
              "value": 1000
            }
          ]
       }
    ```
    </details>
    """
    return await repo.filter(
        username=user,
        filters=request.filters,
        limit=request.limit,
        offset=request.offset
    )


@router.get("/retrieve/{pk}")
async def retrieve(pk: int, repo: CheckRepository = Depends(get_repository(CheckRepository))):
    """
    Перегляд для неавторизованих користувачів
    <details>
    <summary>Докладніше</summary>

    **Параметри**

    - **pk**: (int) Ідентифікатор чеків

    <details>
    <summary>Приклад</summary>
    ```python
        pk=1
    ```
    </details>
    """
    check = await repo.filter(
        filters=[FilterSchema(field="id", op="eq", value=pk)], limit=1, use_list=False
    )
    return responses.PlainTextResponse(
        Printer(
            check.user,
            check.rest,
            check.total,
            check.payment["amount"],
            check.products,
            check.created_at
        ).render()
    )
