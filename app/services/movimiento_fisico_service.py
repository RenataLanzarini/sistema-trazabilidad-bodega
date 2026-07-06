from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.models.movimiento_fisico import MovimientoFisico
from app.repositories.lote_repository import LoteRepository
from app.repositories.movimiento_fisico_repository import MovimientoFisicoRepository
from app.repositories.operacion_productiva_repository import OperacionProductivaRepository
from app.repositories.pileta_repository import PiletaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.stock_service import StockService


class MovimientoFisicoService:
    """Valida y registra movimientos fisicos de stock."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.movimiento_repository = MovimientoFisicoRepository(session)
        self.lote_repository = LoteRepository(session)
        self.pileta_repository = PiletaRepository(session)
        self.operacion_repository = OperacionProductivaRepository(session)
        self.usuario_repository = UsuarioRepository(session)
        self.stock_service = StockService(session)

    def registrar_movimiento(
        self,
        *,
        operacion_productiva_id: int,
        lote_id: int,
        responsable_id: int,
        fecha: datetime,
        litros: Decimal,
        estado: str,
        pileta_origen_id: int | None = None,
        pileta_destino_id: int | None = None,
        codigo_externo: str | None = None,
        observaciones: str | None = None,
    ) -> MovimientoFisico:
        self._validar_movimiento(
            operacion_productiva_id=operacion_productiva_id,
            lote_id=lote_id,
            responsable_id=responsable_id,
            litros=litros,
            estado=estado,
            pileta_origen_id=pileta_origen_id,
            pileta_destino_id=pileta_destino_id,
        )

        movimiento = MovimientoFisico(
            operacion_productiva_id=operacion_productiva_id,
            lote_id=lote_id,
            pileta_origen_id=pileta_origen_id,
            pileta_destino_id=pileta_destino_id,
            responsable_id=responsable_id,
            codigo_externo=codigo_externo,
            fecha=fecha,
            litros=litros,
            estado=estado,
            observaciones=observaciones,
        )

        try:
            movimiento = self.movimiento_repository.add(movimiento)
            self.session.commit()
            self.session.refresh(movimiento)
            return movimiento
        except Exception:
            self.session.rollback()
            raise

    def obtener_movimientos_por_lote(self, lote_id: int) -> list[MovimientoFisico]:
        return self.movimiento_repository.list_by_lote(lote_id)

    def obtener_movimientos_por_pileta(self, pileta_id: int) -> list[MovimientoFisico]:
        return self.movimiento_repository.list_by_pileta(pileta_id)

    def obtener_movimientos_por_operacion(
        self,
        operacion_productiva_id: int,
    ) -> list[MovimientoFisico]:
        return self.movimiento_repository.list_by_operacion(operacion_productiva_id)

    def _validar_movimiento(
        self,
        *,
        operacion_productiva_id: int,
        lote_id: int,
        responsable_id: int,
        litros: Decimal,
        estado: str,
        pileta_origen_id: int | None,
        pileta_destino_id: int | None,
    ) -> None:
        if litros <= 0:
            raise BusinessRuleError("Los litros del movimiento deben ser mayores a cero.")
        if not estado or not estado.strip():
            raise BusinessRuleError("El estado del movimiento fisico es obligatorio.")
        if pileta_origen_id is None and pileta_destino_id is None:
            raise BusinessRuleError("El movimiento debe tener pileta origen o destino.")
        if pileta_origen_id is not None and pileta_destino_id == pileta_origen_id:
            raise BusinessRuleError("La pileta origen y destino deben ser distintas.")

        if self.operacion_repository.get_by_id(operacion_productiva_id) is None:
            raise NotFoundError("Operacion productiva no encontrada.")
        if self.lote_repository.get_by_id(lote_id) is None:
            raise NotFoundError("Lote no encontrado.")
        if self.usuario_repository.get_by_id(responsable_id) is None:
            raise NotFoundError("Usuario responsable no encontrado.")
        if pileta_origen_id is not None and self.pileta_repository.get_by_id(pileta_origen_id) is None:
            raise NotFoundError("Pileta origen no encontrada.")
        if pileta_destino_id is not None and self.pileta_repository.get_by_id(pileta_destino_id) is None:
            raise NotFoundError("Pileta destino no encontrada.")

        if pileta_origen_id is not None:
            stock_disponible = self.stock_service.validar_stock_disponible(
                lote_id,
                pileta_origen_id,
                litros,
            )
            if not stock_disponible:
                raise BusinessRuleError("Stock insuficiente en la pileta origen.")
