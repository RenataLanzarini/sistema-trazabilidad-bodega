import pytest
from fastapi.testclient import TestClient


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


def test_health_openapi_and_docs(client: TestClient) -> None:
    assert client.get("/health").status_code == 200
    assert client.get("/api/v1/health").status_code == 200
    assert client.get("/openapi.json").status_code == 200
    assert client.get("/docs").status_code == 200


def test_login_valido_devuelve_token_bearer(client: TestClient, usuario_admin) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": usuario_admin.email, "password": "clave-segura"},
    )

    assert response.status_code == 200
    data = response.json()
    assert set(data) == {"access_token", "token_type"}
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_email_inexistente_devuelve_401(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "noexiste@example.com", "password": "clave-segura"},
    )

    assert response.status_code == 401


def test_login_password_incorrecto_devuelve_401(client: TestClient, usuario_admin) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": usuario_admin.email, "password": "incorrecta"},
    )

    assert response.status_code == 401


def test_login_usuario_inactivo_devuelve_401(client: TestClient, usuario_inactivo) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": usuario_inactivo.email, "password": "clave-segura"},
    )

    assert response.status_code == 401


def test_auth_me_sin_token_devuelve_401(client: TestClient) -> None:
    assert client.get("/api/v1/auth/me").status_code == 401


def test_auth_me_token_invalido_devuelve_401(client: TestClient) -> None:
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == 401


def test_auth_me_token_valido_devuelve_usuario_seguro(
    client: TestClient,
    usuario_admin,
    auth_headers_admin: dict[str, str],
) -> None:
    response = client.get("/api/v1/auth/me", headers=auth_headers_admin)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == usuario_admin.id
    assert data["email"] == usuario_admin.email
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.parametrize(
    "path",
    [
        "/api/v1/bodegas",
        "/api/v1/piletas",
        "/api/v1/lotes",
        "/api/v1/recepciones-uva",
    ],
)
def test_get_publicos_responden_sin_token(client: TestClient, bodega, path: str) -> None:
    response = client.get(path)

    assert response.status_code == 200


@pytest.mark.parametrize(("method", "path"), PROTECTED_WRITE_ENDPOINTS)
def test_post_patch_protegidos_sin_token_devuelven_401(
    client: TestClient,
    method: str,
    path: str,
) -> None:
    response = getattr(client, method)(path, json={})

    assert response.status_code == 401


@pytest.mark.parametrize(("method", "path"), PROTECTED_WRITE_ENDPOINTS)
def test_post_patch_protegidos_con_operario_devuelven_403(
    client: TestClient,
    auth_headers_operario: dict[str, str],
    method: str,
    path: str,
) -> None:
    response = getattr(client, method)(path, json={}, headers=auth_headers_operario)

    assert response.status_code == 403


@pytest.mark.parametrize(("method", "path"), PROTECTED_WRITE_ENDPOINTS)
@pytest.mark.parametrize("headers_fixture", ["auth_headers_admin", "auth_headers_enologo"])
def test_post_patch_protegidos_con_roles_autorizados_superan_autorizacion(
    client: TestClient,
    request: pytest.FixtureRequest,
    headers_fixture: str,
    method: str,
    path: str,
) -> None:
    headers = request.getfixturevalue(headers_fixture)
    response = getattr(client, method)(path, json={}, headers=headers)

    assert response.status_code == 422
