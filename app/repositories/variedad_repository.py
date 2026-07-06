from sqlalchemy import select

from app.models.variedad import Variedad
from app.repositories.base import BaseRepository
from app.repositories.mixins import NombreLookupMixin


class VariedadRepository(NombreLookupMixin, BaseRepository[Variedad]):
    model = Variedad

    def list_activos(self) -> list[Variedad]:
        statement = select(self.model).where(self.model.activa.is_(True))
        return list(self.session.scalars(statement))
