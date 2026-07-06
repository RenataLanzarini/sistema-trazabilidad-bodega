from datetime import date

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.models.medicion_fermentacion import MedicionFermentacion
from app.repositories.bodega_repository import BodegaRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.medicion_fermentacion_repository import (
    MedicionFermentacionRepository,
)
from app.repositories.pileta_repository import PiletaRepository
from app.schemas.medicion_fermentacion import MedicionFermentacionCreate


class MedicionFermentacionService:
    """Gestiona mediciones de fermentacion sin impacto en stock."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.medicion_repository = MedicionFermentacionRepository(session)
        self.bodega_repository = BodegaRepository(session)
        self.lote_repository = LoteRepository(session)
        self.pileta_repository = PiletaRepository(session)

    def crear_medicion(self, data: MedicionFermentacionCreate) -> MedicionFermentacion:
        self._validar_medicion(data)
        medicion = MedicionFermentacion(**data.model_dump())

        try:
            medicion = self.medicion_repository.add(medicion)
            self.session.commit()
            self.session.refresh(medicion)
            return medicion
        except Exception:
            self.session.rollback()
            raise

    def listar(self) -> list[MedicionFermentacion]:
        return self.medicion_repository.list()

    def obtener_por_id(self, medicion_id: int) -> MedicionFermentacion:
        medicion = self.medicion_repository.get_by_id(medicion_id)
        if medicion is None:
            raise NotFoundError("Medicion de fermentacion no encontrada.")
        return medicion

    def listar_por_lote(self, lote_id: int) -> list[MedicionFermentacion]:
        return self.medicion_repository.list_by_lote(lote_id)

    def listar_por_pileta(self, pileta_id: int) -> list[MedicionFermentacion]:
        return self.medicion_repository.list_by_pileta(pileta_id)

    def listar_por_fecha(self, fecha: date) -> list[MedicionFermentacion]:
        return self.medicion_repository.list_by_fecha(fecha, fecha)

    def obtener_ultima_por_lote(self, lote_id: int) -> MedicionFermentacion:
        medicion = self.medicion_repository.latest_by_lote(lote_id)
        if medicion is None:
            raise NotFoundError("Medicion de fermentacion no encontrada.")
        return medicion

    def obtener_ultima_por_pileta(self, pileta_id: int) -> MedicionFermentacion:
        medicion = self.medicion_repository.latest_by_pileta(pileta_id)
        if medicion is None:
            raise NotFoundError("Medicion de fermentacion no encontrada.")
        return medicion

    def _validar_medicion(self, data: MedicionFermentacionCreate) -> None:
        if data.lote_id is None and data.pileta_id is None:
            raise BusinessRuleError("La medicion debe estar asociada a lote o pileta.")
        if self.bodega_repository.get_by_id(data.bodega_id) is None:
            raise NotFoundError("Bodega no encontrada.")
        if data.lote_id is not None and self.lote_repository.get_by_id(data.lote_id) is None:
            raise NotFoundError("Lote no encontrado.")
        if (
            data.pileta_id is not None
            and self.pileta_repository.get_by_id(data.pileta_id) is None
        ):
            raise NotFoundError("Pileta no encontrada.")
