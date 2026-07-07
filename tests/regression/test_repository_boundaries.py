import ast
from pathlib import Path


REPOSITORY_DIR = Path("app/repositories")


def _parse_python_file(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _repository_files() -> list[Path]:
    return [
        path
        for path in REPOSITORY_DIR.glob("*.py")
        if path.name not in {"__init__.py"}
    ]


def test_repositories_no_hacen_commit_ni_rollback() -> None:
    forbidden_calls = {"commit", "rollback"}
    violations: list[str] = []

    for path in _repository_files():
        tree = _parse_python_file(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in forbidden_calls:
                    violations.append(f"{path}:{node.lineno}:{node.func.attr}")

    assert violations == []


def test_repositories_no_importan_excepciones_de_dominio_ni_services() -> None:
    forbidden_prefixes = ("app.core.exceptions", "app.services")
    violations: list[str] = []

    for path in _repository_files():
        tree = _parse_python_file(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module.startswith(forbidden_prefixes):
                    violations.append(f"{path}:{node.lineno}:{node.module}")

    assert violations == []


def test_repositories_no_contienen_validaciones_de_negocio_explicitas() -> None:
    forbidden_exception_names = {
        "BusinessRuleError",
        "NotFoundError",
        "ConflictError",
        "UnauthorizedError",
        "ForbiddenError",
    }
    violations: list[str] = []

    for path in _repository_files():
        tree = _parse_python_file(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Raise):
                violations.append(f"{path}:{node.lineno}:raise")
            if isinstance(node, ast.Name) and node.id in forbidden_exception_names:
                violations.append(f"{path}:{node.lineno}:{node.id}")

    assert violations == []
