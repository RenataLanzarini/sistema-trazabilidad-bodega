from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.models.lote import Lote
from app.repositories.bodega_repository import BodegaRepository
from app.repositories.calificacion_vino_repository import CalificacionVinoRepository
from app.repositories.estado_lote_repository import EstadoLoteRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.recepcion_uva_repository import RecepcionUvaRepository
from app.repositories.tipo_producto_repository import TipoProductoRepository
from app.repositories.variedad_repository import VariedadRepository
from app.schemas.lote import LoteCreate


class LoteService:
    """Gestiona creacion basica de lotes sin genealogia ni movimientos."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.lote_repository = LoteRepository(session)
        self.bodega_repository = BodegaRepository(session)
        self.tipo_producto_repository = TipoProductoRepository(session)
        self.estado_lote_repository = EstadoLoteRepository(session)
        self.recepcion_repository = RecepcionUvaRepository(session)
        self.variedad_repository = VariedadRepository(session)
        self.calificacion_repository = CalificacionVinoRepository(session)

    def crear_lote(self, data: LoteCreate) -> Lote:
        self._validar_lote(data)
        lote = Lote(**data.model_dump())

        try:
            lote = self.lote_repository.add(lote)
            self.session.commit()
            self.session.refresh(lote)
            return lote
        except IntegrityError as exc:
            self.session.rollback()
            raise ConflictError("Ya existe un lote con esos datos.") from exc
        except Exception:
            self.session.rollback()
            raise

    def _validar_lote(self, data: LoteCreate) -> None:
        if not data.codigo.strip():
            raise BusinessRuleError("El codigo del lote es obligatorio.")
        if self.bodega_repository.get_by_id(data.bodega_id) is None:
            raise NotFoundError("Bodega no encontrada.")
        if self.tipo_producto_repository.get_by_id(data.tipo_producto_id) is None:
            raise NotFoundError("Tipo de producto no encontrado.")
        if self.estado_lote_repository.get_by_id(data.estado_lote_id) is None:
            raise NotFoundError("Estado de lote no encontrado.")
        if (
            data.recepcion_uva_id is not None
            and self.recepcion_repository.get_by_id(data.recepcion_uva_id) is None
        ):
            raise NotFoundError("Recepcion de uva no encontrada.")
        if (
            data.variedad_principal_id is not None
            and self.variedad_repository.get_by_id(data.variedad_principal_id) is None
        ):
            raise NotFoundError("Variedad principal no encontrada.")
        if (
            data.calificacion_vino_id is not None
            and self.calificacion_repository.get_by_id(data.calificacion_vino_id) is None
        ):
            raise NotFoundError("Calificacion de vino no encontrada.")
