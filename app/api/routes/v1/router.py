from fastapi import APIRouter

from app.api.routes.v1 import (
    catalogos,
    fraccionamientos,
    health,
    lotes,
    mermas,
    movimientos_fisicos,
    operaciones_productivas,
    piletas,
    productos_terminados,
    recepciones_uva,
    stock,
    trazabilidad,
    ventas_granel,
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
router.include_router(movimientos_fisicos.router)
router.include_router(mermas.router)
router.include_router(fraccionamientos.router)
router.include_router(productos_terminados.router)
router.include_router(ventas_granel.router)
