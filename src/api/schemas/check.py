from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import conint
from pydantic import condecimal
from pydantic import root_validator


class ProductSchema(BaseModel):
    name: str
    price: condecimal(gt=Decimal('0'))
    quantity: conint(gt=0)

    @root_validator
    def compute_total_price(cls, values):
        values['total'] = values['price'] * values['quantity']
        return values


class PaymentSchema(BaseModel):
    type: Literal['cash', 'cashless']
    amount: Decimal


class CheckSchema(BaseModel):
    products: list[ProductSchema]
    payment: PaymentSchema

    @property
    def total(self):
        return sum([product.total for product in self.products])

    @property
    def rest(self):
        return self.payment.amount - self.total


class CheckResponseSchema(CheckSchema):
    id: int
    total_: Decimal = Field(..., alias='total')
    rest_: Decimal = Field(..., alias='rest')
    created_at: datetime

    class Config:
        orm_mode = True


class FilterSchema(BaseModel):
    field: str
    op: Literal["gt", "lt", "eq"]
    value: Decimal | datetime | str


class QueryParamsSchema(BaseModel):
    limit: int | None = None
    offset: int | None = None
    filters: list[FilterSchema] | None = None
