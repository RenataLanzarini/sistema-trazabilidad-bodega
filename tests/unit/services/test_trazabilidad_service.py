from decimal import Decimal

from sqlalchemy.orm import Session

from app.services.trazabilidad_service import TrazabilidadService
from tests.unit.services._helpers import crear_catalogos_base, crear_lote, crear_relacion


def test_lote_sin_genealogia(db_session: Session, bodega, usuario_admin) -> None:
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    lote = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L1")
    service = TrazabilidadService(db_session)

    assert service.obtener_padres(lote.id) == []
    assert service.obtener_hijos(lote.id) == []
    assert service.recorrer_hacia_atras(lote.id) == []
    assert service.recorrer_hacia_adelante(lote.id) == []
    assert service.construir_grafo_base(lote.id) == {
        "nodos": [{"lote_id": lote.id}],
        "aristas": [],
    }


def test_obtener_padres_e_hijos(db_session: Session, bodega, usuario_admin) -> None:
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    padre = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="PADRE")
    hijo = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="HIJO")
    relacion = crear_relacion(
        db_session,
        operacion=catalogos.operacion,
        lote_padre=padre,
        lote_hijo=hijo,
        litros_aportados=Decimal("80"),
    )
    service = TrazabilidadService(db_session)

    assert service.obtener_padres(hijo.id) == [relacion]
    assert service.obtener_hijos(padre.id) == [relacion]


def test_recorrer_hacia_atras_varios_niveles(db_session: Session, bodega, usuario_admin) -> None:
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    abuelo = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L1")
    padre = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L2")
    hijo = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L3")
    rel_1 = crear_relacion(
        db_session,
        operacion=catalogos.operacion,
        lote_padre=abuelo,
        lote_hijo=padre,
    )
    rel_2 = crear_relacion(
        db_session,
        operacion=catalogos.operacion,
        lote_padre=padre,
        lote_hijo=hijo,
    )

    assert TrazabilidadService(db_session).recorrer_hacia_atras(hijo.id) == [rel_2, rel_1]


def test_recorrer_hacia_adelante_varios_niveles(
    db_session: Session,
    bodega,
    usuario_admin,
) -> None:
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    padre = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L1")
    hijo = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L2")
    nieto = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L3")
    rel_1 = crear_relacion(
        db_session,
        operacion=catalogos.operacion,
        lote_padre=padre,
        lote_hijo=hijo,
    )
    rel_2 = crear_relacion(
        db_session,
        operacion=catalogos.operacion,
        lote_padre=hijo,
        lote_hijo=nieto,
    )

    assert TrazabilidadService(db_session).recorrer_hacia_adelante(padre.id) == [
        rel_1,
        rel_2,
    ]


def test_grafo_base(db_session: Session, bodega, usuario_admin) -> None:
    catalogos = crear_catalogos_base(db_session, bodega, usuario_admin)
    padre = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L1")
    hijo = crear_lote(db_session, bodega=bodega, catalogos=catalogos, codigo="L2")
    relacion = crear_relacion(
        db_session,
        operacion=catalogos.operacion,
        lote_padre=padre,
        lote_hijo=hijo,
        litros_aportados=Decimal("55"),
        tipo_relacion="division",
    )

    grafo = TrazabilidadService(db_session).construir_grafo_base(hijo.id)

    assert grafo["nodos"] == [{"lote_id": padre.id}, {"lote_id": hijo.id}]
    assert grafo["aristas"] == [
        {
            "relacion_id": relacion.id,
            "operacion_productiva_id": catalogos.operacion.id,
            "lote_padre_id": padre.id,
            "lote_hijo_id": hijo.id,
            "litros_aportados": Decimal("55.00"),
            "tipo_relacion": "division",
        }
    ]
