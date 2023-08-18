from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import sql

from src.models.check import Check
from src.repositories import BaseRepository
from src.lib.data_conversion import json2dict
from src.api.schemas.check import CheckSchema
from src.api.schemas.check import FilterSchema


class CheckRepository(BaseRepository):
    async def create(self, check_in: CheckSchema, user) -> Check:
        check = Check(
            user=user,
            rest=check_in.rest,
            total=check_in.total,
            amount=check_in.payment.amount,
            type=check_in.payment.type,
            order_details=json2dict(check_in.json(), "payment")
        )
        self.dbsession.add(check)
        await self.dbsession.commit()
        return check

    async def filter(
        self,
        *,
        username: str | None = None,
        filters: list[FilterSchema] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        use_list: bool = True
    ):
        query = select(
            Check.id,
            Check.user,
            Check.total,
            Check.rest,
            Check.created_at,
            Check.order_details.op("->")("products").label("products"),
            func.json_build_object("amount", Check.amount, "type",  Check.type).label("payment")
        )

        if username is not None:
            query = query.where(Check.user == username)

        if filters is not None:
            query = query.where(
                *[
                    getattr(sql.operators, i.op)(getattr(Check, i.field), i.value)
                    for i in filters
                ]
            )

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        res = await self.dbsession.execute(query)

        if use_list:
            return res.mappings().all()
        return res.one()
