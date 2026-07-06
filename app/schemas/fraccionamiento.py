from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FraccionamientoDetalleCreate(BaseModel):
    lote_id: int
    pileta_id: int
    litros_consumidos: Decimal = Field(gt=0)
    observaciones: str | None = None


class FraccionamientoCreate(BaseModel):
    operacion_productiva_id: int
    responsable_id: int
    fecha: datetime
    estado: str
    detalles: list[FraccionamientoDetalleCreate]
    productos_terminados: list[dict[str, Any]] = Field(default_factory=list)
    observaciones: str | None = None


class FraccionamientoDetalleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fraccionamiento_id: int
    lote_id: int
    pileta_id: int
    litros_consumidos: Decimal
    observaciones: str | None
    created_at: datetime
    updated_at: datetime


class FraccionamientoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    operacion_productiva_id: int
    responsable_id: int
    fecha: datetime
    estado: str
    observaciones: str | None
    created_at: datetime
    updated_at: datetime
