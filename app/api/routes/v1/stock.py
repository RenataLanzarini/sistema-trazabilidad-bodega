from datetime import datetime
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.schemas.stock import (
    DisponibilidadStockRead,
    StockHistoricoRead,
    StockLotePiletaRead,
    StockLoteRead,
    StockPiletaRead,
)
from app.services.stock_service import StockService


router = APIRouter(prefix="/stock", tags=["stock"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/piletas/{pileta_id}", response_model=StockPiletaRead)
def obtener_stock_por_pileta(pileta_id: int, db: DbSession) -> StockPiletaRead:
    litros = StockService(db).calcular_stock_actual_por_pileta(pileta_id)
    return StockPiletaRead(pileta_id=pileta_id, litros=litros)


@router.get("/lotes/{lote_id}", response_model=StockLoteRead)
def obtener_stock_por_lote(lote_id: int, db: DbSession) -> StockLoteRead:
    litros = StockService(db).calcular_stock_actual_por_lote(lote_id)
    return StockLoteRead(lote_id=lote_id, litros=litros)


@router.get("/lotes/{lote_id}/piletas/{pileta_id}", response_model=StockLotePiletaRead)
def obtener_stock_por_lote_y_pileta(
    lote_id: int,
    pileta_id: int,
    db: DbSession,
) -> StockLotePiletaRead:
    litros = StockService(db).calcular_stock_por_lote_y_pileta(lote_id, pileta_id)
    return StockLotePiletaRead(lote_id=lote_id, pileta_id=pileta_id, litros=litros)


@router.get("/historico", response_model=StockHistoricoRead)
def obtener_stock_historico(
    fecha: datetime,
    db: DbSession,
    lote_id: int | None = None,
    pileta_id: int | None = None,
) -> StockHistoricoRead:
    litros = StockService(db).calcular_stock_historico_hasta(
        fecha,
        lote_id=lote_id,
        pileta_id=pileta_id,
    )
    return StockHistoricoRead(
        fecha=fecha,
        lote_id=lote_id,
        pileta_id=pileta_id,
        litros=litros,
    )


@router.get("/validar-disponibilidad", response_model=DisponibilidadStockRead)
def validar_disponibilidad_stock(
    lote_id: int,
    pileta_id: int,
    litros: Annotated[Decimal, Query(gt=0)],
    db: DbSession,
) -> DisponibilidadStockRead:
    disponible = StockService(db).validar_stock_disponible(lote_id, pileta_id, litros)
    return DisponibilidadStockRead(
        lote_id=lote_id,
        pileta_id=pileta_id,
        litros_solicitados=litros,
        disponible=disponible,
    )
