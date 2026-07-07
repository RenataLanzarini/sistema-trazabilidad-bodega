from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.security import require_roles
from app.schemas.movimiento_fisico import MovimientoFisicoCreate, MovimientoFisicoRead
from app.services.movimiento_fisico_service import MovimientoFisicoService


router = APIRouter(prefix="/movimientos-fisicos", tags=["movimientos-fisicos"])
DbSession = Annotated[Session, Depends(get_db)]
WRITE_ACCESS = Depends(require_roles("Administrador", "Administrador/Dueño", "Enólogo"))


@router.get("/lote/{lote_id}", response_model=list[MovimientoFisicoRead])
def listar_movimientos_por_lote(lote_id: int, db: DbSession) -> list[object]:
    return MovimientoFisicoService(db).obtener_movimientos_por_lote(lote_id)


@router.get("/pileta/{pileta_id}", response_model=list[MovimientoFisicoRead])
def listar_movimientos_por_pileta(pileta_id: int, db: DbSession) -> list[object]:
    return MovimientoFisicoService(db).obtener_movimientos_por_pileta(pileta_id)


@router.get("/operacion/{operacion_id}", response_model=list[MovimientoFisicoRead])
def listar_movimientos_por_operacion(operacion_id: int, db: DbSession) -> list[object]:
    return MovimientoFisicoService(db).obtener_movimientos_por_operacion(operacion_id)


@router.post("", response_model=MovimientoFisicoRead, status_code=201, dependencies=[WRITE_ACCESS])
def crear_movimiento_fisico(data: MovimientoFisicoCreate, db: DbSession) -> object:
    return MovimientoFisicoService(db).registrar_movimiento(**data.model_dump())
