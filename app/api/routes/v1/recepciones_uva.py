from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.core.exceptions import NotFoundError
from app.repositories.recepcion_uva_repository import RecepcionUvaRepository
from app.schemas.recepcion_uva import RecepcionUvaCreate, RecepcionUvaRead
from app.services.recepcion_uva_service import RecepcionUvaService


router = APIRouter(prefix="/recepciones-uva", tags=["recepciones-uva"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[RecepcionUvaRead])
def listar_recepciones_uva(db: DbSession) -> list[object]:
    return RecepcionUvaRepository(db).list()


@router.get("/numero-ciu/{numero_ciu}", response_model=RecepcionUvaRead)
def obtener_recepcion_uva_por_numero_ciu(numero_ciu: str, db: DbSession) -> object:
    recepcion = RecepcionUvaRepository(db).get_by_numero_ciu(numero_ciu)
    if recepcion is None:
        raise NotFoundError("Recepcion de uva no encontrada.")
    return recepcion


@router.get("/{recepcion_uva_id}", response_model=RecepcionUvaRead)
def obtener_recepcion_uva(recepcion_uva_id: int, db: DbSession) -> object:
    recepcion = RecepcionUvaRepository(db).get_by_id(recepcion_uva_id)
    if recepcion is None:
        raise NotFoundError("Recepcion de uva no encontrada.")
    return recepcion


@router.post("", response_model=RecepcionUvaRead, status_code=201)
def crear_recepcion_uva(data: RecepcionUvaCreate, db: DbSession) -> object:
    return RecepcionUvaService(db).crear_recepcion(data)
