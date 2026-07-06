from datetime import date, datetime, time
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.schemas.venta_granel import (
    VentaGranelCreate,
    VentaGranelDetalleRead,
    VentaGranelRead,
)
from app.services.venta_granel_service import VentaGranelService


router = APIRouter(prefix="/ventas-granel", tags=["ventas-granel"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=VentaGranelRead, status_code=201)
def crear_venta_granel(data: VentaGranelCreate, db: DbSession) -> object:
    payload = data.model_dump()
    payload["detalles"] = [detalle.model_dump() for detalle in data.detalles]
    return VentaGranelService(db).crear_venta_granel(**payload)


@router.get("/cliente/{cliente_id}", response_model=list[VentaGranelRead])
def listar_ventas_por_cliente(cliente_id: int, db: DbSession) -> list[object]:
    return VentaGranelService(db).listar_por_cliente(cliente_id)


@router.get("/fecha/{fecha}", response_model=list[VentaGranelRead])
def listar_ventas_por_fecha(fecha: date, db: DbSession) -> list[object]:
    fecha_desde = datetime.combine(fecha, time.min)
    fecha_hasta = datetime.combine(fecha, time.max)
    return VentaGranelService(db).listar_por_fecha(fecha_desde, fecha_hasta)


@router.get("/responsable/{responsable_id}", response_model=list[VentaGranelRead])
def listar_ventas_por_responsable(responsable_id: int, db: DbSession) -> list[object]:
    return VentaGranelService(db).listar_por_responsable(responsable_id)


@router.get("/operacion/{operacion_id}", response_model=list[VentaGranelRead])
def listar_ventas_por_operacion(operacion_id: int, db: DbSession) -> list[object]:
    return VentaGranelService(db).listar_por_operacion(operacion_id)


@router.get("/{venta_granel_id}/detalles", response_model=list[VentaGranelDetalleRead])
def listar_detalles_por_venta(venta_granel_id: int, db: DbSession) -> list[object]:
    return VentaGranelService(db).listar_detalles_por_venta(venta_granel_id)
