from datetime import datetime
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.models.movimiento_fisico import MovimientoFisico
from app.services.movimiento_fisico_service import MovimientoFisicoService
from tests.unit.services._helpers import (
    crear_catalogos_base,
    crear_lote,
    crear_movimiento,
    crear_pileta,
)


@pytest.fixture(autouse=True)
def disable_postgresql_advisory_locks(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.services.stock_service.StockService.bloquear_stock_operacion",
        lambda *args, **kwargs: None,
    )


@pytest.fixture
def movimiento_context(db_session: Session, bodega, usuario_admin):
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    origen = crear_pileta(
        db_session,
        bodega=bodega,
        catalogos=catalogos,
        codigo="P1",
        capacidad_litros=Decimal("100"),
    )
    destino = crear_pileta(
        db_session,
        bodega=bodega,
        catalogos=catalogos,
        codigo="P2",
        capacidad_litros=Decimal("100"),
    )
    lote = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L1")
    return catalogos, lote, origen, destino


def _payload(catalogos, lote, usuario_admin, **overrides):
    data = {
        "operacion_productiva_id": catalogos.operacion.id,
        "lote_id": lote.id,
        "responsable_id": usuario_admin.id,
        "fecha": datetime(2026, 1, 1, 9),
        "litros": Decimal("10"),
        "estado": "confirmado",
        "pileta_origen_id": None,
        "pileta_destino_id": None,
    }
    data.update(overrides)
    return data


def test_entrada_valida(db_session: Session, usuario_admin, movimiento_context) -> None:
    catalogos, lote, _, destino = movimiento_context

    movimiento = MovimientoFisicoService(db_session).registrar_movimiento(
        **_payload(catalogos, lote, usuario_admin, pileta_destino_id=destino.id)
    )

    assert movimiento.id is not None
    assert movimiento.pileta_destino_id == destino.id


def test_salida_valida(db_session: Session, usuario_admin, movimiento_context) -> None:
    catalogos, lote, origen, _ = movimiento_context
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 1, 8),
        litros=Decimal("30"),
        pileta_destino=origen,
    )

    movimiento = MovimientoFisicoService(db_session).registrar_movimiento(
        **_payload(catalogos, lote, usuario_admin, pileta_origen_id=origen.id)
    )

    assert movimiento.pileta_origen_id == origen.id


def test_trasiego_valido(db_session: Session, usuario_admin, movimiento_context) -> None:
    catalogos, lote, origen, destino = movimiento_context
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 1, 8),
        litros=Decimal("30"),
        pileta_destino=origen,
    )

    movimiento = MovimientoFisicoService(db_session).registrar_movimiento(
        **_payload(
            catalogos,
            lote,
            usuario_admin,
            pileta_origen_id=origen.id,
            pileta_destino_id=destino.id,
        )
    )

    assert movimiento.pileta_origen_id == origen.id
    assert movimiento.pileta_destino_id == destino.id


@pytest.mark.parametrize(
    "overrides",
    [
        {"litros": Decimal("0"), "pileta_destino_id": 1},
        {"litros": Decimal("-1"), "pileta_destino_id": 1},
    ],
)
def test_litros_menor_o_igual_a_cero(
    db_session: Session,
    usuario_admin,
    movimiento_context,
    overrides,
) -> None:
    catalogos, lote, _, _ = movimiento_context

    with pytest.raises(BusinessRuleError):
        MovimientoFisicoService(db_session).registrar_movimiento(
            **_payload(catalogos, lote, usuario_admin, **overrides)
        )


def test_origen_y_destino_iguales(db_session: Session, usuario_admin, movimiento_context) -> None:
    catalogos, lote, origen, _ = movimiento_context

    with pytest.raises(BusinessRuleError):
        MovimientoFisicoService(db_session).registrar_movimiento(
            **_payload(
                catalogos,
                lote,
                usuario_admin,
                pileta_origen_id=origen.id,
                pileta_destino_id=origen.id,
            )
        )


def test_sin_origen_ni_destino(db_session: Session, usuario_admin, movimiento_context) -> None:
    catalogos, lote, _, _ = movimiento_context

    with pytest.raises(BusinessRuleError):
        MovimientoFisicoService(db_session).registrar_movimiento(
            **_payload(catalogos, lote, usuario_admin)
        )


def test_lote_inexistente(db_session: Session, usuario_admin, movimiento_context) -> None:
    catalogos, lote, _, destino = movimiento_context

    with pytest.raises(NotFoundError):
        MovimientoFisicoService(db_session).registrar_movimiento(
            **_payload(
                catalogos,
                lote,
                usuario_admin,
                lote_id=999,
                pileta_destino_id=destino.id,
            )
        )


def test_usuario_inexistente(db_session: Session, usuario_admin, movimiento_context) -> None:
    catalogos, lote, _, destino = movimiento_context

    with pytest.raises(NotFoundError):
        MovimientoFisicoService(db_session).registrar_movimiento(
            **_payload(
                catalogos,
                lote,
                usuario_admin,
                responsable_id=999,
                pileta_destino_id=destino.id,
            )
        )


def test_operacion_inexistente(db_session: Session, usuario_admin, movimiento_context) -> None:
    catalogos, lote, _, destino = movimiento_context

    with pytest.raises(NotFoundError):
        MovimientoFisicoService(db_session).registrar_movimiento(
            **_payload(
                catalogos,
                lote,
                usuario_admin,
                operacion_productiva_id=999,
                pileta_destino_id=destino.id,
            )
        )


def test_capacidad_maxima_de_pileta(db_session: Session, usuario_admin, movimiento_context) -> None:
    catalogos, lote, _, destino = movimiento_context
    crear_movimiento(
        db_session,
        operacion=catalogos.operacion,
        lote=lote,
        responsable=usuario_admin,
        fecha=datetime(2026, 1, 1, 8),
        litros=Decimal("95"),
        pileta_destino=destino,
    )

    with pytest.raises(BusinessRuleError):
        MovimientoFisicoService(db_session).registrar_movimiento(
            **_payload(
                catalogos,
                lote,
                usuario_admin,
                litros=Decimal("10"),
                pileta_destino_id=destino.id,
            )
        )


def test_stock_insuficiente(db_session: Session, usuario_admin, movimiento_context) -> None:
    catalogos, lote, origen, _ = movimiento_context

    with pytest.raises(BusinessRuleError):
        MovimientoFisicoService(db_session).registrar_movimiento(
            **_payload(
                catalogos,
                lote,
                usuario_admin,
                litros=Decimal("1"),
                pileta_origen_id=origen.id,
            )
        )


def test_commit_correcto(
    db_session: Session,
    usuario_admin,
    movimiento_context,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalogos, lote, _, destino = movimiento_context
    llamado = {"commit": False}
    original_commit = db_session.commit

    def commit_spy():
        llamado["commit"] = True
        original_commit()

    monkeypatch.setattr(db_session, "commit", commit_spy)

    MovimientoFisicoService(db_session).registrar_movimiento(
        **_payload(catalogos, lote, usuario_admin, pileta_destino_id=destino.id)
    )

    assert llamado["commit"]


def test_rollback_ante_error(
    db_session: Session,
    usuario_admin,
    movimiento_context,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalogos, lote, _, destino = movimiento_context
    service = MovimientoFisicoService(db_session)
    llamado = {"rollback": False}

    def add_error(_: MovimientoFisico) -> MovimientoFisico:
        raise RuntimeError("fallo persistencia")

    def rollback_spy():
        llamado["rollback"] = True

    monkeypatch.setattr(service.movimiento_repository, "add", add_error)
    monkeypatch.setattr(db_session, "rollback", rollback_spy)

    with pytest.raises(RuntimeError):
        service.registrar_movimiento(
            **_payload(catalogos, lote, usuario_admin, pileta_destino_id=destino.id)
        )

    assert llamado["rollback"]
