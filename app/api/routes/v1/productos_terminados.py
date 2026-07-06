from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.schemas.producto_terminado import ProductoTerminadoRead
from app.services.producto_terminado_service import ProductoTerminadoService


router = APIRouter(prefix="/productos-terminados", tags=["productos-terminados"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[ProductoTerminadoRead])
def listar_productos_terminados(db: DbSession) -> list[object]:
    return ProductoTerminadoService(db).listar()


@router.get("/codigo/{codigo}", response_model=ProductoTerminadoRead)
def obtener_producto_terminado_por_codigo(codigo: str, db: DbSession) -> object:
    return ProductoTerminadoService(db).obtener_por_codigo(codigo)


@router.get("/lote/{lote_id}", response_model=list[ProductoTerminadoRead])
def listar_productos_terminados_por_lote(lote_id: int, db: DbSession) -> list[object]:
    return ProductoTerminadoService(db).listar_por_lote(lote_id)


@router.get("/fraccionamiento/{fraccionamiento_id}", response_model=list[ProductoTerminadoRead])
def listar_productos_terminados_por_fraccionamiento(
    fraccionamiento_id: int,
    db: DbSession,
) -> list[object]:
    return ProductoTerminadoService(db).listar_por_fraccionamiento(fraccionamiento_id)


@router.get("/fecha/{fecha}", response_model=list[ProductoTerminadoRead])
def listar_productos_terminados_por_fecha(fecha: date, db: DbSession) -> list[object]:
    return ProductoTerminadoService(db).listar_por_fecha_produccion(fecha, fecha)


@router.get("/{producto_terminado_id}", response_model=ProductoTerminadoRead)
def obtener_producto_terminado(producto_terminado_id: int, db: DbSession) -> object:
    return ProductoTerminadoService(db).obtener_por_id(producto_terminado_id)
