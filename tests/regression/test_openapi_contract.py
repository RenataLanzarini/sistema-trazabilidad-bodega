from fastapi.testclient import TestClient


EXPECTED_MAIN_PATHS = {
    "/health",
    "/api/v1/health",
    "/api/v1/auth/login",
    "/api/v1/auth/me",
    "/api/v1/bodegas",
    "/api/v1/depositos",
    "/api/v1/usuarios",
    "/api/v1/variedades",
    "/api/v1/recepciones-uva",
    "/api/v1/lotes",
    "/api/v1/piletas",
    "/api/v1/stock/piletas/{pileta_id}",
    "/api/v1/stock/lotes/{lote_id}",
    "/api/v1/trazabilidad/lotes/{lote_id}/grafo",
    "/api/v1/operaciones-productivas",
    "/api/v1/movimientos-fisicos",
    "/api/v1/mermas",
    "/api/v1/fraccionamientos",
    "/api/v1/productos-terminados",
    "/api/v1/ventas-granel",
    "/api/v1/analisis-enologicos",
    "/api/v1/mediciones-fermentacion",
    "/api/v1/ordenes-trabajo",
    "/api/v1/cortes-teoricos",
}


def test_openapi_genera_correctamente(client: TestClient) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["openapi"].startswith("3.")


def test_openapi_no_tiene_operation_id_duplicados(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    operation_ids = [
        operation["operationId"]
        for methods in schema["paths"].values()
        for operation in methods.values()
        if "operationId" in operation
    ]

    assert len(operation_ids) == len(set(operation_ids))


def test_openapi_registra_todas_las_rutas_principales(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()

    assert EXPECTED_MAIN_PATHS.issubset(set(schema["paths"]))


def test_no_hay_rutas_duplicadas_en_fastapi(client: TestClient) -> None:
    seen: set[tuple[str, str]] = set()
    duplicates: list[tuple[str, str]] = []

    for route in client.app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None) or set()
        for method in methods:
            if method in {"HEAD", "OPTIONS"}:
                continue
            key = (method, path)
            if key in seen:
                duplicates.append(key)
            seen.add(key)

    assert duplicates == []
