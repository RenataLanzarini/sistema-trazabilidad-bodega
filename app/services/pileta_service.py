from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.models.pileta import Pileta
from app.repositories.bodega_repository import BodegaRepository
from app.repositories.deposito_repository import DepositoRepository
from app.repositories.estado_pileta_repository import EstadoPiletaRepository
from app.repositories.pileta_repository import PiletaRepository
from app.schemas.pileta import PiletaCreate


class PiletaService:
    """Gestiona creacion basica de piletas sin calculos de stock."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.pileta_repository = PiletaRepository(session)
        self.bodega_repository = BodegaRepository(session)
        self.deposito_repository = DepositoRepository(session)
        self.estado_pileta_repository = EstadoPiletaRepository(session)

    def crear_pileta(self, data: PiletaCreate) -> Pileta:
        self._validar_pileta(data)
        pileta = Pileta(**data.model_dump())

        try:
            pileta = self.pileta_repository.add(pileta)
            self.session.commit()
            self.session.refresh(pileta)
            return pileta
        except IntegrityError as exc:
            self.session.rollback()
            raise ConflictError("Ya existe una pileta con esos datos.") from exc
        except Exception:
            self.session.rollback()
            raise

    def _validar_pileta(self, data: PiletaCreate) -> None:
        if not data.codigo.strip():
            raise BusinessRuleError("El codigo de la pileta es obligatorio.")
        if not data.nombre.strip():
            raise BusinessRuleError("El nombre de la pileta es obligatorio.")
        if self.bodega_repository.get_by_id(data.bodega_id) is None:
            raise NotFoundError("Bodega no encontrada.")
        if self.deposito_repository.get_by_id(data.deposito_id) is None:
            raise NotFoundError("Deposito no encontrado.")
        if self.estado_pileta_repository.get_by_id(data.estado_pileta_id) is None:
            raise NotFoundError("Estado de pileta no encontrado.")
