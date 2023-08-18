from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings


# Create engines
async_engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), **{"echo": False, "future": True}
)

# Create sessions
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
