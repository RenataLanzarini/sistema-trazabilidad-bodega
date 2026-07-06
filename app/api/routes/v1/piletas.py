from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.core.exceptions import NotFoundError
from app.repositories.pileta_repository import PiletaRepository
from app.schemas.pileta import PiletaCreate, PiletaRead
from app.services.pileta_service import PiletaService


router = APIRouter(prefix="/piletas", tags=["piletas"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[PiletaRead])
def listar_piletas(db: DbSession) -> list[object]:
    return PiletaRepository(db).list()


@router.get("/codigo/{codigo}", response_model=PiletaRead)
def obtener_pileta_por_codigo(codigo: str, db: DbSession) -> object:
    pileta = PiletaRepository(db).get_by_codigo(codigo)
    if pileta is None:
        raise NotFoundError("Pileta no encontrada.")
    return pileta


@router.get("/bodega/{bodega_id}", response_model=list[PiletaRead])
def listar_piletas_por_bodega(bodega_id: int, db: DbSession) -> list[object]:
    return PiletaRepository(db).list_by_bodega(bodega_id)


@router.get("/deposito/{deposito_id}", response_model=list[PiletaRead])
def listar_piletas_por_deposito(deposito_id: int, db: DbSession) -> list[object]:
    return PiletaRepository(db).list_by_deposito(deposito_id)


@router.get("/estado/{estado_pileta_id}", response_model=list[PiletaRead])
def listar_piletas_por_estado(estado_pileta_id: int, db: DbSession) -> list[object]:
    return PiletaRepository(db).list_by_estado(estado_pileta_id)


@router.get("/{pileta_id}", response_model=PiletaRead)
def obtener_pileta(pileta_id: int, db: DbSession) -> object:
    pileta = PiletaRepository(db).get_by_id(pileta_id)
    if pileta is None:
        raise NotFoundError("Pileta no encontrada.")
    return pileta


@router.post("", response_model=PiletaRead, status_code=201)
def crear_pileta(data: PiletaCreate, db: DbSession) -> object:
    return PiletaService(db).crear_pileta(data)
