from datetime import datetime
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.movimiento_fisico import MovimientoFisico
from app.repositories.movimiento_fisico_repository import MovimientoFisicoRepository


class StockService:
    """Calcula stock desde movimientos fisicos, unica fuente de verdad del stock."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.movimiento_repository = MovimientoFisicoRepository(session)

    def bloquear_stock_operacion(
        self,
        lote_id: int,
        *,
        pileta_origen_id: int | None = None,
        pileta_destino_id: int | None = None,
    ) -> None:
        lock_keys = []
        if pileta_origen_id is not None:
            lock_keys.extend(
                [
                    self._stock_lock_key(lote_id, pileta_origen_id),
                    self._pileta_lock_key(pileta_origen_id),
                ]
            )
        if pileta_destino_id is not None:
            lock_keys.extend(
                [
                    self._stock_lock_key(lote_id, pileta_destino_id),
                    self._pileta_lock_key(pileta_destino_id),
                ]
            )

        self._bloquear_claves(lock_keys)

    def bloquear_consumos(self, consumos: list[tuple[int, int]]) -> None:
        lock_keys = []
        for lote_id, pileta_id in consumos:
            lock_keys.extend(
                [
                    self._stock_lock_key(lote_id, pileta_id),
                    self._pileta_lock_key(pileta_id),
                ]
            )

        self._bloquear_claves(lock_keys)

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

    def _bloquear_claves(self, lock_keys: list[str]) -> None:
        for lock_key in sorted(set(lock_keys)):
            self.session.execute(
                text("SELECT pg_advisory_xact_lock(hashtext(:lock_key))"),
                {"lock_key": lock_key},
            )

    def _stock_lock_key(self, lote_id: int, pileta_id: int) -> str:
        return f"stock:lote:{lote_id}:pileta:{pileta_id}"

    def _pileta_lock_key(self, pileta_id: int) -> str:
        return f"stock:pileta:{pileta_id}"
