from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductoTerminadoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fraccionamiento_id: int
    tipo_producto_id: int
    lote_id: int
    codigo: str
    cantidad_unidades: int
    volumen_unidad_ml: int
    litros_totales: Decimal
    fecha_produccion: date
    estado: str
    observaciones: str | None
    created_at: datetime
    updated_at: datetime
