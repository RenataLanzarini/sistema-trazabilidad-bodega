from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.services.stock_service import StockService
from tests.unit.services._helpers import (
    crear_catalogos_base,
    crear_lote,
    crear_movimiento,
    crear_pileta,
)


def test_stock_cero_cuando_no_existen_movimientos(db_session: Session, bodega, usuario_admin) -> None:
    service = StockService(db_session)

    assert service.calcular_stock_actual_por_pileta(999) == Decimal("0")
    assert service.calcular_stock_actual_por_lote(999) == Decimal("0")
    assert service.calcular_stock_por_lote_y_pileta(999, 999) == Decimal("0")


def test_calcular_stock_actual_por_pileta_lote_y_lote_pileta(
    db_session: Session,
    bodega,
    usuario_admin,
) -> None:
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    pileta = crear_pileta(db_session, bodega=bodega, catalogos=catalogos, codigo="P1")
    lote = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L1")
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 1, 9),
        litros=Decimal("100"),
        pileta_destino=pileta,
    )

    service = StockService(db_session)

    assert service.calcular_stock_actual_por_pileta(pileta.id) == Decimal("100.00")
    assert service.calcular_stock_actual_por_lote(lote.id) == Decimal("100.00")
    assert service.calcular_stock_por_lote_y_pileta(lote.id, pileta.id) == Decimal("100.00")


def test_multiples_entradas_y_salidas(db_session: Session, bodega, usuario_admin) -> None:
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    pileta = crear_pileta(db_session, bodega=bodega, catalogos=catalogos, codigo="P1")
    lote = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L1")
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 2, 9),
        litros=Decimal("50"),
        pileta_destino=pileta,
    )
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 1, 9),
        litros=Decimal("100"),
        pileta_destino=pileta,
    )
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 3, 9),
        litros=Decimal("40"),
        pileta_origen=pileta,
    )

    assert StockService(db_session).calcular_stock_por_lote_y_pileta(
        lote.id,
        pileta.id,
    ) == Decimal("110.00")


def test_trasiego_entre_piletas(db_session: Session, bodega, usuario_admin) -> None:
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    origen = crear_pileta(db_session, bodega=bodega, catalogos=catalogos, codigo="P1")
    destino = crear_pileta(db_session, bodega=bodega, catalogos=catalogos, codigo="P2")
    lote = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L1")
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 1, 9),
        litros=Decimal("100"),
        pileta_destino=origen,
    )
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 2, 9),
        litros=Decimal("30"),
        pileta_origen=origen,
        pileta_destino=destino,
    )

    service = StockService(db_session)

    assert service.calcular_stock_actual_por_pileta(origen.id) == Decimal("70.00")
    assert service.calcular_stock_actual_por_pileta(destino.id) == Decimal("30.00")
    assert service.calcular_stock_actual_por_lote(lote.id) == Decimal("100.00")


def test_calcular_stock_historico_hasta_y_movimientos_por_fecha(
    db_session: Session,
    bodega,
    usuario_admin,
) -> None:
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    pileta = crear_pileta(db_session, bodega=bodega, catalogos=catalogos, codigo="P1")
    lote = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L1")
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 3, 9),
        litros=Decimal("40"),
        pileta_origen=pileta,
    )
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 1, 9),
        litros=Decimal("100"),
        pileta_destino=pileta,
    )

    service = StockService(db_session)

    assert service.calcular_stock_historico_hasta(
        datetime(2026, 1, 2, 23),
        lote_id=lote.id,
        pileta_id=pileta.id,
    ) == Decimal("100.00")
    assert service.calcular_stock_historico_hasta(
        datetime(2026, 1, 3, 23),
        lote_id=lote.id,
        pileta_id=pileta.id,
    ) == Decimal("60.00")


def test_validar_stock_disponible(db_session: Session, bodega, usuario_admin) -> None:
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    pileta = crear_pileta(db_session, bodega=bodega, catalogos=catalogos, codigo="P1")
    lote = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L1")
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 1, 9),
        litros=Decimal("100"),
        pileta_destino=pileta,
    )

    service = StockService(db_session)

    assert service.validar_stock_disponible(lote.id, pileta.id, Decimal("100"))
    assert not service.validar_stock_disponible(lote.id, pileta.id, Decimal("101"))
