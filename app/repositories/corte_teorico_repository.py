from datetime import date

from sqlalchemy import select

from app.models.corte_teorico import CorteTeorico
from app.models.corte_teorico_detalle import CorteTeoricoDetalle
from app.repositories.base import BaseRepository


class CorteTeoricoRepository(BaseRepository[CorteTeorico]):
    model = CorteTeorico

    def add_detalle(self, detalle: CorteTeoricoDetalle) -> CorteTeoricoDetalle:
        self.session.add(detalle)
        self.session.flush()
        return detalle

    def list_by_fecha(
        self,
        fecha_desde: date,
        fecha_hasta: date | None = None,
    ) -> list[CorteTeorico]:
        statement = select(self.model).where(self.model.fecha >= fecha_desde)
        if fecha_hasta is not None:
            statement = statement.where(self.model.fecha <= fecha_hasta)
        return list(self.session.scalars(statement))

    def list_by_responsable(self, responsable_id: int) -> list[CorteTeorico]:
        statement = select(self.model).where(self.model.responsable_id == responsable_id)
        return list(self.session.scalars(statement))

    def list_by_operacion_productiva(
        self,
        operacion_productiva_id: int,
    ) -> list[CorteTeorico]:
        statement = select(self.model).where(
            self.model.operacion_productiva_id == operacion_productiva_id
        )
        return list(self.session.scalars(statement))

    def list_detalles_by_corte(self, corte_teorico_id: int) -> list[CorteTeoricoDetalle]:
        statement = select(CorteTeoricoDetalle).where(
            CorteTeoricoDetalle.corte_teorico_id == corte_teorico_id
        )
        return list(self.session.scalars(statement))
