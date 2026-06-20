from fastapi import APIRouter

from app.core.config import settings
from app.api.routes.nexon import router as nexon_router
from app.api.routes.health import router as health_router

api_router = APIRouter(prefix=settings.api_prefix)
api_router.include_router(health_router)
api_router.include_router(nexon_router)
