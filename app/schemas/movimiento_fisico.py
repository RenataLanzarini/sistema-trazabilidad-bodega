from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MovimientoFisicoCreate(BaseModel):
    operacion_productiva_id: int
    lote_id: int
    responsable_id: int
    fecha: datetime
    litros: Decimal = Field(gt=0)
    estado: str
    pileta_origen_id: int | None = None
    pileta_destino_id: int | None = None
    codigo_externo: str | None = None
    observaciones: str | None = None


class MovimientoFisicoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    operacion_productiva_id: int
    lote_id: int
    pileta_origen_id: int | None
    pileta_destino_id: int | None
    responsable_id: int
    codigo_externo: str | None
    fecha: datetime
    litros: Decimal
    estado: str
    observaciones: str | None
    created_at: datetime
    updated_at: datetime
