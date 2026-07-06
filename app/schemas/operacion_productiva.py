from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OperacionProductivaCreate(BaseModel):
    bodega_id: int
    tipo_operacion_id: int
    responsable_id: int
    fecha: datetime
    estado: str
    codigo_externo: str | None = None
    observaciones: str | None = None


class OperacionProductivaAnular(BaseModel):
    motivo_anulacion: str


class OperacionProductivaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    bodega_id: int
    tipo_operacion_id: int
    responsable_id: int
    codigo_externo: str | None
    fecha: datetime
    estado: str
    anulada: bool
    motivo_anulacion: str | None
    observaciones: str | None
    created_at: datetime
    updated_at: datetime
