from sqlalchemy import select

from app.models.deposito import Deposito
from app.repositories.base import BaseRepository
from app.repositories.mixins import ActivosMixin, NombreLookupMixin


class DepositoRepository(NombreLookupMixin, ActivosMixin, BaseRepository[Deposito]):
    model = Deposito

    def list_by_bodega(self, bodega_id: int) -> list[Deposito]:
        statement = select(self.model).where(self.model.bodega_id == bodega_id)
        return list(self.session.scalars(statement))
