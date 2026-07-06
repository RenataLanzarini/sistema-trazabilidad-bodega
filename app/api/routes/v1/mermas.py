from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.schemas.merma import MermaCreate, MermaRead
from app.services.merma_service import MermaService


router = APIRouter(prefix="/mermas", tags=["mermas"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=MermaRead, status_code=201)
def crear_merma(data: MermaCreate, db: DbSession) -> object:
    return MermaService(db).registrar_merma(**data.model_dump())


@router.get("/lote/{lote_id}", response_model=list[MermaRead])
def listar_mermas_por_lote(lote_id: int, db: DbSession) -> list[object]:
    return MermaService(db).listar_por_lote(lote_id)


@router.get("/pileta/{pileta_id}", response_model=list[MermaRead])
def listar_mermas_por_pileta(pileta_id: int, db: DbSession) -> list[object]:
    return MermaService(db).listar_por_pileta(pileta_id)


@router.get("/causa/{causa_merma_id}", response_model=list[MermaRead])
def listar_mermas_por_causa(causa_merma_id: int, db: DbSession) -> list[object]:
    return MermaService(db).listar_por_causa(causa_merma_id)


@router.get("/operacion/{operacion_id}", response_model=list[MermaRead])
def listar_mermas_por_operacion(operacion_id: int, db: DbSession) -> list[object]:
    return MermaService(db).listar_por_operacion(operacion_id)
