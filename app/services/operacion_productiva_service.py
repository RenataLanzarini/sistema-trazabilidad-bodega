from datetime import datetime

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.models.operacion_productiva import OperacionProductiva
from app.repositories.bodega_repository import BodegaRepository
from app.repositories.operacion_productiva_repository import OperacionProductivaRepository
from app.repositories.tipo_operacion_repository import TipoOperacionRepository
from app.repositories.usuario_repository import UsuarioRepository


class OperacionProductivaService:
    """Coordina reglas basicas y persistencia de operaciones productivas."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.operacion_repository = OperacionProductivaRepository(session)
        self.bodega_repository = BodegaRepository(session)
        self.tipo_operacion_repository = TipoOperacionRepository(session)
        self.usuario_repository = UsuarioRepository(session)

    def crear_operacion(
        self,
        *,
        bodega_id: int,
        tipo_operacion_id: int,
        responsable_id: int,
        fecha: datetime,
        estado: str,
        codigo_externo: str | None = None,
        observaciones: str | None = None,
    ) -> OperacionProductiva:
        self._validar_estado(estado)
        self._validar_referencias(
            bodega_id=bodega_id,
            tipo_operacion_id=tipo_operacion_id,
            responsable_id=responsable_id,
        )
        operacion = OperacionProductiva(
            bodega_id=bodega_id,
            tipo_operacion_id=tipo_operacion_id,
            responsable_id=responsable_id,
            codigo_externo=codigo_externo,
            fecha=fecha,
            estado=estado,
            anulada=False,
            observaciones=observaciones,
        )
        try:
            operacion = self.operacion_repository.add(operacion)
            self.session.commit()
            self.session.refresh(operacion)
            return operacion
        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, operacion_id: int) -> OperacionProductiva:
        operacion = self.operacion_repository.get_by_id(operacion_id)
        if operacion is None:
            raise NotFoundError("Operacion productiva no encontrada.")
        return operacion

    def listar_por_bodega(self, bodega_id: int) -> list[OperacionProductiva]:
        return self.operacion_repository.list_by_bodega(bodega_id)

    def listar_por_tipo(self, tipo_operacion_id: int) -> list[OperacionProductiva]:
        return self.operacion_repository.list_by_tipo(tipo_operacion_id)

    def listar_por_fecha(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime | None = None,
    ) -> list[OperacionProductiva]:
        return self.operacion_repository.list_by_fecha(fecha_desde, fecha_hasta)

    def listar_por_responsable(self, responsable_id: int) -> list[OperacionProductiva]:
        return self.operacion_repository.list_by_responsable(responsable_id)

    def listar_anuladas(self) -> list[OperacionProductiva]:
        return self.operacion_repository.list_anuladas()

    def anular_operacion(
        self,
        operacion_id: int,
        *,
        motivo_anulacion: str,
    ) -> OperacionProductiva:
        if not motivo_anulacion.strip():
            raise BusinessRuleError("El motivo de anulacion es obligatorio.")
        operacion = self.obtener_por_id(operacion_id)
        if operacion.anulada:
            raise BusinessRuleError("La operacion productiva ya se encuentra anulada.")

        try:
            operacion.anulada = True
            operacion.motivo_anulacion = motivo_anulacion
            self.session.flush()
            self.session.commit()
            self.session.refresh(operacion)
            return operacion
        except Exception:
            self.session.rollback()
            raise

    def _validar_estado(self, estado: str) -> None:
        if not estado or not estado.strip():
            raise BusinessRuleError("El estado de la operacion productiva es obligatorio.")

    def _validar_referencias(
        self,
        *,
        bodega_id: int,
        tipo_operacion_id: int,
        responsable_id: int,
    ) -> None:
        if self.bodega_repository.get_by_id(bodega_id) is None:
            raise NotFoundError("Bodega no encontrada.")
        if self.tipo_operacion_repository.get_by_id(tipo_operacion_id) is None:
            raise NotFoundError("Tipo de operacion no encontrado.")
        if self.usuario_repository.get_by_id(responsable_id) is None:
            raise NotFoundError("Usuario responsable no encontrado.")
