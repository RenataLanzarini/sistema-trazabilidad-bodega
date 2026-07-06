from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class MedicionFermentacionCreate(BaseModel):
    bodega_id: int
    pileta_id: int | None = None
    lote_id: int | None = None
    codigo_externo: str | None = None
    fecha: date | None = None
    turno: str | None = None
    grado_baume: Decimal | None = None
    temperatura: Decimal | None = None


class MedicionFermentacionRead(MedicionFermentacionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
