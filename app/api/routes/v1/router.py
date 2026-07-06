from fastapi import APIRouter

from app.api.routes.v1 import catalogos, health, lotes, piletas, recepciones_uva


router = APIRouter()
router.include_router(health.router)
router.include_router(catalogos.router)
router.include_router(recepciones_uva.router)
router.include_router(lotes.router)
router.include_router(piletas.router)
