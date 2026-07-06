from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.repositories.operacion_productiva_repository import OperacionProductivaRepository
from app.schemas.operacion_productiva import (
    OperacionProductivaAnular,
    OperacionProductivaCreate,
    OperacionProductivaRead,
)
from app.services.operacion_productiva_service import OperacionProductivaService


router = APIRouter(prefix="/operaciones-productivas", tags=["operaciones-productivas"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[OperacionProductivaRead])
def listar_operaciones_productivas(db: DbSession) -> list[object]:
    return OperacionProductivaRepository(db).list()


@router.get("/bodega/{bodega_id}", response_model=list[OperacionProductivaRead])
def listar_operaciones_por_bodega(bodega_id: int, db: DbSession) -> list[object]:
    return OperacionProductivaService(db).listar_por_bodega(bodega_id)


@router.get("/tipo/{tipo_operacion_id}", response_model=list[OperacionProductivaRead])
def listar_operaciones_por_tipo(tipo_operacion_id: int, db: DbSession) -> list[object]:
    return OperacionProductivaService(db).listar_por_tipo(tipo_operacion_id)


@router.get("/responsable/{responsable_id}", response_model=list[OperacionProductivaRead])
def listar_operaciones_por_responsable(responsable_id: int, db: DbSession) -> list[object]:
    return OperacionProductivaService(db).listar_por_responsable(responsable_id)


@router.get("/anuladas", response_model=list[OperacionProductivaRead])
def listar_operaciones_anuladas(db: DbSession) -> list[object]:
    return OperacionProductivaService(db).listar_anuladas()


@router.get("/{operacion_id}", response_model=OperacionProductivaRead)
def obtener_operacion_productiva(operacion_id: int, db: DbSession) -> object:
    return OperacionProductivaService(db).obtener_por_id(operacion_id)


@router.post("", response_model=OperacionProductivaRead, status_code=201)
def crear_operacion_productiva(
    data: OperacionProductivaCreate,
    db: DbSession,
) -> object:
    return OperacionProductivaService(db).crear_operacion(**data.model_dump())


@router.patch("/{operacion_id}/anular", response_model=OperacionProductivaRead)
def anular_operacion_productiva(
    operacion_id: int,
    data: OperacionProductivaAnular,
    db: DbSession,
) -> object:
    return OperacionProductivaService(db).anular_operacion(
        operacion_id,
        motivo_anulacion=data.motivo_anulacion,
    )
