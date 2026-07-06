from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.models.merma import Merma
from app.repositories.causa_merma_repository import CausaMermaRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.merma_repository import MermaRepository
from app.repositories.operacion_productiva_repository import OperacionProductivaRepository
from app.repositories.pileta_repository import PiletaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.movimiento_fisico_service import MovimientoFisicoService
from app.services.stock_service import StockService


class MermaService:
    """Registra mermas y su salida fisica correspondiente."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.merma_repository = MermaRepository(session)
        self.operacion_repository = OperacionProductivaRepository(session)
        self.lote_repository = LoteRepository(session)
        self.pileta_repository = PiletaRepository(session)
        self.causa_repository = CausaMermaRepository(session)
        self.usuario_repository = UsuarioRepository(session)
        self.stock_service = StockService(session)
        self.movimiento_service = MovimientoFisicoService(session)

    def registrar_merma(
        self,
        *,
        operacion_productiva_id: int,
        lote_id: int,
        pileta_id: int,
        causa_merma_id: int,
        responsable_id: int,
        litros: Decimal,
        fecha: datetime,
        observaciones: str | None = None,
    ) -> Merma:
        self.stock_service.bloquear_stock_operacion(
            lote_id,
            pileta_origen_id=pileta_id,
        )
        self._validar_merma(
            operacion_productiva_id=operacion_productiva_id,
            lote_id=lote_id,
            pileta_id=pileta_id,
            causa_merma_id=causa_merma_id,
            responsable_id=responsable_id,
            litros=litros,
        )

        merma = Merma(
            operacion_productiva_id=operacion_productiva_id,
            lote_id=lote_id,
            pileta_id=pileta_id,
            causa_merma_id=causa_merma_id,
            responsable_id=responsable_id,
            litros=litros,
            fecha=fecha,
            observaciones=observaciones,
        )

        try:
            merma = self.merma_repository.add(merma)
            self.movimiento_service.registrar_movimiento(
                operacion_productiva_id=operacion_productiva_id,
                lote_id=lote_id,
                responsable_id=responsable_id,
                fecha=fecha,
                litros=litros,
                estado="registrado",
                pileta_origen_id=pileta_id,
                observaciones=observaciones,
                commit=False,
            )
            self.session.commit()
            self.session.refresh(merma)
            return merma
        except Exception:
            self.session.rollback()
            raise

    def _validar_merma(
        self,
        *,
        operacion_productiva_id: int,
        lote_id: int,
        pileta_id: int,
        causa_merma_id: int,
        responsable_id: int,
        litros: Decimal,
    ) -> None:
        if litros <= 0:
            raise BusinessRuleError("Los litros de la merma deben ser mayores a cero.")
        if self.operacion_repository.get_by_id(operacion_productiva_id) is None:
            raise NotFoundError("Operacion productiva no encontrada.")
        if self.lote_repository.get_by_id(lote_id) is None:
            raise NotFoundError("Lote no encontrado.")
        if self.pileta_repository.get_by_id(pileta_id) is None:
            raise NotFoundError("Pileta no encontrada.")
        if self.causa_repository.get_by_id(causa_merma_id) is None:
            raise NotFoundError("Causa de merma no encontrada.")
        if self.usuario_repository.get_by_id(responsable_id) is None:
            raise NotFoundError("Usuario responsable no encontrado.")
        if not self.stock_service.validar_stock_disponible(lote_id, pileta_id, litros):
            raise BusinessRuleError("Stock insuficiente para registrar la merma.")
