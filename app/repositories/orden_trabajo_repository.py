from datetime import date

from sqlalchemy import select

from app.models.orden_trabajo import OrdenTrabajo
from app.repositories.base import BaseRepository


class OrdenTrabajoRepository(BaseRepository[OrdenTrabajo]):
    model = OrdenTrabajo

    def list_pendientes(self) -> list[OrdenTrabajo]:
        statement = select(self.model).where(self.model.completada.is_not(True))
        return list(self.session.scalars(statement))

    def list_completadas(self) -> list[OrdenTrabajo]:
        statement = select(self.model).where(self.model.completada.is_(True))
        return list(self.session.scalars(statement))

    def list_by_operario(self, operario_id: int) -> list[OrdenTrabajo]:
        statement = select(self.model).where(self.model.operario_id == operario_id)
        return list(self.session.scalars(statement))

    def list_by_pileta(self, pileta_id: int) -> list[OrdenTrabajo]:
        statement = select(self.model).where(self.model.pileta_id == pileta_id)
        return list(self.session.scalars(statement))

    def list_by_lote(self, lote_id: int) -> list[OrdenTrabajo]:
        statement = select(self.model).where(self.model.lote_id == lote_id)
        return list(self.session.scalars(statement))

    def list_by_operacion_productiva(
        self,
        operacion_productiva_id: int,
    ) -> list[OrdenTrabajo]:
        statement = select(self.model).where(
            self.model.operacion_productiva_id == operacion_productiva_id
        )
        return list(self.session.scalars(statement))

    def list_by_fecha(
        self,
        fecha_desde: date,
        fecha_hasta: date | None = None,
    ) -> list[OrdenTrabajo]:
        statement = select(self.model).where(self.model.fecha >= fecha_desde)
        if fecha_hasta is not None:
            statement = statement.where(self.model.fecha <= fecha_hasta)
        return list(self.session.scalars(statement))
