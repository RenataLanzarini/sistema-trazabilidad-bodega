from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AnalisisEnologicoCreate(BaseModel):
    bodega_id: int
    lote_id: int | None = None
    pileta_id: int | None = None
    codigo_externo: str | None = None
    fecha: date | None = None
    capacidad_litros: Decimal | None = None
    tipo: str | None = None
    alcohol: Decimal | None = None
    azucar: Decimal | None = None
    volatil: Decimal | None = None
    acidez_total: Decimal | None = None
    ph: Decimal | None = None
    anhidrido_libre: Decimal | None = None
    anhidrido_total: Decimal | None = None
    extracto_seco: Decimal | None = None
    absorbancia_420: Decimal | None = None
    absorbancia_520: Decimal | None = None
    absorbancia_620: Decimal | None = None
    intensidad: Decimal | None = None
    indice: Decimal | None = None
    suma_420_520_620: Decimal | None = None
    brix: Decimal | None = None
    oxigeno: Decimal | None = None
    observaciones: str | None = None


class AnalisisEnologicoRead(AnalisisEnologicoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
