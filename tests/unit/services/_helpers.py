from datetime import date, datetime
from decimal import Decimal
from types import SimpleNamespace

from sqlalchemy.orm import Session

from app.models.bodega import Bodega
from app.models.deposito import Deposito
from app.models.estado_lote import EstadoLote
from app.models.estado_pileta import EstadoPileta
from app.models.lote import Lote
from app.models.movimiento_fisico import MovimientoFisico
from app.models.operacion_productiva import OperacionProductiva
from app.models.pileta import Pileta
from app.models.relacion_genealogica_lote import RelacionGenealogicaLote
from app.models.tipo_operacion import TipoOperacion
from app.models.tipo_producto import TipoProducto
from app.models.usuario import Usuario


def crear_catalogos_base(db: Session, bodega: Bodega, usuario: Usuario) -> SimpleNamespace:
    deposito = Deposito(bodega_id=bodega.id, nombre="Deposito Test")
    estado_pileta = EstadoPileta(nombre="Disponible")
    estado_lote = EstadoLote(nombre="Activo")
    tipo_producto = TipoProducto(nombre="Vino")
    tipo_operacion = TipoOperacion(nombre="Movimiento")
    db.add_all([deposito, estado_pileta, estado_lote, tipo_producto, tipo_operacion])
    db.flush()

    operacion = OperacionProductiva(
        bodega_id=bodega.id,
        tipo_operacion_id=tipo_operacion.id,
        responsable_id=usuario.id,
        fecha=datetime(2026, 1, 1, 8, 0, 0),
        estado="confirmada",
    )
    db.add(operacion)
    db.flush()

    return SimpleNamespace(
        deposito=deposito,
        estado_pileta=estado_pileta,
        estado_lote=estado_lote,
        tipo_producto=tipo_producto,
        tipo_operacion=tipo_operacion,
        operacion=operacion,
    )


def crear_pileta(
    db: Session,
    *,
    bodega: Bodega,
    catalogos: SimpleNamespace,
    codigo: str,
    capacidad_litros: Decimal = Decimal("1000"),
) -> Pileta:
    pileta = Pileta(
        bodega_id=bodega.id,
        deposito_id=catalogos.deposito.id,
        estado_pileta_id=catalogos.estado_pileta.id,
        codigo=codigo,
        nombre=f"Pileta {codigo}",
        capacidad_litros=capacidad_litros,
    )
    db.add(pileta)
    db.flush()
    return pileta


def crear_lote(
    db: Session,
    *,
    bodega: Bodega,
    catalogos: SimpleNamespace,
    codigo: str,
) -> Lote:
    lote = Lote(
        bodega_id=bodega.id,
        tipo_producto_id=catalogos.tipo_producto.id,
        estado_lote_id=catalogos.estado_lote.id,
        codigo=codigo,
        fecha_nacimiento=date(2026, 1, 1),
    )
    db.add(lote)
    db.flush()
    return lote


def crear_movimiento(
    db: Session,
    *,
    operacion: OperacionProductiva,
    lote: Lote,
    responsable: Usuario,
    fecha: datetime,
    litros: Decimal,
    pileta_origen: Pileta | None = None,
    pileta_destino: Pileta | None = None,
    estado: str = "confirmado",
) -> MovimientoFisico:
    movimiento = MovimientoFisico(
        operacion_productiva_id=operacion.id,
        lote_id=lote.id,
        pileta_origen_id=pileta_origen.id if pileta_origen else None,
        pileta_destino_id=pileta_destino.id if pileta_destino else None,
        responsable_id=responsable.id,
        fecha=fecha,
        litros=litros,
        estado=estado,
    )
    db.add(movimiento)
    db.flush()
    return movimiento


def crear_relacion(
    db: Session,
    *,
    operacion: OperacionProductiva,
    lote_padre: Lote,
    lote_hijo: Lote,
    litros_aportados: Decimal = Decimal("100"),
    tipo_relacion: str = "mezcla",
) -> RelacionGenealogicaLote:
    relacion = RelacionGenealogicaLote(
        operacion_productiva_id=operacion.id,
        lote_padre_id=lote_padre.id,
        lote_hijo_id=lote_hijo.id,
        litros_aportados=litros_aportados,
        tipo_relacion=tipo_relacion,
    )
    db.add(relacion)
    db.flush()
    return relacion
