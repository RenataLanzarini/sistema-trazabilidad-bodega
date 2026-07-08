"""Inspecciona el Excel funcional de la bodega sin modificar la base de datos.

Uso:
    python scripts/inspeccionar_excel.py
    python scripts/inspeccionar_excel.py data/imports/otro_archivo.xlsx
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    import pandas as pd
except ModuleNotFoundError as exc:
    print(
        "ERROR: falta instalar pandas. Instalar tambien openpyxl para leer archivos .xlsx.",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


DEFAULT_EXCEL_PATH = Path("data/imports/datos_bodega_lanzarini.xlsx")

ENTITY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "lotes": (
        "lote",
        "partida",
        "codigo_lote",
        "cod_lote",
        "cosecha",
        "variedad",
        "color",
        "vino",
    ),
    "piletas": (
        "pileta",
        "piletas",
        "tanque",
        "vasija",
        "deposito",
        "capacidad",
        "litros_por_cm",
    ),
    "movimientos_fisicos": (
        "movimiento",
        "trasiego",
        "trasegado",
        "origen",
        "destino",
        "litros",
        "volumen",
        "litros_movidos",
        "pileta_origen",
        "pileta_destino",
    ),
    "operaciones_productivas": (
        "operacion",
        "tipo_operacion",
        "proceso",
        "fecha",
        "date",
        "date_time",
        "datetime",
        "responsable",
        "estado",
        "anulada",
        "orden",
    ),
    "bodegas": (
        "bodega",
        "establecimiento",
        "razon_social",
        "cuit",
        "ubicacion",
        "deposito",
    ),
}


def normalize_text(value: object) -> str:
    """Normaliza textos de columnas para comparaciones simples."""

    text = str(value).strip().lower()
    text = (
        text.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
    )
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def format_columns(columns: Iterable[object]) -> str:
    return "\n".join(f"    - {column}" for column in columns)


def detect_entity_matches(sheet_name: str, columns: Iterable[object]) -> dict[str, list[str]]:
    normalized_sheet = normalize_text(sheet_name)
    normalized_columns = {str(column): normalize_text(column) for column in columns}
    matches: dict[str, list[str]] = {}

    for entity, keywords in ENTITY_KEYWORDS.items():
        entity_matches: list[str] = []

        if any(keyword in normalized_sheet for keyword in keywords):
            entity_matches.append(f"[hoja] {sheet_name}")

        for original_column, normalized_column in normalized_columns.items():
            if any(keyword in normalized_column for keyword in keywords):
                entity_matches.append(original_column)

        if entity_matches:
            matches[entity] = sorted(set(entity_matches))

    return matches


def print_sheet_summary(sheet_name: str, dataframe: pd.DataFrame) -> dict[str, list[str]]:
    rows, columns = dataframe.shape

    print("\n" + "=" * 100)
    print(f"HOJA: {sheet_name}")
    print("=" * 100)
    print(f"Filas: {rows}")
    print(f"Columnas: {columns}")

    print("\nColumnas:")
    if columns:
        print(format_columns(dataframe.columns))
    else:
        print("    (sin columnas)")

    print("\nTipos de datos:")
    if columns:
        for column, dtype in dataframe.dtypes.items():
            print(f"    - {column}: {dtype}")
    else:
        print("    (sin tipos)")

    print("\nPrimeras 5 filas:")
    if dataframe.empty:
        print("    (hoja vacia)")
    else:
        print(dataframe.head(5).to_string(index=False))

    matches = detect_entity_matches(sheet_name, dataframe.columns)
    print("\nPosibles mapeos detectados:")
    if matches:
        for entity, matched_columns in matches.items():
            print(f"    - {entity}:")
            for matched_column in matched_columns:
                print(f"        * {matched_column}")
    else:
        print("    (sin coincidencias heuristicas)")

    return matches


def inspect_excel(excel_path: Path) -> None:
    if not excel_path.exists():
        raise FileNotFoundError(f"No existe el archivo Excel: {excel_path}")

    print("=" * 100)
    print("INSPECCION DE EXCEL")
    print("=" * 100)
    print(f"Archivo: {excel_path}")
    print("Modo: solo lectura. No modifica base de datos, modelos ni migraciones.")

    workbook = pd.ExcelFile(excel_path)
    print(f"\nCantidad de hojas: {len(workbook.sheet_names)}")
    print("Hojas:")
    for sheet_name in workbook.sheet_names:
        print(f"    - {sheet_name}")

    global_matches: dict[str, dict[str, list[str]]] = {
        entity: {} for entity in ENTITY_KEYWORDS
    }

    for sheet_name in workbook.sheet_names:
        dataframe = pd.read_excel(workbook, sheet_name=sheet_name)
        sheet_matches = print_sheet_summary(sheet_name, dataframe)
        for entity, matched_columns in sheet_matches.items():
            global_matches[entity][sheet_name] = matched_columns

    print("\n" + "=" * 100)
    print("RESUMEN DE POSIBLES MAPEOS AL MODELO")
    print("=" * 100)
    for entity in ENTITY_KEYWORDS:
        print(f"\n{entity}:")
        entity_matches = global_matches[entity]
        if not entity_matches:
            print("    No se detectaron columnas candidatas.")
            continue
        for sheet_name, matched_columns in entity_matches.items():
            print(f"    Hoja: {sheet_name}")
            for matched_column in matched_columns:
                print(f"        - {matched_column}")

    print("\nInspeccion finalizada.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspecciona hojas, columnas, tipos y primeras filas de un Excel.",
    )
    parser.add_argument(
        "excel_path",
        nargs="?",
        default=str(DEFAULT_EXCEL_PATH),
        help=f"Ruta del Excel a inspeccionar. Por defecto: {DEFAULT_EXCEL_PATH}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    excel_path = Path(args.excel_path)

    try:
        inspect_excel(excel_path)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
