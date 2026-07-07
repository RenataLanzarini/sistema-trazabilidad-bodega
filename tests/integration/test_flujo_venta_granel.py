from datetime import datetime
from decimal import Decimal

import pytest

from app.core.exceptions import BusinessRuleError
from app.models.movimiento_fisico import MovimientoFisico
from app.services.stock_service import StockService
from app.services.venta_granel_service import VentaGranelService
from tests.integration._helpers import crear_cliente, crear_contexto_con_stock


def test_flujo_venta_granel_persiste_venta_salida_y_reduce_stock(
    db_session,
    bodega,
    usuario_admin,
):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-VG",
        codigo_pileta="P-VG",
        litros=Decimal("150"),
    )
    cliente = crear_cliente(db_session)

    venta = VentaGranelService(db_session).crear_venta_granel(
        operacion_productiva_id=contexto.catalogos.operacion.id,
        cliente_id=cliente.id,
        responsable_id=usuario_admin.id,
        fecha=datetime(2026, 1, 7, 9, 0, 0),
        estado="registrada",
        documento="REM-T3-001",
        detalles=[
            {
                "lote_id": contexto.lote.id,
                "pileta_id": contexto.pileta.id,
                "litros": Decimal("60"),
            }
        ],
    )

    assert venta.id is not None
    assert len(venta.detalles) == 1
    assert venta.detalles[0].litros == Decimal("60")
    assert StockService(db_session).calcular_stock_por_lote_y_pileta(
        contexto.lote.id,
        contexto.pileta.id,
    ) == Decimal("90")

    salida = (
        db_session.query(MovimientoFisico)
        .filter(
            MovimientoFisico.lote_id == contexto.lote.id,
            MovimientoFisico.pileta_origen_id == contexto.pileta.id,
            MovimientoFisico.litros == Decimal("60"),
        )
        .one()
    )
    assert salida.pileta_destino_id is None


def test_venta_granel_no_permite_stock_negativo(db_session, bodega, usuario_admin):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-VG-NEG",
        codigo_pileta="P-VG-NEG",
        litros=Decimal("30"),
    )
    cliente = crear_cliente(db_session, nombre="Cliente Stock")

    with pytest.raises(BusinessRuleError, match="Stock insuficiente"):
        VentaGranelService(db_session).crear_venta_granel(
            operacion_productiva_id=contexto.catalogos.operacion.id,
            cliente_id=cliente.id,
            responsable_id=usuario_admin.id,
            fecha=datetime(2026, 1, 7, 10, 0, 0),
            estado="registrada",
            detalles=[
                {
                    "lote_id": contexto.lote.id,
                    "pileta_id": contexto.pileta.id,
                    "litros": Decimal("31"),
                }
            ],
        )


def test_venta_granel_usa_una_transaccion_logica(
    db_session,
    bodega,
    usuario_admin,
    monkeypatch,
):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-VG-COMMIT",
        codigo_pileta="P-VG-COMMIT",
        litros=Decimal("90"),
    )
    cliente = crear_cliente(db_session, nombre="Cliente Commit")
    commits = 0
    original_commit = db_session.commit

    def count_commit():
        nonlocal commits
        commits += 1
        original_commit()

    monkeypatch.setattr(db_session, "commit", count_commit)

    VentaGranelService(db_session).crear_venta_granel(
        operacion_productiva_id=contexto.catalogos.operacion.id,
        cliente_id=cliente.id,
        responsable_id=usuario_admin.id,
        fecha=datetime(2026, 1, 7, 11, 0, 0),
        estado="registrada",
        detalles=[
            {
                "lote_id": contexto.lote.id,
                "pileta_id": contexto.pileta.id,
                "litros": Decimal("15"),
            }
        ],
    )

    assert commits == 1
