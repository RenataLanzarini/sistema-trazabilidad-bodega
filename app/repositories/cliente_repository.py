from sqlalchemy import select

from app.models.cliente import Cliente
from app.repositories.base import BaseRepository
from app.repositories.mixins import ActivosMixin, NombreLookupMixin


class ClienteRepository(NombreLookupMixin, ActivosMixin, BaseRepository[Cliente]):
    model = Cliente

    def get_by_identificacion_fiscal(self, identificacion_fiscal: str) -> Cliente | None:
        statement = select(self.model).where(
            self.model.identificacion_fiscal == identificacion_fiscal
        )
        return self.session.scalar(statement)
