from __future__ import annotations

import os
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.engine import make_url


ENV_PATH = Path(".env")

BODEGA_NOMBRE = "Bodega y Viñedos Lanzarini"
DEPOSITO_NOMBRE = "Depósito Principal"
ROL_IMPORTACION = "Administrador"
USUARIO_IMPORTACION_NOMBRE = "Usuario Técnico Importación"
USUARIO_IMPORTACION_EMAIL = "importacion@lanzarini.local"
ESTADO_PILETA_DEFAULT = "Activa"
DEFAULT_CAPACIDAD_LITROS = Decimal(os.getenv("IMPORT_DEFAULT_CAPACIDAD_LITROS", "1"))


@dataclass
class ImportStats:
    found: int = 0
    created: int = 0

    @property
    def total_seen(self) -> int:
        return self.found + self.created


def load_dotenv_if_needed() -> None:
    if not ENV_PATH.exists():
        return

    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def add_default_connect_timeout(database_url: str) -> str:
    url = make_url(database_url)
    query = dict(url.query)
    query.setdefault("connect_timeout", "10")
    return url.set(query=query).render_as_string(hide_password=False)


def get_database_url() -> str:
    load_dotenv_if_needed()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL no está definido.")
    return add_default_connect_timeout(database_url)


def normalize_text(value: Any) -> str | None:
    if value is None:
        return None

    text_value = str(value).strip()
    if not text_value or text_value.lower() in {"nan", "none", "null"}:
        return None

    if text_value.endswith(".0"):
        text_value = text_value[:-2]

    return text_value


def normalize_pileta_number(value: Any) -> str | None:
    if value is None:
        return None

    try:
        number = Decimal(str(value))
    except InvalidOperation:
        return normalize_text(value)

    if number == number.to_integral_value():
        return str(int(number))

    return str(number.normalize())


def pileta_codigo(value: Any) -> str | None:
    number = normalize_pileta_number(value)
    if number is None:
        return None

    if number.isdigit():
        return f"P-{int(number):03d}"

    return f"P-{number.replace('.', '-')}"


def decimal_or_none(value: Any) -> Decimal | None:
    if value is None:
        return None

    try:
        decimal_value = Decimal(str(value))
    except InvalidOperation:
        return None

    if decimal_value <= 0:
        return None

    return decimal_value


def get_or_create_by_nombre(
    connection: Connection,
    *,
    table_name: str,
    nombre: str,
    active_column: str,
    extra_values: dict[str, Any] | None = None,
) -> tuple[int, bool]:
    row = connection.execute(
        text(f"SELECT id FROM {table_name} WHERE nombre = :nombre"),
        {"nombre": nombre},
    ).first()
    if row:
        return int(row.id), False

    values = {"nombre": nombre, active_column: True}
    if extra_values:
        values.update(extra_values)

    columns = ", ".join(values.keys())
    placeholders = ", ".join(f":{key}" for key in values)
    inserted = connection.execute(
        text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING id"),
        values,
    ).first()
    return int(inserted.id), True


def ensure_bodega(connection: Connection) -> tuple[int, bool]:
    return get_or_create_by_nombre(
        connection,
        table_name="bodegas",
        nombre=BODEGA_NOMBRE,
        active_column="activa",
    )


def ensure_deposito(connection: Connection, bodega_id: int) -> tuple[int, bool]:
    row = connection.execute(
        text(
            """
            SELECT id
            FROM depositos
            WHERE bodega_id = :bodega_id AND nombre = :nombre
            """
        ),
        {"bodega_id": bodega_id, "nombre": DEPOSITO_NOMBRE},
    ).first()
    if row:
        return int(row.id), False

    inserted = connection.execute(
        text(
            """
            INSERT INTO depositos (bodega_id, nombre, tipo, descripcion, activo)
            VALUES (:bodega_id, :nombre, :tipo, :descripcion, true)
            RETURNING id
            """
        ),
        {
            "bodega_id": bodega_id,
            "nombre": DEPOSITO_NOMBRE,
            "tipo": "Bodega",
            "descripcion": "Depósito default creado desde importación staging.",
        },
    ).first()
    return int(inserted.id), True


def ensure_usuario_importacion(connection: Connection, bodega_id: int) -> tuple[int, bool]:
    rol_id, _ = get_or_create_by_nombre(
        connection,
        table_name="roles",
        nombre=ROL_IMPORTACION,
        active_column="activo",
        extra_values={"descripcion": "Rol técnico utilizado para importaciones controladas."},
    )

    row = connection.execute(
        text("SELECT id FROM usuarios WHERE email = :email"),
        {"email": USUARIO_IMPORTACION_EMAIL},
    ).first()
    if row:
        return int(row.id), False

    inserted = connection.execute(
        text(
            """
            INSERT INTO usuarios (bodega_id, rol_id, nombre, email, activo)
            VALUES (:bodega_id, :rol_id, :nombre, :email, true)
            RETURNING id
            """
        ),
        {
            "bodega_id": bodega_id,
            "rol_id": rol_id,
            "nombre": USUARIO_IMPORTACION_NOMBRE,
            "email": USUARIO_IMPORTACION_EMAIL,
        },
    ).first()
    return int(inserted.id), True


def fetch_unique_values(connection: Connection, sql: str) -> list[str]:
    rows = connection.execute(text(sql)).scalars().all()
    values = {normalized for value in rows if (normalized := normalize_text(value))}
    return sorted(values)


def ensure_calificaciones(connection: Connection) -> ImportStats:
    values = fetch_unique_values(
        connection,
        """
        SELECT califiacion_vino::text FROM staging.piletas_lotes
        UNION
        SELECT calificacion_origen::text FROM staging.movimiento
        UNION
        SELECT calificacion_destino::text FROM staging.movimiento
        UNION
        SELECT calificacion_destino_final::text FROM staging.movimiento
        """,
    )

    stats = ImportStats()
    for value in values:
        _, created = get_or_create_by_nombre(
            connection,
            table_name="calificaciones_vino",
            nombre=value,
            active_column="activa",
        )
        if created:
            stats.created += 1
        else:
            stats.found += 1

    return stats


def ensure_estados_lote(connection: Connection) -> ImportStats:
    values = fetch_unique_values(
        connection,
        """
        SELECT estado::text
        FROM staging.piletas_lotes
        """,
    )

    stats = ImportStats()
    for value in values:
        _, created = get_or_create_by_nombre(
            connection,
            table_name="estados_lote",
            nombre=value,
            active_column="activo",
        )
        if created:
            stats.created += 1
        else:
            stats.found += 1

    return stats


def fetch_piletas(connection: Connection) -> list[dict[str, Any]]:
    rows = connection.execute(
        text(
            """
            WITH numeros AS (
                SELECT pileta_nro AS numero FROM staging.piletas_lotes WHERE pileta_nro IS NOT NULL
                UNION
                SELECT pileta_origen AS numero FROM staging.movimiento WHERE pileta_origen IS NOT NULL
                UNION
                SELECT pileta_destino AS numero FROM staging.movimiento WHERE pileta_destino IS NOT NULL
            ),
            capacidades AS (
                SELECT pileta_nro AS numero, MAX(capacidad) AS capacidad
                FROM staging.piletas_lotes
                WHERE pileta_nro IS NOT NULL AND capacidad IS NOT NULL AND capacidad > 0
                GROUP BY pileta_nro
            )
            SELECT numeros.numero, capacidades.capacidad
            FROM numeros
            LEFT JOIN capacidades ON capacidades.numero = numeros.numero
            ORDER BY numeros.numero
            """
        )
    ).all()
    return [dict(row._mapping) for row in rows]


def ensure_piletas(
    connection: Connection,
    *,
    bodega_id: int,
    deposito_id: int,
    estado_pileta_id: int,
) -> ImportStats:
    stats = ImportStats()
    for row in fetch_piletas(connection):
        codigo = pileta_codigo(row["numero"])
        numero = normalize_pileta_number(row["numero"])
        if not codigo or not numero:
            continue

        existing = connection.execute(
            text(
                """
                SELECT id
                FROM piletas
                WHERE bodega_id = :bodega_id AND codigo = :codigo
                """
            ),
            {"bodega_id": bodega_id, "codigo": codigo},
        ).first()
        if existing:
            stats.found += 1
            continue

        capacidad = decimal_or_none(row["capacidad"])
        observaciones = "Pileta creada desde staging."
        if capacidad is None:
            capacidad = DEFAULT_CAPACIDAD_LITROS
            observaciones = (
                "Pileta creada desde staging sin capacidad informada; "
                f"se asigna capacidad técnica default {DEFAULT_CAPACIDAD_LITROS}."
            )

        connection.execute(
            text(
                """
                INSERT INTO piletas (
                    bodega_id,
                    deposito_id,
                    estado_pileta_id,
                    codigo,
                    nombre,
                    capacidad_litros,
                    observaciones,
                    activa
                )
                VALUES (
                    :bodega_id,
                    :deposito_id,
                    :estado_pileta_id,
                    :codigo,
                    :nombre,
                    :capacidad_litros,
                    :observaciones,
                    true
                )
                """
            ),
            {
                "bodega_id": bodega_id,
                "deposito_id": deposito_id,
                "estado_pileta_id": estado_pileta_id,
                "codigo": codigo,
                "nombre": f"Pileta {numero}",
                "capacidad_litros": capacidad,
                "observaciones": observaciones,
            },
        )
        stats.created += 1

    return stats


def final_count(connection: Connection, table_name: str) -> int:
    return int(connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one())


def run_import(engine: Engine) -> dict[str, Any]:
    with engine.begin() as connection:
        bodega_id, bodega_created = ensure_bodega(connection)
        deposito_id, deposito_created = ensure_deposito(connection, bodega_id)
        usuario_id, usuario_created = ensure_usuario_importacion(connection, bodega_id)
        estado_pileta_id, estado_pileta_created = get_or_create_by_nombre(
            connection,
            table_name="estados_pileta",
            nombre=ESTADO_PILETA_DEFAULT,
            active_column="activo",
            extra_values={"descripcion": "Estado default para piletas importadas desde staging."},
        )

        calificaciones = ensure_calificaciones(connection)
        estados_lote = ensure_estados_lote(connection)
        piletas = ensure_piletas(
            connection,
            bodega_id=bodega_id,
            deposito_id=deposito_id,
            estado_pileta_id=estado_pileta_id,
        )

        return {
            "bodega": {"id": bodega_id, "created": bodega_created},
            "deposito": {"id": deposito_id, "created": deposito_created},
            "usuario_importacion": {"id": usuario_id, "created": usuario_created},
            "estado_pileta_default": {"id": estado_pileta_id, "created": estado_pileta_created},
            "calificaciones_vino": calificaciones,
            "estados_lote": estados_lote,
            "piletas": piletas,
            "final_counts": {
                "bodegas": final_count(connection, "bodegas"),
                "depositos": final_count(connection, "depositos"),
                "usuarios": final_count(connection, "usuarios"),
                "calificaciones_vino": final_count(connection, "calificaciones_vino"),
                "estados_lote": final_count(connection, "estados_lote"),
                "estados_pileta": final_count(connection, "estados_pileta"),
                "piletas": final_count(connection, "piletas"),
            },
        }


def print_stats(result: dict[str, Any]) -> None:
    print("IMPORTACION STAGING: CATALOGOS Y PILETAS")
    print("=" * 80)
    print(f"Bodega default: id={result['bodega']['id']} creada={result['bodega']['created']}")
    print(
        "Depósito default: "
        f"id={result['deposito']['id']} creado={result['deposito']['created']}"
    )
    print(
        "Usuario técnico: "
        f"id={result['usuario_importacion']['id']} creado={result['usuario_importacion']['created']}"
    )
    print(
        "Estado pileta default: "
        f"id={result['estado_pileta_default']['id']} "
        f"creado={result['estado_pileta_default']['created']}"
    )

    for label in ["calificaciones_vino", "estados_lote", "piletas"]:
        stats: ImportStats = result[label]
        print(
            f"{label}: creados={stats.created}, encontrados={stats.found}, "
            f"procesados={stats.total_seen}"
        )

    print("\nConteos finales:")
    for table_name, count in result["final_counts"].items():
        print(f"- {table_name}: {count}")


def main() -> int:
    try:
        engine = create_engine(get_database_url())
        result = run_import(engine)
        print_stats(result)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
