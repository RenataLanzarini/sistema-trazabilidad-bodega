from datetime import datetime

from sqlalchemy import select

from app.models.merma import Merma
from app.repositories.base import BaseRepository


class MermaRepository(BaseRepository[Merma]):
    model = Merma

    def list_by_lote(self, lote_id: int) -> list[Merma]:
        statement = select(self.model).where(self.model.lote_id == lote_id)
        return list(self.session.scalars(statement))

    def list_by_pileta(self, pileta_id: int) -> list[Merma]:
        statement = select(self.model).where(self.model.pileta_id == pileta_id)
        return list(self.session.scalars(statement))

    def list_by_causa(self, causa_merma_id: int) -> list[Merma]:
        statement = select(self.model).where(self.model.causa_merma_id == causa_merma_id)
        return list(self.session.scalars(statement))

    def list_by_fecha(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime | None = None,
    ) -> list[Merma]:
        statement = select(self.model).where(self.model.fecha >= fecha_desde)
        if fecha_hasta is not None:
            statement = statement.where(self.model.fecha <= fecha_hasta)
        return list(self.session.scalars(statement))

    def list_by_operacion(self, operacion_productiva_id: int) -> list[Merma]:
        statement = select(self.model).where(
            self.model.operacion_productiva_id == operacion_productiva_id
        )
        return list(self.session.scalars(statement))
