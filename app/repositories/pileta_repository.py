from sqlalchemy import select

from app.models.pileta import Pileta
from app.repositories.base import BaseRepository


class PiletaRepository(BaseRepository[Pileta]):
    model = Pileta

    def get_by_codigo(self, codigo: str) -> Pileta | None:
        statement = select(self.model).where(self.model.codigo == codigo)
        return self.session.scalar(statement)

    def list_by_bodega(self, bodega_id: int) -> list[Pileta]:
        statement = select(self.model).where(self.model.bodega_id == bodega_id)
        return list(self.session.scalars(statement))

    def list_activas(self) -> list[Pileta]:
        statement = select(self.model).where(self.model.activa.is_(True))
        return list(self.session.scalars(statement))

    def list_by_deposito(self, deposito_id: int) -> list[Pileta]:
        statement = select(self.model).where(self.model.deposito_id == deposito_id)
        return list(self.session.scalars(statement))

    def list_by_estado(self, estado_pileta_id: int) -> list[Pileta]:
        statement = select(self.model).where(self.model.estado_pileta_id == estado_pileta_id)
        return list(self.session.scalars(statement))
