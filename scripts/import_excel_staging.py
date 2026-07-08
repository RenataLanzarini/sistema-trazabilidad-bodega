"""Importa el Excel real a tablas staging en PostgreSQL.

Este script solo trabaja sobre el schema `staging`.
No modifica modelos SQLAlchemy, migraciones, services, repositories ni tablas del dominio.

Uso:
    python scripts/import_excel_staging.py

Variables:
    DATABASE_URL=postgresql+psycopg://usuario:password@localhost:5432/base
"""

from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.engine import make_url


EXCEL_PATH = Path("data/imports/datos_bodega_lanzarini.xlsx")
ENV_PATH = Path(".env")
STAGING_SCHEMA = "staging"
SHEETS_TO_TABLES = {
    "PILETAS LOTES": "piletas_lotes",
    "MOVIMIENTO": "movimiento",
    "borrador": "borrador",
}


def load_dotenv_if_needed(env_path: Path = ENV_PATH) -> None:
    """Carga pares simples CLAVE=VALOR desde .env sin pisar variables existentes."""

    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_database_url() -> str:
    load_dotenv_if_needed()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("No se encontro DATABASE_URL en variables de entorno ni en .env.")
    return database_url


def normalize_identifier(value: object) -> str:
    """Convierte nombres de columnas a snake_case ASCII seguro para PostgreSQL."""

    text_value = "" if value is None else str(value)
    normalized = unicodedata.normalize("NFKD", text_value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower().strip()
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text)
    ascii_text = re.sub(r"_+", "_", ascii_text).strip("_")
    return ascii_text or "columna"


def normalize_columns(columns: list[object]) -> list[str]:
    normalized_columns: list[str] = []
    seen: dict[str, int] = {}

    for column in columns:
        normalized = normalize_identifier(column)
        count = seen.get(normalized, 0)
        seen[normalized] = count + 1
        if count:
            normalized = f"{normalized}_{count + 1}"
        normalized_columns.append(normalized)

    return normalized_columns


def read_sheet(sheet_name: str) -> pd.DataFrame:
    dataframe = pd.read_excel(EXCEL_PATH, sheet_name=sheet_name)
    dataframe.columns = normalize_columns(list(dataframe.columns))
    return dataframe


def create_staging_schema(engine: Engine) -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{STAGING_SCHEMA}"'))


def replace_table(engine: Engine, table_name: str, dataframe: pd.DataFrame) -> int:
    dataframe.to_sql(
        name=table_name,
        con=engine,
        schema=STAGING_SCHEMA,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )

    with engine.connect() as connection:
        loaded_rows = connection.execute(
            text(f'SELECT COUNT(*) FROM "{STAGING_SCHEMA}"."{table_name}"')
        ).scalar_one()

    return int(loaded_rows)


def print_table_summary(
    *,
    sheet_name: str,
    table_name: str,
    dataframe: pd.DataFrame,
    loaded_rows: int,
) -> None:
    print("\n" + "=" * 100)
    print(f"Hoja Excel: {sheet_name}")
    print(f"Tabla staging: {STAGING_SCHEMA}.{table_name}")
    print("=" * 100)
    print(f"Filas leidas: {len(dataframe)}")
    print(f"Filas cargadas: {loaded_rows}")
    print("Columnas normalizadas:")
    for column in dataframe.columns:
        print(f"    - {column}")


def import_excel_to_staging() -> list[dict[str, Any]]:
    if not EXCEL_PATH.exists():
        raise FileNotFoundError(f"No existe el archivo Excel: {EXCEL_PATH}")

    database_url = get_database_url()
    engine = create_engine(database_url)
    create_staging_schema(engine)

    results: list[dict[str, Any]] = []

    for sheet_name, table_name in SHEETS_TO_TABLES.items():
        dataframe = read_sheet(sheet_name)
        loaded_rows = replace_table(engine, table_name, dataframe)
        print_table_summary(
            sheet_name=sheet_name,
            table_name=table_name,
            dataframe=dataframe,
            loaded_rows=loaded_rows,
        )
        results.append(
            {
                "sheet_name": sheet_name,
                "table_name": f"{STAGING_SCHEMA}.{table_name}",
                "read_rows": len(dataframe),
                "loaded_rows": loaded_rows,
                "columns": list(dataframe.columns),
            }
        )

    engine.dispose()
    return results


def add_default_connect_timeout(database_url: str) -> str:
    """Evita esperas largas si PostgreSQL no esta disponible."""

    url = make_url(database_url)
    if "connect_timeout" in url.query:
        return database_url
    return str(url.update_query_dict({"connect_timeout": "10"}))


def main() -> int:
    print("=" * 100)
    print("IMPORTACION EXCEL A STAGING")
    print("=" * 100)
    print(f"Archivo: {EXCEL_PATH}")
    print("Destino: schema staging")
    print("Modo: reemplaza solo tablas staging. No modifica el modelo del dominio.")

    try:
        results = import_excel_to_staging()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("\n" + "=" * 100)
    print("RESUMEN FINAL")
    print("=" * 100)
    for result in results:
        print(
            f"{result['table_name']}: "
            f"{result['read_rows']} filas leidas / {result['loaded_rows']} filas cargadas"
        )

    print("\nImportacion finalizada correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
