from datetime import date

from sqlalchemy import select

from app.models.recepcion_uva import RecepcionUva
from app.repositories.base import BaseRepository


class RecepcionUvaRepository(BaseRepository[RecepcionUva]):
    model = RecepcionUva

    def get_by_numero_ciu(self, numero_ciu: str) -> RecepcionUva | None:
        statement = select(self.model).where(self.model.numero_ciu == numero_ciu)
        return self.session.scalar(statement)

    def list_by_bodega(self, bodega_id: int) -> list[RecepcionUva]:
        statement = select(self.model).where(self.model.bodega_id == bodega_id)
        return list(self.session.scalars(statement))

    def list_by_origen_uva(self, origen_uva_id: int) -> list[RecepcionUva]:
        statement = select(self.model).where(self.model.origen_uva_id == origen_uva_id)
        return list(self.session.scalars(statement))

    def list_by_variedad(self, variedad_id: int) -> list[RecepcionUva]:
        statement = select(self.model).where(self.model.variedad_id == variedad_id)
        return list(self.session.scalars(statement))

    def list_by_cosecha(self, cosecha: int) -> list[RecepcionUva]:
        statement = select(self.model).where(self.model.cosecha == cosecha)
        return list(self.session.scalars(statement))

    def list_by_fecha(self, fecha_desde: date, fecha_hasta: date | None = None) -> list[RecepcionUva]:
        statement = select(self.model).where(self.model.fecha >= fecha_desde)
        if fecha_hasta is not None:
            statement = statement.where(self.model.fecha <= fecha_hasta)
        return list(self.session.scalars(statement))
