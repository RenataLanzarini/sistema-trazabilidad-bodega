from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class RelacionGenealogicaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    operacion_productiva_id: int
    lote_padre_id: int
    lote_hijo_id: int
    litros_aportados: Decimal
    tipo_relacion: str
    observaciones: str | None
    created_at: datetime
    updated_at: datetime


class NodoTrazabilidadRead(BaseModel):
    lote_id: int


class AristaTrazabilidadRead(BaseModel):
    relacion_id: int
    operacion_productiva_id: int
    lote_padre_id: int
    lote_hijo_id: int
    litros_aportados: Decimal
    tipo_relacion: str


class GrafoTrazabilidadRead(BaseModel):
    nodos: list[NodoTrazabilidadRead]
    aristas: list[AristaTrazabilidadRead]
