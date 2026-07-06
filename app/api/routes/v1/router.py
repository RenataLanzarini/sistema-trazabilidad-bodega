from fastapi import APIRouter

from app.api.routes.v1 import catalogos, health


router = APIRouter()
router.include_router(health.router)
router.include_router(catalogos.router)
