from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.core.exceptions import NotFoundError
from app.repositories.lote_repository import LoteRepository
from app.schemas.lote import LoteCreate, LoteRead
from app.services.lote_service import LoteService


router = APIRouter(prefix="/lotes", tags=["lotes"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[LoteRead])
def listar_lotes(db: DbSession) -> list[object]:
    return LoteRepository(db).list()


@router.get("/codigo/{codigo}", response_model=LoteRead)
def obtener_lote_por_codigo(codigo: str, db: DbSession) -> object:
    lote = LoteRepository(db).get_by_codigo(codigo)
    if lote is None:
        raise NotFoundError("Lote no encontrado.")
    return lote


@router.get("/recepcion-uva/{recepcion_uva_id}", response_model=list[LoteRead])
def listar_lotes_por_recepcion_uva(recepcion_uva_id: int, db: DbSession) -> list[object]:
    return LoteRepository(db).list_by_recepcion_uva(recepcion_uva_id)


@router.get("/{lote_id}", response_model=LoteRead)
def obtener_lote(lote_id: int, db: DbSession) -> object:
    lote = LoteRepository(db).get_by_id(lote_id)
    if lote is None:
        raise NotFoundError("Lote no encontrado.")
    return lote


@router.post("", response_model=LoteRead, status_code=201)
def crear_lote(data: LoteCreate, db: DbSession) -> object:
    return LoteService(db).crear_lote(data)
