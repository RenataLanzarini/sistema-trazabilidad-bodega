from fastapi import APIRouter

from app.api.routes.v1 import (
    analisis_enologicos,
    auth,
    catalogos,
    cortes_teoricos,
    fraccionamientos,
    health,
    lotes,
    mermas,
    mediciones_fermentacion,
    movimientos_fisicos,
    operaciones_productivas,
    ordenes_trabajo,
    piletas,
    productos_terminados,
    recepciones_uva,
    stock,
    trazabilidad,
    ventas_granel,
)


router = APIRouter()
router.include_router(health.router)
router.include_router(auth.router)
router.include_router(analisis_enologicos.router)
router.include_router(mediciones_fermentacion.router)
router.include_router(ordenes_trabajo.router)
router.include_router(cortes_teoricos.router)
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
