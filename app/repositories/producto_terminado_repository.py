from datetime import date

from sqlalchemy import select

from app.models.producto_terminado import ProductoTerminado
from app.repositories.base import BaseRepository


class ProductoTerminadoRepository(BaseRepository[ProductoTerminado]):
    model = ProductoTerminado

    def get_by_codigo(self, codigo: str) -> ProductoTerminado | None:
        statement = select(self.model).where(self.model.codigo == codigo)
        return self.session.scalar(statement)

    def list_by_lote(self, lote_id: int) -> list[ProductoTerminado]:
        statement = select(self.model).where(self.model.lote_id == lote_id)
        return list(self.session.scalars(statement))

    def list_by_fraccionamiento(self, fraccionamiento_id: int) -> list[ProductoTerminado]:
        statement = select(self.model).where(self.model.fraccionamiento_id == fraccionamiento_id)
        return list(self.session.scalars(statement))

    def list_by_tipo_producto(self, tipo_producto_id: int) -> list[ProductoTerminado]:
        statement = select(self.model).where(self.model.tipo_producto_id == tipo_producto_id)
        return list(self.session.scalars(statement))

    def list_by_fecha_produccion(
        self,
        fecha_desde: date,
        fecha_hasta: date | None = None,
    ) -> list[ProductoTerminado]:
        statement = select(self.model).where(self.model.fecha_produccion >= fecha_desde)
        if fecha_hasta is not None:
            statement = statement.where(self.model.fecha_produccion <= fecha_hasta)
        return list(self.session.scalars(statement))
