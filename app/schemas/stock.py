from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class StockPiletaRead(BaseModel):
    pileta_id: int
    litros: Decimal


class StockLoteRead(BaseModel):
    lote_id: int
    litros: Decimal


class StockLotePiletaRead(BaseModel):
    lote_id: int
    pileta_id: int
    litros: Decimal


class StockHistoricoRead(BaseModel):
    fecha: datetime
    lote_id: int | None
    pileta_id: int | None
    litros: Decimal


class DisponibilidadStockRead(BaseModel):
    lote_id: int
    pileta_id: int
    litros_solicitados: Decimal
    disponible: bool
