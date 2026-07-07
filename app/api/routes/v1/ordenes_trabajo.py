from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.security import require_roles
from app.schemas.orden_trabajo import (
    OrdenTrabajoCompletar,
    OrdenTrabajoCreate,
    OrdenTrabajoRead,
    OrdenTrabajoVincularOperacion,
)
from app.services.orden_trabajo_service import OrdenTrabajoService


router = APIRouter(prefix="/ordenes-trabajo", tags=["ordenes-trabajo"])
DbSession = Annotated[Session, Depends(get_db)]
WRITE_ACCESS = Depends(require_roles("Administrador", "Administrador/Dueño", "Enólogo"))


@router.post("", response_model=OrdenTrabajoRead, status_code=201, dependencies=[WRITE_ACCESS])
def crear_orden_trabajo(data: OrdenTrabajoCreate, db: DbSession) -> object:
    return OrdenTrabajoService(db).crear_orden_trabajo(**data.model_dump())


@router.get("", response_model=list[OrdenTrabajoRead])
def listar_ordenes_trabajo(db: DbSession) -> list[object]:
    return OrdenTrabajoService(db).listar()


@router.get("/pendientes", response_model=list[OrdenTrabajoRead])
def listar_ordenes_pendientes(db: DbSession) -> list[object]:
    return OrdenTrabajoService(db).listar_pendientes()


@router.get("/completadas", response_model=list[OrdenTrabajoRead])
def listar_ordenes_completadas(db: DbSession) -> list[object]:
    return OrdenTrabajoService(db).listar_completadas()


@router.get("/operario/{operario_id}", response_model=list[OrdenTrabajoRead])
def listar_ordenes_por_operario(operario_id: int, db: DbSession) -> list[object]:
    return OrdenTrabajoService(db).listar_por_operario(operario_id)


@router.get("/pileta/{pileta_id}", response_model=list[OrdenTrabajoRead])
def listar_ordenes_por_pileta(pileta_id: int, db: DbSession) -> list[object]:
    return OrdenTrabajoService(db).listar_por_pileta(pileta_id)


@router.get("/lote/{lote_id}", response_model=list[OrdenTrabajoRead])
def listar_ordenes_por_lote(lote_id: int, db: DbSession) -> list[object]:
    return OrdenTrabajoService(db).listar_por_lote(lote_id)


@router.get("/{orden_trabajo_id}", response_model=OrdenTrabajoRead)
def obtener_orden_trabajo(orden_trabajo_id: int, db: DbSession) -> object:
    return OrdenTrabajoService(db).obtener_por_id(orden_trabajo_id)


@router.patch(
    "/{orden_trabajo_id}/completar",
    response_model=OrdenTrabajoRead,
    dependencies=[WRITE_ACCESS],
)
def completar_orden_trabajo(
    orden_trabajo_id: int,
    data: OrdenTrabajoCompletar,
    db: DbSession,
) -> object:
    return OrdenTrabajoService(db).marcar_completada(
        orden_trabajo_id,
        fecha_completada=data.fecha_completada,
        observaciones_completada=data.observaciones_completada,
    )


@router.patch(
    "/{orden_trabajo_id}/vincular-operacion",
    response_model=OrdenTrabajoRead,
    dependencies=[WRITE_ACCESS],
)
def vincular_operacion_productiva(
    orden_trabajo_id: int,
    data: OrdenTrabajoVincularOperacion,
    db: DbSession,
) -> object:
    return OrdenTrabajoService(db).vincular_operacion_productiva(
        orden_trabajo_id,
        data.operacion_productiva_id,
    )
