from sqlalchemy import select

from app.models.calificacion_vino import CalificacionVino
from app.repositories.base import BaseRepository
from app.repositories.mixins import NombreLookupMixin


class CalificacionVinoRepository(NombreLookupMixin, BaseRepository[CalificacionVino]):
    model = CalificacionVino

    def list_activos(self) -> list[CalificacionVino]:
        statement = select(self.model).where(self.model.activa.is_(True))
        return list(self.session.scalars(statement))
