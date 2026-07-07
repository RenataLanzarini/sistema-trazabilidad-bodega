from datetime import date, datetime
from decimal import Decimal

import pytest

from app.core.exceptions import BusinessRuleError
from app.models.movimiento_fisico import MovimientoFisico
from app.models.producto_terminado import ProductoTerminado
from app.services.fraccionamiento_service import FraccionamientoService
from app.services.stock_service import StockService
from tests.integration._helpers import crear_contexto_con_stock


def test_flujo_fraccionamiento_crea_detalle_producto_y_reduce_stock(
    db_session,
    bodega,
    usuario_admin,
):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-FRAC",
        codigo_pileta="P-FRAC",
        litros=Decimal("200"),
    )

    fraccionamiento = FraccionamientoService(db_session).crear_fraccionamiento(
        operacion_productiva_id=contexto.catalogos.operacion.id,
        responsable_id=usuario_admin.id,
        fecha=datetime(2026, 1, 6, 9, 0, 0),
        estado="registrado",
        detalles=[
            {
                "lote_id": contexto.lote.id,
                "pileta_id": contexto.pileta.id,
                "litros_consumidos": Decimal("75"),
            }
        ],
        productos_terminados=[
            {
                "tipo_producto_id": contexto.catalogos.tipo_producto.id,
                "lote_id": contexto.lote.id,
                "codigo": "PT-FRAC-T3",
                "cantidad_unidades": 100,
                "volumen_unidad_ml": 750,
                "litros_totales": Decimal("75"),
                "fecha_produccion": date(2026, 1, 6),
                "estado": "disponible",
            }
        ],
    )

    assert fraccionamiento.id is not None
    assert len(fraccionamiento.detalles) == 1
    assert StockService(db_session).calcular_stock_por_lote_y_pileta(
        contexto.lote.id,
        contexto.pileta.id,
    ) == Decimal("125")

    producto = (
        db_session.query(ProductoTerminado)
        .filter(ProductoTerminado.fraccionamiento_id == fraccionamiento.id)
        .one()
    )
    assert producto.codigo == "PT-FRAC-T3"
    assert producto.litros_totales == Decimal("75")

    salida = (
        db_session.query(MovimientoFisico)
        .filter(
            MovimientoFisico.lote_id == contexto.lote.id,
            MovimientoFisico.pileta_origen_id == contexto.pileta.id,
            MovimientoFisico.litros == Decimal("75"),
        )
        .one()
    )
    assert salida.pileta_destino_id is None


def test_fraccionamiento_no_permite_stock_negativo(db_session, bodega, usuario_admin):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-FRAC-NEG",
        codigo_pileta="P-FRAC-NEG",
        litros=Decimal("20"),
    )

    with pytest.raises(BusinessRuleError, match="Stock insuficiente"):
        FraccionamientoService(db_session).crear_fraccionamiento(
            operacion_productiva_id=contexto.catalogos.operacion.id,
            responsable_id=usuario_admin.id,
            fecha=datetime(2026, 1, 6, 10, 0, 0),
            estado="registrado",
            detalles=[
                {
                    "lote_id": contexto.lote.id,
                    "pileta_id": contexto.pileta.id,
                    "litros_consumidos": Decimal("21"),
                }
            ],
            productos_terminados=[],
        )


def test_fraccionamiento_usa_una_transaccion_logica(
    db_session,
    bodega,
    usuario_admin,
    monkeypatch,
):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-FRAC-COMMIT",
        codigo_pileta="P-FRAC-COMMIT",
        litros=Decimal("100"),
    )
    commits = 0
    original_commit = db_session.commit

    def count_commit():
        nonlocal commits
        commits += 1
        original_commit()

    monkeypatch.setattr(db_session, "commit", count_commit)

    FraccionamientoService(db_session).crear_fraccionamiento(
        operacion_productiva_id=contexto.catalogos.operacion.id,
        responsable_id=usuario_admin.id,
        fecha=datetime(2026, 1, 6, 11, 0, 0),
        estado="registrado",
        detalles=[
            {
                "lote_id": contexto.lote.id,
                "pileta_id": contexto.pileta.id,
                "litros_consumidos": Decimal("10"),
            }
        ],
        productos_terminados=[],
    )

    assert commits == 1
