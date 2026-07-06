from datetime import date

from sqlalchemy import select

from app.models.medicion_fermentacion import MedicionFermentacion
from app.repositories.base import BaseRepository


class MedicionFermentacionRepository(BaseRepository[MedicionFermentacion]):
    model = MedicionFermentacion

    def list_by_lote(self, lote_id: int) -> list[MedicionFermentacion]:
        statement = select(self.model).where(self.model.lote_id == lote_id)
        return list(self.session.scalars(statement))

    def list_by_pileta(self, pileta_id: int) -> list[MedicionFermentacion]:
        statement = select(self.model).where(self.model.pileta_id == pileta_id)
        return list(self.session.scalars(statement))

    def list_by_bodega(self, bodega_id: int) -> list[MedicionFermentacion]:
        statement = select(self.model).where(self.model.bodega_id == bodega_id)
        return list(self.session.scalars(statement))

    def list_by_fecha(
        self,
        fecha_desde: date,
        fecha_hasta: date | None = None,
    ) -> list[MedicionFermentacion]:
        statement = select(self.model).where(self.model.fecha >= fecha_desde)
        if fecha_hasta is not None:
            statement = statement.where(self.model.fecha <= fecha_hasta)
        return list(self.session.scalars(statement))

    def latest_by_lote(self, lote_id: int) -> MedicionFermentacion | None:
        statement = (
            select(self.model)
            .where(self.model.lote_id == lote_id)
            .order_by(self.model.fecha.desc(), self.model.id.desc())
            .limit(1)
        )
        return self.session.scalar(statement)

    def latest_by_pileta(self, pileta_id: int) -> MedicionFermentacion | None:
        statement = (
            select(self.model)
            .where(self.model.pileta_id == pileta_id)
            .order_by(self.model.fecha.desc(), self.model.id.desc())
            .limit(1)
        )
        return self.session.scalar(statement)
