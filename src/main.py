from fastapi import FastAPI

from sqlalchemy.exc import IntegrityError

from src.config import settings
from src.api.endpoints import router
from src.errors import global_error_handler
from src.errors import integrity_error_handler


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION
    )

    # include routers
    application.include_router(router)

    # register error handlers
    application.add_exception_handler(IntegrityError, integrity_error_handler)
    application.add_exception_handler(Exception, global_error_handler)

    if settings.DEBUG:
        async def init_tables():
            from src.models import async_engine
            from src.models.base import Base
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

        # application.add_event_handler("startup", init_tables)

    return application


app = get_application()
