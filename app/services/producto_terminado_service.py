from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.models.producto_terminado import ProductoTerminado
from app.repositories.fraccionamiento_repository import FraccionamientoRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.producto_terminado_repository import ProductoTerminadoRepository
from app.repositories.tipo_producto_repository import TipoProductoRepository


class ProductoTerminadoService:
    """Coordina reglas basicas de producto terminado y delega persistencia."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.producto_repository = ProductoTerminadoRepository(session)
        self.fraccionamiento_repository = FraccionamientoRepository(session)
        self.lote_repository = LoteRepository(session)
        self.tipo_producto_repository = TipoProductoRepository(session)

    def crear_producto_terminado(
        self,
        *,
        fraccionamiento_id: int,
        tipo_producto_id: int,
        lote_id: int,
        codigo: str,
        cantidad_unidades: int,
        volumen_unidad_ml: int,
        litros_totales: Decimal,
        fecha_produccion: date,
        estado: str,
        observaciones: str | None = None,
        commit: bool = True,
    ) -> ProductoTerminado:
        self._validar_producto(
            fraccionamiento_id=fraccionamiento_id,
            tipo_producto_id=tipo_producto_id,
            lote_id=lote_id,
            codigo=codigo,
            cantidad_unidades=cantidad_unidades,
            volumen_unidad_ml=volumen_unidad_ml,
            litros_totales=litros_totales,
            estado=estado,
        )
        producto = ProductoTerminado(
            fraccionamiento_id=fraccionamiento_id,
            tipo_producto_id=tipo_producto_id,
            lote_id=lote_id,
            codigo=codigo,
            cantidad_unidades=cantidad_unidades,
            volumen_unidad_ml=volumen_unidad_ml,
            litros_totales=litros_totales,
            fecha_produccion=fecha_produccion,
            estado=estado,
            observaciones=observaciones,
        )

        try:
            producto = self.producto_repository.add(producto)
            if commit:
                self.session.commit()
                self.session.refresh(producto)
            return producto
        except Exception:
            if commit:
                self.session.rollback()
            raise

    def obtener_por_codigo(self, codigo: str) -> ProductoTerminado:
        producto = self.producto_repository.get_by_codigo(codigo)
        if producto is None:
            raise NotFoundError("Producto terminado no encontrado.")
        return producto

    def listar_por_lote(self, lote_id: int) -> list[ProductoTerminado]:
        return self.producto_repository.list_by_lote(lote_id)

    def listar_por_fraccionamiento(self, fraccionamiento_id: int) -> list[ProductoTerminado]:
        return self.producto_repository.list_by_fraccionamiento(fraccionamiento_id)

    def listar_por_fecha_produccion(
        self,
        fecha_desde: date,
        fecha_hasta: date | None = None,
    ) -> list[ProductoTerminado]:
        return self.producto_repository.list_by_fecha_produccion(fecha_desde, fecha_hasta)

    def _validar_producto(
        self,
        *,
        fraccionamiento_id: int,
        tipo_producto_id: int,
        lote_id: int,
        codigo: str,
        cantidad_unidades: int,
        volumen_unidad_ml: int,
        litros_totales: Decimal,
        estado: str,
    ) -> None:
        if not codigo.strip():
            raise BusinessRuleError("El codigo del producto terminado es obligatorio.")
        if self.producto_repository.get_by_codigo(codigo) is not None:
            raise ConflictError("Ya existe un producto terminado con ese codigo.")
        if cantidad_unidades <= 0:
            raise BusinessRuleError("La cantidad de unidades debe ser mayor a cero.")
        if volumen_unidad_ml <= 0:
            raise BusinessRuleError("El volumen por unidad debe ser mayor a cero.")
        if litros_totales <= 0:
            raise BusinessRuleError("Los litros totales deben ser mayores a cero.")
        if not estado or not estado.strip():
            raise BusinessRuleError("El estado del producto terminado es obligatorio.")
        if self.fraccionamiento_repository.get_by_id(fraccionamiento_id) is None:
            raise NotFoundError("Fraccionamiento no encontrado.")
        if self.tipo_producto_repository.get_by_id(tipo_producto_id) is None:
            raise NotFoundError("Tipo de producto no encontrado.")
        if self.lote_repository.get_by_id(lote_id) is None:
            raise NotFoundError("Lote no encontrado.")
