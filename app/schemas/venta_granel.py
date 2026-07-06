from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class VentaGranelDetalleCreate(BaseModel):
    lote_id: int
    pileta_id: int
    litros: Decimal = Field(gt=0)
    observaciones: str | None = None


class VentaGranelCreate(BaseModel):
    operacion_productiva_id: int
    cliente_id: int
    responsable_id: int
    fecha: datetime
    estado: str
    detalles: list[VentaGranelDetalleCreate]
    documento: str | None = None
    observaciones: str | None = None


class VentaGranelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    operacion_productiva_id: int
    cliente_id: int
    responsable_id: int
    fecha: datetime
    documento: str | None
    estado: str
    observaciones: str | None
    created_at: datetime
    updated_at: datetime


class VentaGranelDetalleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    venta_granel_id: int
    lote_id: int
    pileta_id: int
    litros: Decimal
    observaciones: str | None
    created_at: datetime
    updated_at: datetime
