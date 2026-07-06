from fastapi import APIRouter

from app.api.routes.v1 import (
    catalogos,
    health,
    lotes,
    operaciones_productivas,
    piletas,
    recepciones_uva,
    stock,
    trazabilidad,
)


router = APIRouter()
router.include_router(health.router)
router.include_router(catalogos.router)
router.include_router(recepciones_uva.router)
router.include_router(lotes.router)
router.include_router(piletas.router)
router.include_router(stock.router)
router.include_router(trazabilidad.router)
router.include_router(operaciones_productivas.router)
