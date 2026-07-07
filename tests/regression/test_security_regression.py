import pytest
from fastapi.testclient import TestClient


PUBLIC_GET_ENDPOINTS = [
    "/api/v1/bodegas",
    "/api/v1/piletas",
    "/api/v1/lotes",
    "/api/v1/recepciones-uva",
    "/api/v1/stock/piletas/1",
    "/api/v1/trazabilidad/lotes/1/grafo",
]

PROTECTED_WRITE_ENDPOINTS = [
    ("post", "/api/v1/recepciones-uva"),
    ("post", "/api/v1/lotes"),
    ("post", "/api/v1/piletas"),
    ("post", "/api/v1/operaciones-productivas"),
    ("patch", "/api/v1/operaciones-productivas/1/anular"),
    ("post", "/api/v1/movimientos-fisicos"),
    ("post", "/api/v1/mermas"),
    ("post", "/api/v1/fraccionamientos"),
    ("post", "/api/v1/ventas-granel"),
    ("post", "/api/v1/analisis-enologicos"),
    ("post", "/api/v1/mediciones-fermentacion"),
    ("post", "/api/v1/ordenes-trabajo"),
    ("patch", "/api/v1/ordenes-trabajo/1/completar"),
    ("patch", "/api/v1/ordenes-trabajo/1/vincular-operacion"),
    ("post", "/api/v1/cortes-teoricos"),
    ("post", "/api/v1/cortes-teoricos/1/detalles"),
    ("patch", "/api/v1/cortes-teoricos/1/vincular-operacion"),
]


@pytest.mark.parametrize("path", PUBLIC_GET_ENDPOINTS)
def test_get_publicos_siguen_publicos(client: TestClient, bodega, path: str) -> None:
    response = client.get(path)

    assert response.status_code != 401
    assert response.status_code != 403


def test_auth_me_sigue_protegido(client: TestClient) -> None:
    assert client.get("/api/v1/auth/me").status_code == 401


@pytest.mark.parametrize(("method", "path"), PROTECTED_WRITE_ENDPOINTS)
def test_post_patch_siguen_protegidos_sin_token(
    client: TestClient,
    method: str,
    path: str,
) -> None:
    response = getattr(client, method)(path, json={})

    assert response.status_code == 401


@pytest.mark.parametrize(("method", "path"), PROTECTED_WRITE_ENDPOINTS)
def test_post_patch_siguen_rechazando_rol_no_autorizado(
    client: TestClient,
    auth_headers_operario: dict[str, str],
    method: str,
    path: str,
) -> None:
    response = getattr(client, method)(path, json={}, headers=auth_headers_operario)

    assert response.status_code == 403


@pytest.mark.parametrize("headers_fixture", ["auth_headers_admin", "auth_headers_enologo"])
@pytest.mark.parametrize(("method", "path"), PROTECTED_WRITE_ENDPOINTS)
def test_roles_autorizados_superan_autorizacion(
    client: TestClient,
    request: pytest.FixtureRequest,
    headers_fixture: str,
    method: str,
    path: str,
) -> None:
    headers = request.getfixturevalue(headers_fixture)
    response = getattr(client, method)(path, json={}, headers=headers)

    assert response.status_code != 401
    assert response.status_code != 403
