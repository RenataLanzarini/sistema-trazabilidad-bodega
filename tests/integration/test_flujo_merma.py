from datetime import datetime
from decimal import Decimal

import pytest

from app.core.exceptions import BusinessRuleError
from app.models.movimiento_fisico import MovimientoFisico
from app.services.merma_service import MermaService
from app.services.stock_service import StockService
from tests.integration._helpers import crear_causa_merma, crear_contexto_con_stock


def test_flujo_merma_registra_merma_movimiento_salida_y_reduce_stock(
    db_session,
    bodega,
    usuario_admin,
):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-MERMA",
        codigo_pileta="P-MERMA",
        litros=Decimal("120"),
    )
    causa = crear_causa_merma(db_session)

    merma = MermaService(db_session).registrar_merma(
        operacion_productiva_id=contexto.catalogos.operacion.id,
        lote_id=contexto.lote.id,
        pileta_id=contexto.pileta.id,
        causa_merma_id=causa.id,
        responsable_id=usuario_admin.id,
        litros=Decimal("25"),
        fecha=datetime(2026, 1, 5, 10, 0, 0),
        observaciones="Merma controlada",
    )

    assert merma.id is not None
    assert merma.litros == Decimal("25")
    assert StockService(db_session).calcular_stock_por_lote_y_pileta(
        contexto.lote.id,
        contexto.pileta.id,
    ) == Decimal("95")

    movimientos_salida = (
        db_session.query(MovimientoFisico)
        .filter(
            MovimientoFisico.lote_id == contexto.lote.id,
            MovimientoFisico.pileta_origen_id == contexto.pileta.id,
        )
        .all()
    )
    assert len(movimientos_salida) == 1
    assert movimientos_salida[0].litros == Decimal("25")


def test_merma_no_permite_stock_negativo(db_session, bodega, usuario_admin):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-MERMA-NEG",
        codigo_pileta="P-MERMA-NEG",
        litros=Decimal("10"),
    )
    causa = crear_causa_merma(db_session, nombre="Derrame")

    with pytest.raises(BusinessRuleError, match="Stock insuficiente"):
        MermaService(db_session).registrar_merma(
            operacion_productiva_id=contexto.catalogos.operacion.id,
            lote_id=contexto.lote.id,
            pileta_id=contexto.pileta.id,
            causa_merma_id=causa.id,
            responsable_id=usuario_admin.id,
            litros=Decimal("11"),
            fecha=datetime(2026, 1, 5, 11, 0, 0),
        )


def test_merma_usa_una_transaccion_logica(db_session, bodega, usuario_admin, monkeypatch):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-MERMA-COMMIT",
        codigo_pileta="P-MERMA-COMMIT",
        litros=Decimal("80"),
    )
    causa = crear_causa_merma(db_session, nombre="Filtrado")
    commits = 0
    original_commit = db_session.commit

    def count_commit():
        nonlocal commits
        commits += 1
        original_commit()

    monkeypatch.setattr(db_session, "commit", count_commit)

    MermaService(db_session).registrar_merma(
        operacion_productiva_id=contexto.catalogos.operacion.id,
        lote_id=contexto.lote.id,
        pileta_id=contexto.pileta.id,
        causa_merma_id=causa.id,
        responsable_id=usuario_admin.id,
        litros=Decimal("5"),
        fecha=datetime(2026, 1, 5, 12, 0, 0),
    )

    assert commits == 1
