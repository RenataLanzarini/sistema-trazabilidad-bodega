from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class RecepcionUvaBase(BaseModel):
    bodega_id: int
    origen_uva_id: int
    variedad_id: int
    responsable_id: int
    numero_ciu: str
    fecha: date
    cosecha: int
    kilos_recibidos: Decimal = Field(gt=0)
    estado: str
    semana: int | None = None
    rto: Decimal | None = None
    finca: str | None = None
    inv: str | None = None
    cambio: str | None = None
    cuartel: str | None = None
    tachos: int | None = None
    chofer: str | None = None
    cuit_cuil: str | None = None
    camion: str | None = None
    modelo: str | None = None
    patente: str | None = None
    bruto_kg: Decimal | None = None
    tara_kg: Decimal | None = None
    neto_kg: Decimal | None = None
    uva_real_kg: Decimal | None = None
    destino_vino: str | None = None
    brix_real: Decimal | None = None
    tenor_azucar: Decimal | None = None
    vasija: str | None = None
    observaciones: str | None = None


class RecepcionUvaCreate(RecepcionUvaBase):
    pass


class RecepcionUvaRead(RecepcionUvaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
