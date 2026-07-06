from sqlalchemy import select

from app.models.bodega import Bodega
from app.repositories.base import BaseRepository
from app.repositories.mixins import NombreLookupMixin


class BodegaRepository(NombreLookupMixin, BaseRepository[Bodega]):
    model = Bodega

    def list_activas(self) -> list[Bodega]:
        statement = select(self.model).where(self.model.activa.is_(True))
        return list(self.session.scalars(statement))
