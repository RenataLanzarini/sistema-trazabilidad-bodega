from datetime import date
from decimal import Decimal

from app.models.relacion_genealogica_lote import RelacionGenealogicaLote
from app.services.corte_teorico_service import CorteTeoricoService
from app.services.stock_service import StockService
from tests.integration._helpers import crear_contexto_con_stock


def test_flujo_corte_teorico_crear_detalle_y_vincular_no_modifica_stock_ni_genealogia(
    db_session,
    bodega,
    usuario_admin,
):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-CORTE",
        codigo_pileta="P-CORTE",
        litros=Decimal("180"),
    )
    stock_service = StockService(db_session)
    stock_inicial = stock_service.calcular_stock_por_lote_y_pileta(
        contexto.lote.id,
        contexto.pileta.id,
    )
    genealogia_inicial = db_session.query(RelacionGenealogicaLote).count()

    service = CorteTeoricoService(db_session)
    corte = service.crear_corte_teorico(
        responsable_id=usuario_admin.id,
        codigo_externo="CT-T3-001",
        fecha=date(2026, 1, 10),
        nombre="Corte teorico test",
    )
    detalle = service.crear_detalle_corte(
        corte.id,
        pileta_id=contexto.pileta.id,
        lote_id=contexto.lote.id,
        volumen_al_corte=Decimal("50"),
        varietal_snapshot="Malbec",
        volumen_actual_snapshot=stock_inicial,
        alcohol=Decimal("13.5"),
        ph=Decimal("3.6"),
    )
    vinculado = service.vincular_operacion_productiva(
        corte.id,
        contexto.catalogos.operacion.id,
    )

    assert corte.id is not None
    assert detalle.corte_teorico_id == corte.id
    assert vinculado.operacion_productiva_id == contexto.catalogos.operacion.id
    assert service.obtener_detalles_por_corte(corte.id) == [detalle]
    assert stock_service.calcular_stock_por_lote_y_pileta(
        contexto.lote.id,
        contexto.pileta.id,
    ) == stock_inicial
    assert db_session.query(RelacionGenealogicaLote).count() == genealogia_inicial


def test_corte_teorico_listados_por_fecha_y_responsable(
    db_session,
    bodega,
    usuario_admin,
):
    crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-CORTE-LIST",
        codigo_pileta="P-CORTE-LIST",
        litros=Decimal("70"),
    )
    service = CorteTeoricoService(db_session)
    corte = service.crear_corte_teorico(
        responsable_id=usuario_admin.id,
        codigo_externo="CT-T3-002",
        fecha=date(2026, 1, 11),
        nombre="Corte listado",
    )

    assert corte in service.listar_por_responsable(usuario_admin.id)
    assert corte in service.listar_por_fecha(date(2026, 1, 11))
