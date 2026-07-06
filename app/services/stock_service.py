from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.movimiento_fisico import MovimientoFisico
from app.repositories.movimiento_fisico_repository import MovimientoFisicoRepository


class StockService:
    """Calcula stock desde movimientos fisicos, unica fuente de verdad del stock."""

    def __init__(self, session: Session) -> None:
        self.movimiento_repository = MovimientoFisicoRepository(session)

    def calcular_stock_actual_por_pileta(self, pileta_id: int) -> Decimal:
        movimientos = self.movimiento_repository.list_by_pileta(pileta_id)
        return self._calcular_stock(movimientos, pileta_id=pileta_id)

    def calcular_stock_actual_por_lote(self, lote_id: int) -> Decimal:
        movimientos = self.movimiento_repository.list_by_lote(lote_id)
        return self._calcular_stock(movimientos, lote_id=lote_id)

    def calcular_stock_por_lote_y_pileta(self, lote_id: int, pileta_id: int) -> Decimal:
        movimientos = self.movimiento_repository.list_by_lote(lote_id)
        return self._calcular_stock(movimientos, lote_id=lote_id, pileta_id=pileta_id)

    def calcular_stock_historico_hasta(
        self,
        fecha: datetime,
        *,
        lote_id: int | None = None,
        pileta_id: int | None = None,
    ) -> Decimal:
        movimientos = self.movimiento_repository.list_until_fecha(fecha)
        return self._calcular_stock(movimientos, lote_id=lote_id, pileta_id=pileta_id)

    def validar_stock_disponible(
        self,
        lote_id: int,
        pileta_id: int,
        litros: Decimal,
        *,
        fecha: datetime | None = None,
    ) -> bool:
        stock = (
            self.calcular_stock_historico_hasta(fecha, lote_id=lote_id, pileta_id=pileta_id)
            if fecha is not None
            else self.calcular_stock_por_lote_y_pileta(lote_id, pileta_id)
        )
        return stock >= litros

    def _calcular_stock(
        self,
        movimientos: list[MovimientoFisico],
        *,
        lote_id: int | None = None,
        pileta_id: int | None = None,
    ) -> Decimal:
        stock = Decimal("0")
        for movimiento in movimientos:
            if lote_id is not None and movimiento.lote_id != lote_id:
                continue

            if pileta_id is None:
                stock += self._impacto_en_lote(movimiento)
                continue

            if movimiento.pileta_destino_id == pileta_id:
                stock += movimiento.litros
            if movimiento.pileta_origen_id == pileta_id:
                stock -= movimiento.litros

        return stock

    def _impacto_en_lote(self, movimiento: MovimientoFisico) -> Decimal:
        if movimiento.pileta_destino_id is not None and movimiento.pileta_origen_id is None:
            return movimiento.litros
        if movimiento.pileta_origen_id is not None and movimiento.pileta_destino_id is None:
            return -movimiento.litros
        return Decimal("0")
