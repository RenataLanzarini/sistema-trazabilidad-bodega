# Sistema de Trazabilidad Bodega

Sistema profesional de trazabilidad y gestion de produccion para bodegas.

El proyecto usa FastAPI, SQLAlchemy 2.x, PostgreSQL, Alembic y Pydantic v2 con arquitectura por capas:

```text
API -> Services -> Repositories -> PostgreSQL
```

## Estado actual

Infraestructura base del proyecto. Todavia no incluye endpoints funcionales, modelos definitivos del DER, services ni repositories.

## Requisitos

- Python 3.12+
- Docker y Docker Compose
- PostgreSQL 16 si se ejecuta fuera de Docker

## Configuracion inicial

1. Copiar variables de entorno:

```bash
cp .env.example .env
```

2. Levantar servicios:

```bash
docker compose up --build
```

3. API local:

```text
http://localhost:8000
```

4. Documentacion OpenAPI:

```text
http://localhost:8000/docs
```

## Alembic

Alembic queda configurado para futuras migraciones. En esta fase no se crean migraciones de entidades.

## Testing

La estructura inicial de pruebas queda organizada en:

```text
tests/
├── api/
├── integration/
└── unit/
```

## Convenciones principales

- No hay borrado fisico para datos criticos.
- El stock se calcula desde movimientos fisicos.
- La genealogia se calcula desde relaciones genealogicas entre lotes.
- Los endpoints no contienen logica de negocio.
- Services concentran reglas de negocio.
- Repositories concentran acceso a datos.
