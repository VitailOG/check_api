from typing import Type
from typing import Callable
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import async_session
from src.repositories import BaseRepository


async def get_dbsession() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


def get_repository(
        repository_type: Type[BaseRepository],
) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repository(
            dbsession: AsyncSession = Depends(get_dbsession),
    ) -> BaseRepository:
        return repository_type(dbsession)

    return _get_repository
