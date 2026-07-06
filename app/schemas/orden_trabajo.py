from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, model_validator


class OrdenTrabajoCreate(BaseModel):
    tarea_orden_trabajo_id: int | None = None
    pileta_id: int | None = None
    lote_id: int | None = None
    operario_id: int | None = None
    operacion_productiva_id: int | None = None
    pileta_origen_id: int | None = None
    pileta_destino_id: int | None = None
    codigo_externo: str | None = None
    numero: str | None = None
    fecha: date | None = None
    volumen_lleno: Decimal | None = None
    variedad: str | None = None
    anio: int | None = None
    observaciones: str | None = None
    insumo: str | None = None
    cantidad: Decimal | None = None
    col1: str | None = None
    litros_a_trasegar: Decimal | None = None
    lleno_disponible: Decimal | None = None
    litros_por_cm: Decimal | None = None
    pasada_a_trazabilidad: bool | None = None
    completada: bool | None = None
    fecha_completada: datetime | None = None
    observaciones_completada: str | None = None
    so2l_real: Decimal | None = None

    @model_validator(mode="after")
    def validar_payload_no_vacio(self) -> "OrdenTrabajoCreate":
        if all(value is None for value in self.model_dump().values()):
            raise ValueError("La orden de trabajo debe contener al menos un dato.")
        return self


class OrdenTrabajoCompletar(BaseModel):
    fecha_completada: datetime
    observaciones_completada: str | None = None


class OrdenTrabajoVincularOperacion(BaseModel):
    operacion_productiva_id: int | None


class OrdenTrabajoRead(OrdenTrabajoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
