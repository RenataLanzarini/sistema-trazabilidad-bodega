from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.models.fraccionamiento import Fraccionamiento
from app.models.fraccionamiento_detalle import FraccionamientoDetalle
from app.models.producto_terminado import ProductoTerminado
from app.repositories.fraccionamiento_repository import FraccionamientoRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.operacion_productiva_repository import OperacionProductivaRepository
from app.repositories.pileta_repository import PiletaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.movimiento_fisico_service import MovimientoFisicoService
from app.services.producto_terminado_service import ProductoTerminadoService
from app.services.stock_service import StockService


class FraccionamientoService:
    """Crea fraccionamientos, consumos fisicos y productos terminados asociados."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.fraccionamiento_repository = FraccionamientoRepository(session)
        self.operacion_repository = OperacionProductivaRepository(session)
        self.usuario_repository = UsuarioRepository(session)
        self.lote_repository = LoteRepository(session)
        self.pileta_repository = PiletaRepository(session)
        self.stock_service = StockService(session)
        self.movimiento_service = MovimientoFisicoService(session)
        self.producto_service = ProductoTerminadoService(session)

    def crear_fraccionamiento(
        self,
        *,
        operacion_productiva_id: int,
        responsable_id: int,
        fecha: datetime,
        estado: str,
        detalles: list[dict[str, Any]],
        productos_terminados: list[dict[str, Any]],
        observaciones: str | None = None,
    ) -> Fraccionamiento:
        self._validar_fraccionamiento(
            operacion_productiva_id=operacion_productiva_id,
            responsable_id=responsable_id,
            estado=estado,
            detalles=detalles,
        )

        fraccionamiento = Fraccionamiento(
            operacion_productiva_id=operacion_productiva_id,
            responsable_id=responsable_id,
            fecha=fecha,
            estado=estado,
            observaciones=observaciones,
        )

        try:
            fraccionamiento = self.fraccionamiento_repository.add(fraccionamiento)
            for detalle_data in detalles:
                self._registrar_detalle_y_movimiento(
                    fraccionamiento_id=fraccionamiento.id,
                    operacion_productiva_id=operacion_productiva_id,
                    responsable_id=responsable_id,
                    fecha=fecha,
                    detalle_data=detalle_data,
                )

            for producto_data in productos_terminados:
                self._crear_producto_terminado(
                    fraccionamiento_id=fraccionamiento.id,
                    producto_data=producto_data,
                )

            self.session.commit()
            self.session.refresh(fraccionamiento)
            return fraccionamiento
        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, fraccionamiento_id: int) -> Fraccionamiento:
        fraccionamiento = self.fraccionamiento_repository.get_by_id(fraccionamiento_id)
        if fraccionamiento is None:
            raise NotFoundError("Fraccionamiento no encontrado.")
        return fraccionamiento

    def listar(self) -> list[Fraccionamiento]:
        return self.fraccionamiento_repository.list()

    def listar_por_lote(self, lote_id: int) -> list[Fraccionamiento]:
        return self.fraccionamiento_repository.list_by_lote(lote_id)

    def listar_por_fecha(self, fecha: date) -> list[Fraccionamiento]:
        fecha_desde = datetime.combine(fecha, time.min)
        fecha_hasta = datetime.combine(fecha, time.max)
        return self.fraccionamiento_repository.list_by_fecha(fecha_desde, fecha_hasta)

    def _registrar_detalle_y_movimiento(
        self,
        *,
        fraccionamiento_id: int,
        operacion_productiva_id: int,
        responsable_id: int,
        fecha: datetime,
        detalle_data: dict[str, Any],
    ) -> FraccionamientoDetalle:
        lote_id = int(detalle_data["lote_id"])
        pileta_id = int(detalle_data["pileta_id"])
        litros_consumidos = Decimal(str(detalle_data["litros_consumidos"]))
        observaciones = detalle_data.get("observaciones")

        detalle = FraccionamientoDetalle(
            fraccionamiento_id=fraccionamiento_id,
            lote_id=lote_id,
            pileta_id=pileta_id,
            litros_consumidos=litros_consumidos,
            observaciones=str(observaciones) if observaciones is not None else None,
        )
        detalle = self.fraccionamiento_repository.add_detalle(detalle)
        self.movimiento_service.registrar_movimiento(
            operacion_productiva_id=operacion_productiva_id,
            lote_id=lote_id,
            responsable_id=responsable_id,
            fecha=fecha,
            litros=litros_consumidos,
            estado="registrado",
            pileta_origen_id=pileta_id,
            observaciones=detalle.observaciones,
            commit=False,
        )
        return detalle

    def _crear_producto_terminado(
        self,
        *,
        fraccionamiento_id: int,
        producto_data: dict[str, Any],
    ) -> ProductoTerminado:
        return self.producto_service.crear_producto_terminado(
            fraccionamiento_id=fraccionamiento_id,
            tipo_producto_id=int(producto_data["tipo_producto_id"]),
            lote_id=int(producto_data["lote_id"]),
            codigo=str(producto_data["codigo"]),
            cantidad_unidades=int(producto_data["cantidad_unidades"]),
            volumen_unidad_ml=int(producto_data["volumen_unidad_ml"]),
            litros_totales=Decimal(str(producto_data["litros_totales"])),
            fecha_produccion=producto_data["fecha_produccion"]
            if isinstance(producto_data["fecha_produccion"], date)
            else date.fromisoformat(str(producto_data["fecha_produccion"])),
            estado=str(producto_data["estado"]),
            observaciones=producto_data.get("observaciones"),
            commit=False,
        )

    def _validar_fraccionamiento(
        self,
        *,
        operacion_productiva_id: int,
        responsable_id: int,
        estado: str,
        detalles: list[dict[str, Any]],
    ) -> None:
        if not estado or not estado.strip():
            raise BusinessRuleError("El estado del fraccionamiento es obligatorio.")
        if not detalles:
            raise BusinessRuleError("El fraccionamiento debe tener al menos un detalle.")
        if self.operacion_repository.get_by_id(operacion_productiva_id) is None:
            raise NotFoundError("Operacion productiva no encontrada.")
        if self.usuario_repository.get_by_id(responsable_id) is None:
            raise NotFoundError("Usuario responsable no encontrado.")

        consumos_por_stock: dict[tuple[int, int], Decimal] = {}
        for detalle in detalles:
            lote_id = int(detalle["lote_id"])
            pileta_id = int(detalle["pileta_id"])
            litros_consumidos = Decimal(str(detalle["litros_consumidos"]))
            if litros_consumidos <= 0:
                raise BusinessRuleError("Los litros consumidos deben ser mayores a cero.")
            if self.lote_repository.get_by_id(lote_id) is None:
                raise NotFoundError("Lote no encontrado.")
            if self.pileta_repository.get_by_id(pileta_id) is None:
                raise NotFoundError("Pileta no encontrada.")

            clave_stock = (lote_id, pileta_id)
            consumos_por_stock[clave_stock] = (
                consumos_por_stock.get(clave_stock, Decimal("0")) + litros_consumidos
            )

        self.stock_service.bloquear_consumos(list(consumos_por_stock))
        for (lote_id, pileta_id), litros_consumidos in consumos_por_stock.items():
            if not self.stock_service.validar_stock_disponible(
                lote_id,
                pileta_id,
                litros_consumidos,
            ):
                raise BusinessRuleError("Stock insuficiente para fraccionar.")
