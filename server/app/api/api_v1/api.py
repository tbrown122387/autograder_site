from app.api.api_v1.endpoints import auth, grading
from app.core.config import settings
from fastapi import APIRouter

api_router = APIRouter(prefix=settings.API_V1_STR)
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(grading.router)
