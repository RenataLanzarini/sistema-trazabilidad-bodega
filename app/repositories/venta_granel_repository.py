from datetime import datetime

from sqlalchemy import select

from app.models.venta_granel import VentaGranel
from app.models.venta_granel_detalle import VentaGranelDetalle
from app.repositories.base import BaseRepository


class VentaGranelRepository(BaseRepository[VentaGranel]):
    model = VentaGranel

    def add_detalle(self, detalle: VentaGranelDetalle) -> VentaGranelDetalle:
        self.session.add(detalle)
        self.session.flush()
        return detalle

    def list_by_cliente(self, cliente_id: int) -> list[VentaGranel]:
        statement = select(self.model).where(self.model.cliente_id == cliente_id)
        return list(self.session.scalars(statement))

    def list_by_fecha(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime | None = None,
    ) -> list[VentaGranel]:
        statement = select(self.model).where(self.model.fecha >= fecha_desde)
        if fecha_hasta is not None:
            statement = statement.where(self.model.fecha <= fecha_hasta)
        return list(self.session.scalars(statement))

    def list_by_responsable(self, responsable_id: int) -> list[VentaGranel]:
        statement = select(self.model).where(self.model.responsable_id == responsable_id)
        return list(self.session.scalars(statement))

    def list_by_operacion(self, operacion_productiva_id: int) -> list[VentaGranel]:
        statement = select(self.model).where(
            self.model.operacion_productiva_id == operacion_productiva_id
        )
        return list(self.session.scalars(statement))

    def list_detalles_by_venta(self, venta_granel_id: int) -> list[VentaGranelDetalle]:
        statement = select(VentaGranelDetalle).where(
            VentaGranelDetalle.venta_granel_id == venta_granel_id
        )
        return list(self.session.scalars(statement))

    def list_by_lote(self, lote_id: int) -> list[VentaGranel]:
        statement = (
            select(self.model)
            .join(VentaGranelDetalle)
            .where(VentaGranelDetalle.lote_id == lote_id)
        )
        return list(self.session.scalars(statement).unique())

    def list_by_pileta(self, pileta_id: int) -> list[VentaGranel]:
        statement = (
            select(self.model)
            .join(VentaGranelDetalle)
            .where(VentaGranelDetalle.pileta_id == pileta_id)
        )
        return list(self.session.scalars(statement).unique())
