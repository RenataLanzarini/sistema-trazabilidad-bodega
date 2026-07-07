import pytest


@pytest.fixture(autouse=True)
def disable_postgresql_advisory_locks(monkeypatch):
    """SQLite de test no soporta pg_advisory_xact_lock; el bloqueo se cubre en PostgreSQL."""

    monkeypatch.setattr(
        "app.services.stock_service.StockService.bloquear_stock_operacion",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "app.services.stock_service.StockService.bloquear_consumos",
        lambda *args, **kwargs: None,
    )
