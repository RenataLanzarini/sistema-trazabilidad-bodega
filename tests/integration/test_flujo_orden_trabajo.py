from datetime import datetime
from decimal import Decimal

from app.services.orden_trabajo_service import OrdenTrabajoService
from app.services.stock_service import StockService
from tests.integration._helpers import crear_contexto_con_stock, crear_tarea_orden_trabajo


def test_flujo_orden_trabajo_completar_y_vincular_no_modifica_stock(
    db_session,
    bodega,
    usuario_admin,
    usuario_operario,
):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-OT",
        codigo_pileta="P-OT",
        litros=Decimal("110"),
    )
    tarea = crear_tarea_orden_trabajo(db_session)
    stock_service = StockService(db_session)
    stock_inicial = stock_service.calcular_stock_por_lote_y_pileta(
        contexto.lote.id,
        contexto.pileta.id,
    )

    service = OrdenTrabajoService(db_session)
    orden = service.crear_orden_trabajo(
        tarea_orden_trabajo_id=tarea.id,
        pileta_id=contexto.pileta.id,
        lote_id=contexto.lote.id,
        operario_id=usuario_operario.id,
        fecha=datetime(2026, 1, 8).date(),
        numero="OT-T3-001",
        completada=False,
        litros_a_trasegar=Decimal("20"),
    )

    assert orden.id is not None
    assert orden.completada is False
    assert stock_service.calcular_stock_por_lote_y_pileta(
        contexto.lote.id,
        contexto.pileta.id,
    ) == stock_inicial

    completada = service.marcar_completada(
        orden.id,
        fecha_completada=datetime(2026, 1, 8, 17, 0, 0),
        observaciones_completada="Trabajo realizado",
    )
    vinculada = service.vincular_operacion_productiva(
        completada.id,
        contexto.catalogos.operacion.id,
    )

    assert vinculada.completada is True
    assert vinculada.fecha_completada == datetime(2026, 1, 8, 17, 0, 0)
    assert vinculada.operacion_productiva_id == contexto.catalogos.operacion.id
    assert stock_service.calcular_stock_por_lote_y_pileta(
        contexto.lote.id,
        contexto.pileta.id,
    ) == stock_inicial


def test_orden_trabajo_listados_operativos(
    db_session,
    bodega,
    usuario_admin,
    usuario_operario,
):
    contexto = crear_contexto_con_stock(
        db_session,
        bodega=bodega,
        usuario=usuario_admin,
        codigo_lote="L-OT-LIST",
        codigo_pileta="P-OT-LIST",
        litros=Decimal("40"),
    )
    tarea = crear_tarea_orden_trabajo(db_session, nombre="Agregar insumo")
    service = OrdenTrabajoService(db_session)
    orden = service.crear_orden_trabajo(
        tarea_orden_trabajo_id=tarea.id,
        pileta_id=contexto.pileta.id,
        lote_id=contexto.lote.id,
        operario_id=usuario_operario.id,
        fecha=datetime(2026, 1, 9).date(),
        numero="OT-T3-002",
        completada=False,
    )

    assert orden in service.listar_pendientes()
    assert orden in service.listar_por_operario(usuario_operario.id)
    assert orden in service.listar_por_pileta(contexto.pileta.id)
    assert orden in service.listar_por_lote(contexto.lote.id)

    completada = service.marcar_completada(
        orden.id,
        fecha_completada=datetime(2026, 1, 9, 16, 0, 0),
    )
    assert completada in service.listar_completadas()
