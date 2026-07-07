from pathlib import Path


def test_repositories_siguen_sin_commit_ni_rollback() -> None:
    for path in Path("app/repositories").glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert ".commit(" not in source, path
        assert ".rollback(" not in source, path


def test_movimiento_fisico_service_maneja_transacciones() -> None:
    source = Path("app/services/movimiento_fisico_service.py").read_text(encoding="utf-8")

    assert "self.session.commit()" in source
    assert "self.session.rollback()" in source


def test_stock_service_concentra_calculo_de_stock() -> None:
    stock_source = Path("app/services/stock_service.py").read_text(encoding="utf-8")
    assert "def calcular_stock_actual_por_pileta" in stock_source
    assert "def validar_stock_disponible" in stock_source

    for path in Path("app/services").glob("*.py"):
        if path.name == "stock_service.py":
            continue
        source = path.read_text(encoding="utf-8")
        assert "def calcular_stock" not in source, path
        assert "def validar_stock_disponible" not in source, path
