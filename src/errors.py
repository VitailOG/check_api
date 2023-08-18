from starlette import status
from starlette.requests import Request
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse


async def integrity_error_handler(_: Request, exc: IntegrityError) -> JSONResponse:
    return JSONResponse(
        {"errors": "The object exists"},
        status_code=status.HTTP_409_CONFLICT
    )


async def global_error_handler(_: Request, exc: Exception) -> JSONResponse:
    print('error')
    return JSONResponse(
        {"errors": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
