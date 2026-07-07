from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace

from sqlalchemy.orm import Session

from app.models.bodega import Bodega
from app.models.causa_merma import CausaMerma
from app.models.cliente import Cliente
from app.models.origen_uva import OrigenUva
from app.models.tarea_orden_trabajo import TareaOrdenTrabajo
from app.models.usuario import Usuario
from app.models.variedad import Variedad
from app.services.movimiento_fisico_service import MovimientoFisicoService
from tests.unit.services._helpers import crear_catalogos_base, crear_lote, crear_pileta


def crear_variedad(db: Session, nombre: str = "Malbec") -> Variedad:
    variedad = Variedad(nombre=nombre)
    db.add(variedad)
    db.flush()
    return variedad


def crear_origen_uva(db: Session, nombre: str = "Finca Test") -> OrigenUva:
    origen = OrigenUva(nombre=nombre, tipo="propio")
    db.add(origen)
    db.flush()
    return origen


def crear_causa_merma(db: Session, nombre: str = "Evaporacion") -> CausaMerma:
    causa = CausaMerma(nombre=nombre)
    db.add(causa)
    db.flush()
    return causa


def crear_cliente(db: Session, nombre: str = "Cliente Test") -> Cliente:
    cliente = Cliente(nombre=nombre)
    db.add(cliente)
    db.flush()
    return cliente


def crear_tarea_orden_trabajo(
    db: Session,
    nombre: str = "Trasiego",
) -> TareaOrdenTrabajo:
    tarea = TareaOrdenTrabajo(nombre=nombre)
    db.add(tarea)
    db.flush()
    return tarea


def crear_contexto_con_stock(
    db: Session,
    *,
    bodega: Bodega,
    usuario: Usuario,
    codigo_lote: str = "L-STOCK",
    codigo_pileta: str = "P-STOCK",
    litros: Decimal = Decimal("100"),
    capacidad_litros: Decimal = Decimal("1000"),
) -> SimpleNamespace:
    catalogos = crear_catalogos_base(db, bodega, usuario)
    lote = crear_lote(db, bodega=bodega, catalogos=catalogos, codigo=codigo_lote)
    pileta = crear_pileta(
        db,
        bodega=bodega,
        catalogos=catalogos,
        codigo=codigo_pileta,
        capacidad_litros=capacidad_litros,
    )
    movimiento = MovimientoFisicoService(db).registrar_movimiento(
        operacion_productiva_id=catalogos.operacion.id,
        lote_id=lote.id,
        responsable_id=usuario.id,
        fecha=datetime(2026, 1, 1, 9, 0, 0),
        litros=litros,
        estado="registrado",
        pileta_destino_id=pileta.id,
    )
    return SimpleNamespace(
        catalogos=catalogos,
        lote=lote,
        pileta=pileta,
        movimiento=movimiento,
    )
