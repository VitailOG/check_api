from fastapi import APIRouter

from src.api.endpoints.auth import router as auth_router
from src.api.endpoints.check import router as check_router

router = APIRouter(prefix="/api/v1")
router.include_router(check_router, tags=["check"], prefix="/check")
router.include_router(auth_router, tags=["auth"], prefix="/auth")
