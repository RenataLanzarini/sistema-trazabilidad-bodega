from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class LoteBase(BaseModel):
    bodega_id: int
    tipo_producto_id: int
    estado_lote_id: int
    codigo: str
    fecha_nacimiento: date
    recepcion_uva_id: int | None = None
    variedad_principal_id: int | None = None
    calificacion_vino_id: int | None = None
    cosecha: int | None = None
    color: str | None = None
    observaciones: str | None = None
    activo: bool = True


class LoteCreate(LoteBase):
    pass


class LoteRead(LoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
