from sqlalchemy import select

from app.models.causa_merma import CausaMerma
from app.repositories.base import BaseRepository
from app.repositories.mixins import NombreLookupMixin


class CausaMermaRepository(NombreLookupMixin, BaseRepository[CausaMerma]):
    model = CausaMerma

    def list_activos(self) -> list[CausaMerma]:
        statement = select(self.model).where(self.model.activa.is_(True))
        return list(self.session.scalars(statement))
