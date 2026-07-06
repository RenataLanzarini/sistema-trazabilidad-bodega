from datetime import datetime

from sqlalchemy import or_, select

from app.models.movimiento_fisico import MovimientoFisico
from app.repositories.base import BaseRepository


class MovimientoFisicoRepository(BaseRepository[MovimientoFisico]):
    model = MovimientoFisico

    def get_by_codigo_externo(self, codigo_externo: str) -> MovimientoFisico | None:
        statement = select(self.model).where(self.model.codigo_externo == codigo_externo)
        return self.session.scalar(statement)

    def list_by_lote(self, lote_id: int) -> list[MovimientoFisico]:
        statement = select(self.model).where(self.model.lote_id == lote_id)
        return list(self.session.scalars(statement))

    def list_by_pileta(self, pileta_id: int) -> list[MovimientoFisico]:
        statement = select(self.model).where(
            or_(
                self.model.pileta_origen_id == pileta_id,
                self.model.pileta_destino_id == pileta_id,
            )
        )
        return list(self.session.scalars(statement))

    def list_by_operacion(self, operacion_productiva_id: int) -> list[MovimientoFisico]:
        statement = select(self.model).where(
            self.model.operacion_productiva_id == operacion_productiva_id
        )
        return list(self.session.scalars(statement))

    def list_until_fecha(self, fecha: datetime) -> list[MovimientoFisico]:
        statement = select(self.model).where(self.model.fecha <= fecha)
        return list(self.session.scalars(statement))

    def list_by_fecha(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime | None = None,
    ) -> list[MovimientoFisico]:
        statement = select(self.model).where(self.model.fecha >= fecha_desde)
        if fecha_hasta is not None:
            statement = statement.where(self.model.fecha <= fecha_hasta)
        return list(self.session.scalars(statement))
