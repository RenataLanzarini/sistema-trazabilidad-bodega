from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.schemas.trazabilidad import GrafoTrazabilidadRead, RelacionGenealogicaRead
from app.services.trazabilidad_service import TrazabilidadService


router = APIRouter(prefix="/trazabilidad", tags=["trazabilidad"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/lotes/{lote_id}/padres", response_model=list[RelacionGenealogicaRead])
def obtener_padres_lote(lote_id: int, db: DbSession) -> list[object]:
    return TrazabilidadService(db).obtener_padres(lote_id)


@router.get("/lotes/{lote_id}/hijos", response_model=list[RelacionGenealogicaRead])
def obtener_hijos_lote(lote_id: int, db: DbSession) -> list[object]:
    return TrazabilidadService(db).obtener_hijos(lote_id)


@router.get("/lotes/{lote_id}/hacia-atras", response_model=list[RelacionGenealogicaRead])
def recorrer_lote_hacia_atras(lote_id: int, db: DbSession) -> list[object]:
    return TrazabilidadService(db).recorrer_hacia_atras(lote_id)


@router.get("/lotes/{lote_id}/hacia-adelante", response_model=list[RelacionGenealogicaRead])
def recorrer_lote_hacia_adelante(lote_id: int, db: DbSession) -> list[object]:
    return TrazabilidadService(db).recorrer_hacia_adelante(lote_id)


@router.get("/lotes/{lote_id}/grafo", response_model=GrafoTrazabilidadRead)
def obtener_grafo_lote(lote_id: int, db: DbSession) -> dict[str, object]:
    return TrazabilidadService(db).construir_grafo_base(lote_id)
