from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.security import require_roles
from app.schemas.corte_teorico import (
    CorteTeoricoCreate,
    CorteTeoricoDetalleCreate,
    CorteTeoricoDetalleRead,
    CorteTeoricoRead,
    CorteTeoricoVincularOperacion,
)
from app.services.corte_teorico_service import CorteTeoricoService


router = APIRouter(prefix="/cortes-teoricos", tags=["cortes-teoricos"])
DbSession = Annotated[Session, Depends(get_db)]
WRITE_ACCESS = Depends(require_roles("Administrador", "Administrador/Dueño", "Enólogo"))


@router.post("", response_model=CorteTeoricoRead, status_code=201, dependencies=[WRITE_ACCESS])
def crear_corte_teorico(data: CorteTeoricoCreate, db: DbSession) -> object:
    payload = data.model_dump()
    payload["detalles"] = [detalle.model_dump() for detalle in data.detalles]
    return CorteTeoricoService(db).crear_corte_teorico(**payload)


@router.post(
    "/{corte_teorico_id}/detalles",
    response_model=CorteTeoricoDetalleRead,
    status_code=201,
    dependencies=[WRITE_ACCESS],
)
def crear_detalle_corte_teorico(
    corte_teorico_id: int,
    data: CorteTeoricoDetalleCreate,
    db: DbSession,
) -> object:
    return CorteTeoricoService(db).crear_detalle_corte(
        corte_teorico_id,
        **data.model_dump(),
    )


@router.get("", response_model=list[CorteTeoricoRead])
def listar_cortes_teoricos(db: DbSession) -> list[object]:
    return CorteTeoricoService(db).listar()


@router.get("/fecha/{fecha}", response_model=list[CorteTeoricoRead])
def listar_cortes_teoricos_por_fecha(fecha: date, db: DbSession) -> list[object]:
    return CorteTeoricoService(db).listar_por_fecha(fecha, fecha)


@router.get("/responsable/{responsable_id}", response_model=list[CorteTeoricoRead])
def listar_cortes_teoricos_por_responsable(
    responsable_id: int,
    db: DbSession,
) -> list[object]:
    return CorteTeoricoService(db).listar_por_responsable(responsable_id)


@router.get("/{corte_teorico_id}/detalles", response_model=list[CorteTeoricoDetalleRead])
def listar_detalles_corte_teorico(
    corte_teorico_id: int,
    db: DbSession,
) -> list[object]:
    return CorteTeoricoService(db).obtener_detalles_por_corte(corte_teorico_id)


@router.get("/{corte_teorico_id}", response_model=CorteTeoricoRead)
def obtener_corte_teorico(corte_teorico_id: int, db: DbSession) -> object:
    return CorteTeoricoService(db).obtener_por_id(corte_teorico_id)


@router.patch(
    "/{corte_teorico_id}/vincular-operacion",
    response_model=CorteTeoricoRead,
    dependencies=[WRITE_ACCESS],
)
def vincular_operacion_productiva(
    corte_teorico_id: int,
    data: CorteTeoricoVincularOperacion,
    db: DbSession,
) -> object:
    return CorteTeoricoService(db).vincular_operacion_productiva(
        corte_teorico_id,
        data.operacion_productiva_id,
    )
