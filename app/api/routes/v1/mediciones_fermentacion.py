from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.security import require_roles
from app.schemas.medicion_fermentacion import (
    MedicionFermentacionCreate,
    MedicionFermentacionRead,
)
from app.services.medicion_fermentacion_service import MedicionFermentacionService


router = APIRouter(prefix="/mediciones-fermentacion", tags=["mediciones-fermentacion"])
DbSession = Annotated[Session, Depends(get_db)]
WRITE_ACCESS = Depends(require_roles("Administrador", "Administrador/Dueño", "Enólogo"))


@router.post(
    "",
    response_model=MedicionFermentacionRead,
    status_code=201,
    dependencies=[WRITE_ACCESS],
)
def crear_medicion_fermentacion(data: MedicionFermentacionCreate, db: DbSession) -> object:
    return MedicionFermentacionService(db).crear_medicion(data)


@router.get("", response_model=list[MedicionFermentacionRead])
def listar_mediciones_fermentacion(db: DbSession) -> list[object]:
    return MedicionFermentacionService(db).listar()


@router.get("/lote/{lote_id}", response_model=list[MedicionFermentacionRead])
def listar_mediciones_por_lote(lote_id: int, db: DbSession) -> list[object]:
    return MedicionFermentacionService(db).listar_por_lote(lote_id)


@router.get("/pileta/{pileta_id}", response_model=list[MedicionFermentacionRead])
def listar_mediciones_por_pileta(pileta_id: int, db: DbSession) -> list[object]:
    return MedicionFermentacionService(db).listar_por_pileta(pileta_id)


@router.get("/fecha/{fecha}", response_model=list[MedicionFermentacionRead])
def listar_mediciones_por_fecha(fecha: date, db: DbSession) -> list[object]:
    return MedicionFermentacionService(db).listar_por_fecha(fecha)


@router.get("/ultimo/lote/{lote_id}", response_model=MedicionFermentacionRead)
def obtener_ultima_medicion_por_lote(lote_id: int, db: DbSession) -> object:
    return MedicionFermentacionService(db).obtener_ultima_por_lote(lote_id)


@router.get("/ultimo/pileta/{pileta_id}", response_model=MedicionFermentacionRead)
def obtener_ultima_medicion_por_pileta(pileta_id: int, db: DbSession) -> object:
    return MedicionFermentacionService(db).obtener_ultima_por_pileta(pileta_id)


@router.get("/{medicion_id}", response_model=MedicionFermentacionRead)
def obtener_medicion_fermentacion(medicion_id: int, db: DbSession) -> object:
    return MedicionFermentacionService(db).obtener_por_id(medicion_id)
