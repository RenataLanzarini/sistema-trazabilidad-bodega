from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.models.venta_granel import VentaGranel
from app.models.venta_granel_detalle import VentaGranelDetalle
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.operacion_productiva_repository import OperacionProductivaRepository
from app.repositories.pileta_repository import PiletaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.venta_granel_repository import VentaGranelRepository
from app.services.movimiento_fisico_service import MovimientoFisicoService
from app.services.stock_service import StockService


class VentaGranelService:
    """Crea ventas a granel y registra sus salidas fisicas de stock."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.venta_repository = VentaGranelRepository(session)
        self.operacion_repository = OperacionProductivaRepository(session)
        self.cliente_repository = ClienteRepository(session)
        self.usuario_repository = UsuarioRepository(session)
        self.lote_repository = LoteRepository(session)
        self.pileta_repository = PiletaRepository(session)
        self.stock_service = StockService(session)
        self.movimiento_service = MovimientoFisicoService(session)

    def crear_venta_granel(
        self,
        *,
        operacion_productiva_id: int,
        cliente_id: int,
        responsable_id: int,
        fecha: datetime,
        estado: str,
        detalles: list[dict[str, Any]],
        documento: str | None = None,
        observaciones: str | None = None,
    ) -> VentaGranel:
        self._validar_venta(
            operacion_productiva_id=operacion_productiva_id,
            cliente_id=cliente_id,
            responsable_id=responsable_id,
            estado=estado,
            detalles=detalles,
        )

        venta = VentaGranel(
            operacion_productiva_id=operacion_productiva_id,
            cliente_id=cliente_id,
            responsable_id=responsable_id,
            fecha=fecha,
            documento=documento,
            estado=estado,
            observaciones=observaciones,
        )

        try:
            venta = self.venta_repository.add(venta)
            for detalle_data in detalles:
                self._registrar_detalle_y_movimiento(
                    venta_granel_id=venta.id,
                    operacion_productiva_id=operacion_productiva_id,
                    responsable_id=responsable_id,
                    fecha=fecha,
                    detalle_data=detalle_data,
                )

            self.session.commit()
            self.session.refresh(venta)
            return venta
        except Exception:
            self.session.rollback()
            raise

    def listar_por_cliente(self, cliente_id: int) -> list[VentaGranel]:
        return self.venta_repository.list_by_cliente(cliente_id)

    def listar_por_fecha(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime | None = None,
    ) -> list[VentaGranel]:
        return self.venta_repository.list_by_fecha(fecha_desde, fecha_hasta)

    def listar_por_responsable(self, responsable_id: int) -> list[VentaGranel]:
        return self.venta_repository.list_by_responsable(responsable_id)

    def listar_por_operacion(self, operacion_productiva_id: int) -> list[VentaGranel]:
        return self.venta_repository.list_by_operacion(operacion_productiva_id)

    def listar_detalles_por_venta(
        self,
        venta_granel_id: int,
    ) -> list[VentaGranelDetalle]:
        return self.venta_repository.list_detalles_by_venta(venta_granel_id)

    def _registrar_detalle_y_movimiento(
        self,
        *,
        venta_granel_id: int,
        operacion_productiva_id: int,
        responsable_id: int,
        fecha: datetime,
        detalle_data: dict[str, Any],
    ) -> VentaGranelDetalle:
        lote_id = int(detalle_data["lote_id"])
        pileta_id = int(detalle_data["pileta_id"])
        litros = Decimal(str(detalle_data["litros"]))
        observaciones = detalle_data.get("observaciones")

        detalle = VentaGranelDetalle(
            venta_granel_id=venta_granel_id,
            lote_id=lote_id,
            pileta_id=pileta_id,
            litros=litros,
            observaciones=str(observaciones) if observaciones is not None else None,
        )
        detalle = self.venta_repository.add_detalle(detalle)
        self.movimiento_service.registrar_movimiento(
            operacion_productiva_id=operacion_productiva_id,
            lote_id=lote_id,
            responsable_id=responsable_id,
            fecha=fecha,
            litros=litros,
            estado="registrado",
            pileta_origen_id=pileta_id,
            observaciones=detalle.observaciones,
            commit=False,
        )
        return detalle

    def _validar_venta(
        self,
        *,
        operacion_productiva_id: int,
        cliente_id: int,
        responsable_id: int,
        estado: str,
        detalles: list[dict[str, Any]],
    ) -> None:
        if not estado or not estado.strip():
            raise BusinessRuleError("El estado de la venta a granel es obligatorio.")
        if not detalles:
            raise BusinessRuleError("La venta a granel debe tener al menos un detalle.")
        if self.operacion_repository.get_by_id(operacion_productiva_id) is None:
            raise NotFoundError("Operacion productiva no encontrada.")
        if self.cliente_repository.get_by_id(cliente_id) is None:
            raise NotFoundError("Cliente no encontrado.")
        if self.usuario_repository.get_by_id(responsable_id) is None:
            raise NotFoundError("Usuario responsable no encontrado.")

        consumos_por_stock: dict[tuple[int, int], Decimal] = {}
        for detalle in detalles:
            lote_id = int(detalle["lote_id"])
            pileta_id = int(detalle["pileta_id"])
            litros = Decimal(str(detalle["litros"]))
            if litros <= 0:
                raise BusinessRuleError("Los litros vendidos deben ser mayores a cero.")
            if self.lote_repository.get_by_id(lote_id) is None:
                raise NotFoundError("Lote no encontrado.")
            if self.pileta_repository.get_by_id(pileta_id) is None:
                raise NotFoundError("Pileta no encontrada.")

            clave_stock = (lote_id, pileta_id)
            consumos_por_stock[clave_stock] = (
                consumos_por_stock.get(clave_stock, Decimal("0")) + litros
            )

        self.stock_service.bloquear_consumos(list(consumos_por_stock))
        for (lote_id, pileta_id), litros in consumos_por_stock.items():
            if not self.stock_service.validar_stock_disponible(
                lote_id,
                pileta_id,
                litros,
            ):
                raise BusinessRuleError("Stock insuficiente para vender a granel.")
