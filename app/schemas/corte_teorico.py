from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CorteTeoricoDetalleCreate(BaseModel):
    pileta_id: int | None = None
    lote_id: int | None = None
    codigo_externo: str | None = None
    volumen_al_corte: Decimal | None = None
    varietal_snapshot: str | None = None
    volumen_actual_snapshot: Decimal | None = None
    alcohol: Decimal | None = None
    acidez_volatil: Decimal | None = None
    acidez_total: Decimal | None = None
    ph: Decimal | None = None
    so2_libre: Decimal | None = None
    so2_total: Decimal | None = None

    @model_validator(mode="after")
    def validar_payload_no_vacio(self) -> "CorteTeoricoDetalleCreate":
        if all(value is None for value in self.model_dump().values()):
            raise ValueError("El detalle del corte teorico debe contener al menos un dato.")
        return self


class CorteTeoricoCreate(BaseModel):
    responsable_id: int | None = None
    operacion_productiva_id: int | None = None
    codigo_externo: str | None = None
    fecha: date | None = None
    nombre: str | None = None
    observaciones: str | None = None
    detalles: list[CorteTeoricoDetalleCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validar_payload_no_vacio(self) -> "CorteTeoricoCreate":
        values = self.model_dump()
        detalles = values.pop("detalles")
        if not detalles and all(value is None for value in values.values()):
            raise ValueError("El corte teorico debe contener al menos un dato.")
        return self


class CorteTeoricoVincularOperacion(BaseModel):
    operacion_productiva_id: int | None


class CorteTeoricoDetalleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    corte_teorico_id: int
    pileta_id: int | None
    lote_id: int | None
    codigo_externo: str | None
    volumen_al_corte: Decimal | None
    varietal_snapshot: str | None
    volumen_actual_snapshot: Decimal | None
    alcohol: Decimal | None
    acidez_volatil: Decimal | None
    acidez_total: Decimal | None
    ph: Decimal | None
    so2_libre: Decimal | None
    so2_total: Decimal | None
    created_at: datetime
    updated_at: datetime


class CorteTeoricoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    responsable_id: int | None
    operacion_productiva_id: int | None
    codigo_externo: str | None
    fecha: date | None
    nombre: str | None
    observaciones: str | None
    created_at: datetime
    updated_at: datetime
