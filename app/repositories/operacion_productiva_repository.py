from datetime import datetime

from sqlalchemy import select

from app.models.operacion_productiva import OperacionProductiva
from app.repositories.base import BaseRepository


class OperacionProductivaRepository(BaseRepository[OperacionProductiva]):
    model = OperacionProductiva

    def get_by_codigo_externo(self, codigo_externo: str) -> OperacionProductiva | None:
        statement = select(self.model).where(self.model.codigo_externo == codigo_externo)
        return self.session.scalar(statement)

    def list_by_bodega(self, bodega_id: int) -> list[OperacionProductiva]:
        statement = select(self.model).where(self.model.bodega_id == bodega_id)
        return list(self.session.scalars(statement))

    def list_by_tipo(self, tipo_operacion_id: int) -> list[OperacionProductiva]:
        statement = select(self.model).where(self.model.tipo_operacion_id == tipo_operacion_id)
        return list(self.session.scalars(statement))

    def list_by_fecha(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime | None = None,
    ) -> list[OperacionProductiva]:
        statement = select(self.model).where(self.model.fecha >= fecha_desde)
        if fecha_hasta is not None:
            statement = statement.where(self.model.fecha <= fecha_hasta)
        return list(self.session.scalars(statement))

    def list_by_responsable(self, responsable_id: int) -> list[OperacionProductiva]:
        statement = select(self.model).where(self.model.responsable_id == responsable_id)
        return list(self.session.scalars(statement))

    def list_anuladas(self) -> list[OperacionProductiva]:
        statement = select(self.model).where(self.model.anulada.is_(True))
        return list(self.session.scalars(statement))
