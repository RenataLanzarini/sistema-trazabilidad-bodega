import pytest
from fastapi.testclient import TestClient


PUBLIC_ENDPOINTS = [
    "/health",
    "/api/v1/health",
    "/api/v1/bodegas",
    "/api/v1/depositos",
    "/api/v1/roles",
    "/api/v1/usuarios",
    "/api/v1/variedades",
    "/api/v1/estados-lote",
    "/api/v1/estados-pileta",
    "/api/v1/tipos-producto",
    "/api/v1/tipos-operacion",
    "/api/v1/causas-merma",
    "/api/v1/clientes",
    "/api/v1/calificaciones-vino",
    "/api/v1/tareas-orden-trabajo",
    "/api/v1/recepciones-uva",
    "/api/v1/lotes",
    "/api/v1/piletas",
    "/api/v1/operaciones-productivas",
    "/api/v1/productos-terminados",
    "/api/v1/analisis-enologicos",
    "/api/v1/mediciones-fermentacion",
    "/api/v1/ordenes-trabajo",
    "/api/v1/cortes-teoricos",
]

PARAMETRIZED_READ_ENDPOINTS = [
    "/api/v1/stock/piletas/1",
    "/api/v1/stock/lotes/1",
    "/api/v1/stock/lotes/1/piletas/1",
    "/api/v1/stock/historico?fecha=2026-01-01T00:00:00",
    "/api/v1/stock/validar-disponibilidad?lote_id=1&pileta_id=1&litros=1",
    "/api/v1/trazabilidad/lotes/1/padres",
    "/api/v1/trazabilidad/lotes/1/hijos",
    "/api/v1/trazabilidad/lotes/1/hacia-atras",
    "/api/v1/trazabilidad/lotes/1/hacia-adelante",
    "/api/v1/trazabilidad/lotes/1/grafo",
    "/api/v1/movimientos-fisicos/lote/1",
    "/api/v1/movimientos-fisicos/pileta/1",
    "/api/v1/movimientos-fisicos/operacion/1",
    "/api/v1/mermas/lote/1",
    "/api/v1/mermas/pileta/1",
    "/api/v1/mermas/causa/1",
    "/api/v1/mermas/operacion/1",
    "/api/v1/fraccionamientos/lote/1",
    "/api/v1/ventas-granel/cliente/1",
    "/api/v1/ventas-granel/operacion/1",
]


@pytest.mark.parametrize("path", PUBLIC_ENDPOINTS)
def test_endpoints_publicos_principales_responden_sin_token(
    client: TestClient,
    bodega,
    path: str,
) -> None:
    response = client.get(path)

    assert response.status_code < 500


@pytest.mark.parametrize("path", PARAMETRIZED_READ_ENDPOINTS)
def test_endpoints_principales_con_parametros_no_rompen(
    client: TestClient,
    path: str,
) -> None:
    response = client.get(path)

    assert response.status_code < 500


def test_login_response_mantiene_contrato_minimo(client: TestClient, usuario_admin) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": usuario_admin.email, "password": "clave-segura"},
    )

    assert response.status_code == 200
    data = response.json()
    assert set(data) == {"access_token", "token_type"}
    assert isinstance(data["access_token"], str)
    assert data["token_type"] == "bearer"


def test_stock_response_mantiene_tipos_esperados(client: TestClient) -> None:
    response = client.get("/api/v1/stock/piletas/1")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["pileta_id"], int)
    assert isinstance(data["litros"], int | float | str)
