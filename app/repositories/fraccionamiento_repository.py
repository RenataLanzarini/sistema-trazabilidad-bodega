from datetime import datetime

from sqlalchemy import select

from app.models.fraccionamiento import Fraccionamiento
from app.models.fraccionamiento_detalle import FraccionamientoDetalle
from app.repositories.base import BaseRepository


class FraccionamientoRepository(BaseRepository[Fraccionamiento]):
    model = Fraccionamiento

    def add_detalle(self, detalle: FraccionamientoDetalle) -> FraccionamientoDetalle:
        self.session.add(detalle)
        self.session.flush()
        return detalle

    def list_by_fecha(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime | None = None,
    ) -> list[Fraccionamiento]:
        statement = select(self.model).where(self.model.fecha >= fecha_desde)
        if fecha_hasta is not None:
            statement = statement.where(self.model.fecha <= fecha_hasta)
        return list(self.session.scalars(statement))

    def list_by_responsable(self, responsable_id: int) -> list[Fraccionamiento]:
        statement = select(self.model).where(self.model.responsable_id == responsable_id)
        return list(self.session.scalars(statement))

    def list_by_operacion(self, operacion_productiva_id: int) -> list[Fraccionamiento]:
        statement = select(self.model).where(
            self.model.operacion_productiva_id == operacion_productiva_id
        )
        return list(self.session.scalars(statement))

    def list_detalles_by_fraccionamiento(
        self,
        fraccionamiento_id: int,
    ) -> list[FraccionamientoDetalle]:
        statement = select(FraccionamientoDetalle).where(
            FraccionamientoDetalle.fraccionamiento_id == fraccionamiento_id
        )
        return list(self.session.scalars(statement))

    def list_by_lote(self, lote_id: int) -> list[Fraccionamiento]:
        statement = (
            select(self.model)
            .join(FraccionamientoDetalle)
            .where(FraccionamientoDetalle.lote_id == lote_id)
        )
        return list(self.session.scalars(statement).unique())
