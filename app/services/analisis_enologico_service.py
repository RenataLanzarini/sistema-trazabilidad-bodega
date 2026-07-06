from datetime import date

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.models.analisis_enologico import AnalisisEnologico
from app.repositories.analisis_enologico_repository import AnalisisEnologicoRepository
from app.repositories.bodega_repository import BodegaRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.pileta_repository import PiletaRepository
from app.schemas.analisis_enologico import AnalisisEnologicoCreate


class AnalisisEnologicoService:
    """Gestiona registro y consultas de analisis enologicos sin impacto en stock."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.analisis_repository = AnalisisEnologicoRepository(session)
        self.bodega_repository = BodegaRepository(session)
        self.lote_repository = LoteRepository(session)
        self.pileta_repository = PiletaRepository(session)

    def crear_analisis(self, data: AnalisisEnologicoCreate) -> AnalisisEnologico:
        self._validar_analisis(data)
        analisis = AnalisisEnologico(**data.model_dump())

        try:
            analisis = self.analisis_repository.add(analisis)
            self.session.commit()
            self.session.refresh(analisis)
            return analisis
        except Exception:
            self.session.rollback()
            raise

    def listar(self) -> list[AnalisisEnologico]:
        return self.analisis_repository.list()

    def obtener_por_id(self, analisis_id: int) -> AnalisisEnologico:
        analisis = self.analisis_repository.get_by_id(analisis_id)
        if analisis is None:
            raise NotFoundError("Analisis enologico no encontrado.")
        return analisis

    def listar_por_lote(self, lote_id: int) -> list[AnalisisEnologico]:
        return self.analisis_repository.list_by_lote(lote_id)

    def listar_por_pileta(self, pileta_id: int) -> list[AnalisisEnologico]:
        return self.analisis_repository.list_by_pileta(pileta_id)

    def listar_por_fecha(self, fecha: date) -> list[AnalisisEnologico]:
        return self.analisis_repository.list_by_fecha(fecha, fecha)

    def obtener_ultimo_por_lote(self, lote_id: int) -> AnalisisEnologico:
        analisis = self.analisis_repository.latest_by_lote(lote_id)
        if analisis is None:
            raise NotFoundError("Analisis enologico no encontrado.")
        return analisis

    def obtener_ultimo_por_pileta(self, pileta_id: int) -> AnalisisEnologico:
        analisis = self.analisis_repository.latest_by_pileta(pileta_id)
        if analisis is None:
            raise NotFoundError("Analisis enologico no encontrado.")
        return analisis

    def _validar_analisis(self, data: AnalisisEnologicoCreate) -> None:
        if data.lote_id is None and data.pileta_id is None:
            raise BusinessRuleError("El analisis debe estar asociado a lote o pileta.")
        if self.bodega_repository.get_by_id(data.bodega_id) is None:
            raise NotFoundError("Bodega no encontrada.")
        if data.lote_id is not None and self.lote_repository.get_by_id(data.lote_id) is None:
            raise NotFoundError("Lote no encontrado.")
        if (
            data.pileta_id is not None
            and self.pileta_repository.get_by_id(data.pileta_id) is None
        ):
            raise NotFoundError("Pileta no encontrada.")
