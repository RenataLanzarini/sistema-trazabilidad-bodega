from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.security import require_roles
from app.schemas.analisis_enologico import AnalisisEnologicoCreate, AnalisisEnologicoRead
from app.services.analisis_enologico_service import AnalisisEnologicoService


router = APIRouter(prefix="/analisis-enologicos", tags=["analisis-enologicos"])
DbSession = Annotated[Session, Depends(get_db)]
WRITE_ACCESS = Depends(require_roles("Administrador", "Administrador/Dueño", "Enólogo"))


@router.post("", response_model=AnalisisEnologicoRead, status_code=201, dependencies=[WRITE_ACCESS])
def crear_analisis_enologico(data: AnalisisEnologicoCreate, db: DbSession) -> object:
    return AnalisisEnologicoService(db).crear_analisis(data)


@router.get("", response_model=list[AnalisisEnologicoRead])
def listar_analisis_enologicos(db: DbSession) -> list[object]:
    return AnalisisEnologicoService(db).listar()


@router.get("/lote/{lote_id}", response_model=list[AnalisisEnologicoRead])
def listar_analisis_por_lote(lote_id: int, db: DbSession) -> list[object]:
    return AnalisisEnologicoService(db).listar_por_lote(lote_id)


@router.get("/pileta/{pileta_id}", response_model=list[AnalisisEnologicoRead])
def listar_analisis_por_pileta(pileta_id: int, db: DbSession) -> list[object]:
    return AnalisisEnologicoService(db).listar_por_pileta(pileta_id)


@router.get("/fecha/{fecha}", response_model=list[AnalisisEnologicoRead])
def listar_analisis_por_fecha(fecha: date, db: DbSession) -> list[object]:
    return AnalisisEnologicoService(db).listar_por_fecha(fecha)


@router.get("/ultimo/lote/{lote_id}", response_model=AnalisisEnologicoRead)
def obtener_ultimo_analisis_por_lote(lote_id: int, db: DbSession) -> object:
    return AnalisisEnologicoService(db).obtener_ultimo_por_lote(lote_id)


@router.get("/ultimo/pileta/{pileta_id}", response_model=AnalisisEnologicoRead)
def obtener_ultimo_analisis_por_pileta(pileta_id: int, db: DbSession) -> object:
    return AnalisisEnologicoService(db).obtener_ultimo_por_pileta(pileta_id)


@router.get("/{analisis_id}", response_model=AnalisisEnologicoRead)
def obtener_analisis_enologico(analisis_id: int, db: DbSession) -> object:
    return AnalisisEnologicoService(db).obtener_por_id(analisis_id)
