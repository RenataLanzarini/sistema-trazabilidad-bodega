from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MermaCreate(BaseModel):
    operacion_productiva_id: int
    lote_id: int
    pileta_id: int
    causa_merma_id: int
    responsable_id: int
    litros: Decimal = Field(gt=0)
    fecha: datetime
    observaciones: str | None = None


class MermaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    operacion_productiva_id: int
    lote_id: int
    pileta_id: int | None
    causa_merma_id: int
    responsable_id: int
    litros: Decimal
    fecha: datetime
    observaciones: str | None
    created_at: datetime
    updated_at: datetime
