from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PiletaBase(BaseModel):
    bodega_id: int
    deposito_id: int
    estado_pileta_id: int
    codigo: str
    nombre: str
    capacidad_litros: Decimal = Field(gt=0)
    litros_por_cm: Decimal | None = Field(default=None, gt=0)
    material: str | None = None
    observaciones: str | None = None
    activa: bool = True


class PiletaCreate(PiletaBase):
    pass


class PiletaRead(PiletaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
