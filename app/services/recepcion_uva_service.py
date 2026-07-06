from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.models.origen_uva import OrigenUva
from app.models.recepcion_uva import RecepcionUva
from app.repositories.bodega_repository import BodegaRepository
from app.repositories.recepcion_uva_repository import RecepcionUvaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.variedad_repository import VariedadRepository
from app.schemas.recepcion_uva import RecepcionUvaCreate


class RecepcionUvaService:
    """Gestiona creacion basica de recepciones de uva sin movimientos de stock."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.recepcion_repository = RecepcionUvaRepository(session)
        self.bodega_repository = BodegaRepository(session)
        self.variedad_repository = VariedadRepository(session)
        self.usuario_repository = UsuarioRepository(session)

    def crear_recepcion(self, data: RecepcionUvaCreate) -> RecepcionUva:
        self._validar_recepcion(data)
        recepcion = RecepcionUva(**data.model_dump())

        try:
            recepcion = self.recepcion_repository.add(recepcion)
            self.session.commit()
            self.session.refresh(recepcion)
            return recepcion
        except IntegrityError as exc:
            self.session.rollback()
            raise ConflictError("Ya existe una recepcion de uva con esos datos.") from exc
        except Exception:
            self.session.rollback()
            raise

    def _validar_recepcion(self, data: RecepcionUvaCreate) -> None:
        if not data.numero_ciu.strip():
            raise BusinessRuleError("El numero CIU es obligatorio.")
        if not data.estado.strip():
            raise BusinessRuleError("El estado de la recepcion es obligatorio.")
        if self.bodega_repository.get_by_id(data.bodega_id) is None:
            raise NotFoundError("Bodega no encontrada.")
        if self.session.get(OrigenUva, data.origen_uva_id) is None:
            raise NotFoundError("Origen de uva no encontrado.")
        if self.variedad_repository.get_by_id(data.variedad_id) is None:
            raise NotFoundError("Variedad no encontrada.")
        if self.usuario_repository.get_by_id(data.responsable_id) is None:
            raise NotFoundError("Usuario responsable no encontrado.")
