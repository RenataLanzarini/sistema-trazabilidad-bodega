import ast
import importlib
from pathlib import Path

from pydantic import BaseModel


SERVICE_DIR = Path("app/services")
SCHEMA_DIR = Path("app/schemas")


def _parse_python_file(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_services_siguen_manejando_transacciones_en_operaciones_de_escritura() -> None:
    services_with_writes = {
        "recepcion_uva_service.py",
        "lote_service.py",
        "pileta_service.py",
        "operacion_productiva_service.py",
        "movimiento_fisico_service.py",
        "merma_service.py",
        "fraccionamiento_service.py",
        "producto_terminado_service.py",
        "venta_granel_service.py",
        "analisis_enologico_service.py",
        "medicion_fermentacion_service.py",
        "orden_trabajo_service.py",
        "corte_teorico_service.py",
        "usuario_service.py",
    }
    violations: list[str] = []

    for path in SERVICE_DIR.glob("*.py"):
        if path.name not in services_with_writes:
            continue
        tree = _parse_python_file(path)
        calls = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        if "commit" not in calls or "rollback" not in calls:
            violations.append(path.name)

    assert violations == []


def test_stock_service_es_el_unico_que_calcula_stock() -> None:
    forbidden_calculation_methods = {
        "calcular_stock_actual_por_pileta",
        "calcular_stock_actual_por_lote",
        "calcular_stock_por_lote_y_pileta",
        "calcular_stock_historico_hasta",
    }
    violations: list[str] = []

    for path in SERVICE_DIR.glob("*.py"):
        if path.name == "stock_service.py":
            continue
        tree = _parse_python_file(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name in forbidden_calculation_methods:
                violations.append(f"{path}:{node.lineno}:{node.name}")

    assert violations == []


def test_no_hay_imports_circulares_evidentes_en_modulos_principales() -> None:
    modules = [
        "app.main",
        "app.api.routes.v1.router",
        "app.services.stock_service",
        "app.services.trazabilidad_service",
        "app.services.movimiento_fisico_service",
        "app.services.merma_service",
        "app.services.fraccionamiento_service",
        "app.services.venta_granel_service",
    ]

    for module in modules:
        importlib.import_module(module)


def test_schemas_create_no_exponen_campos_internos() -> None:
    forbidden_fields = {"id", "created_at", "updated_at", "password_hash"}
    violations: list[str] = []

    for path in SCHEMA_DIR.glob("*.py"):
        module = importlib.import_module(f"app.schemas.{path.stem}")
        for name, obj in vars(module).items():
            if (
                isinstance(obj, type)
                and issubclass(obj, BaseModel)
                and name.endswith("Create")
            ):
                exposed = forbidden_fields.intersection(obj.model_fields)
                if exposed:
                    violations.append(f"{name}:{sorted(exposed)}")

    assert violations == []


def test_schemas_read_no_exponen_password_hash() -> None:
    violations: list[str] = []

    for path in SCHEMA_DIR.glob("*.py"):
        module = importlib.import_module(f"app.schemas.{path.stem}")
        for name, obj in vars(module).items():
            if (
                isinstance(obj, type)
                and issubclass(obj, BaseModel)
                and name.endswith("Read")
                and "password_hash" in obj.model_fields
            ):
                violations.append(name)

    assert violations == []
