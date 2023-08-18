from sqlalchemy import select

from src.models.user import User
from src.repositories import BaseRepository
from src.api.schemas.user import UserSchema


class UserRepository(BaseRepository):
    async def create(self, user: UserSchema):
        self.dbsession.add(User(**user.dict()))
        await self.dbsession.commit()

    async def get_by_username(self, username: str):
        user = await self.dbsession.execute(
            select(User).where(User.username == username)
        )
        return user.scalar()
