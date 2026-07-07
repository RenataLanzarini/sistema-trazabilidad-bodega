from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from app.core.exceptions import BusinessRuleError
from app.repositories.movimiento_fisico_repository import MovimientoFisicoRepository
from app.schemas.lote import LoteCreate
from app.schemas.recepcion_uva import RecepcionUvaCreate
from app.services.lote_service import LoteService
from app.services.movimiento_fisico_service import MovimientoFisicoService
from app.services.operacion_productiva_service import OperacionProductivaService
from app.services.recepcion_uva_service import RecepcionUvaService
from app.services.stock_service import StockService
from tests.integration._helpers import crear_origen_uva, crear_variedad
from tests.unit.services._helpers import crear_catalogos_base, crear_pileta


def test_flujo_recepcion_lote_movimiento_actualiza_stock(
    db_session,
    bodega,
    usuario_admin,
):
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    variedad = crear_variedad(db_session)
    origen = crear_origen_uva(db_session)
    pileta = crear_pileta(
        db_session,
        bodega=bodega,
        catalogos=catalogos,
        codigo="P-REC",
        capacidad_litros=Decimal("500"),
    )

    recepcion = RecepcionUvaService(db_session).crear_recepcion(
        RecepcionUvaCreate(
            bodega_id=bodega.id,
            origen_uva_id=origen.id,
            variedad_id=variedad.id,
            responsable_id=usuario_admin.id,
            numero_ciu="CIU-T3-001",
            fecha=date(2026, 1, 2),
            cosecha=2026,
            kilos_recibidos=Decimal("1200"),
            estado="recibida",
        )
    )
    lote = LoteService(db_session).crear_lote(
        LoteCreate(
            bodega_id=bodega.id,
            tipo_producto_id=catalogos.tipo_producto.id,
            estado_lote_id=catalogos.estado_lote.id,
            recepcion_uva_id=recepcion.id,
            variedad_principal_id=variedad.id,
            codigo="L-REC-T3-001",
            fecha_nacimiento=date(2026, 1, 2),
            cosecha=2026,
        )
    )
    operacion = OperacionProductivaService(db_session).crear_operacion(
        bodega_id=bodega.id,
        tipo_operacion_id=catalogos.tipo_operacion.id,
        responsable_id=usuario_admin.id,
        fecha=datetime(2026, 1, 2, 10, 0, 0),
        estado="registrada",
    )

    MovimientoFisicoService(db_session).registrar_movimiento(
        operacion_productiva_id=operacion.id,
        lote_id=lote.id,
        responsable_id=usuario_admin.id,
        fecha=datetime(2026, 1, 2, 11, 0, 0),
        litros=Decimal("300"),
        estado="registrado",
        pileta_destino_id=pileta.id,
    )

    stock_service = StockService(db_session)
    assert stock_service.calcular_stock_actual_por_pileta(pileta.id) == Decimal("300")
    assert stock_service.calcular_stock_actual_por_lote(lote.id) == Decimal("300")
    assert stock_service.calcular_stock_por_lote_y_pileta(lote.id, pileta.id) == Decimal("300")


def test_movimiento_no_supera_capacidad_de_pileta(db_session, bodega, usuario_admin):
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    lote = LoteService(db_session).crear_lote(
        LoteCreate(
            bodega_id=bodega.id,
            tipo_producto_id=catalogos.tipo_producto.id,
            estado_lote_id=catalogos.estado_lote.id,
            codigo="L-CAP-T3",
            fecha_nacimiento=date(2026, 1, 3),
        )
    )
    pileta = crear_pileta(
        db_session,
        bodega=bodega,
        catalogos=catalogos,
        codigo="P-CAP",
        capacidad_litros=Decimal("100"),
    )

    service = MovimientoFisicoService(db_session)
    service.registrar_movimiento(
        operacion_productiva_id=catalogos.operacion.id,
        lote_id=lote.id,
        responsable_id=usuario_admin.id,
        fecha=datetime(2026, 1, 3, 9, 0, 0),
        litros=Decimal("90"),
        estado="registrado",
        pileta_destino_id=pileta.id,
    )

    with pytest.raises(BusinessRuleError, match="capacidad"):
        service.registrar_movimiento(
            operacion_productiva_id=catalogos.operacion.id,
            lote_id=lote.id,
            responsable_id=usuario_admin.id,
            fecha=datetime(2026, 1, 3, 10, 0, 0),
            litros=Decimal("20"),
            estado="registrado",
            pileta_destino_id=pileta.id,
        )


def test_repositories_no_contienen_commits_ni_rollbacks():
    repository_files = Path("app/repositories").glob("*.py")
    forbidden = (".commit(", ".rollback(")

    for repository_file in repository_files:
        content = repository_file.read_text(encoding="utf-8")
        assert not any(token in content for token in forbidden), repository_file


def test_movimientos_del_flujo_se_persisten_en_repository(
    db_session,
    bodega,
    usuario_admin,
):
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    lote = LoteService(db_session).crear_lote(
        LoteCreate(
            bodega_id=bodega.id,
            tipo_producto_id=catalogos.tipo_producto.id,
            estado_lote_id=catalogos.estado_lote.id,
            codigo="L-REPO-T3",
            fecha_nacimiento=date(2026, 1, 4),
        )
    )
    pileta = crear_pileta(
        db_session,
        bodega=bodega,
        catalogos=catalogos,
        codigo="P-REPO",
    )

    movimiento = MovimientoFisicoService(db_session).registrar_movimiento(
        operacion_productiva_id=catalogos.operacion.id,
        lote_id=lote.id,
        responsable_id=usuario_admin.id,
        fecha=datetime(2026, 1, 4, 9, 0, 0),
        litros=Decimal("50"),
        estado="registrado",
        pileta_destino_id=pileta.id,
    )

    movimientos = MovimientoFisicoRepository(db_session).list_by_lote(lote.id)
    assert [item.id for item in movimientos] == [movimiento.id]
