from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.security import require_roles
from app.schemas.fraccionamiento import (
    FraccionamientoCreate,
    FraccionamientoRead,
)
from app.services.fraccionamiento_service import FraccionamientoService


router = APIRouter(prefix="/fraccionamientos", tags=["fraccionamientos"])
DbSession = Annotated[Session, Depends(get_db)]
WRITE_ACCESS = Depends(require_roles("Administrador", "Administrador/Dueño", "Enólogo"))


@router.post("", response_model=FraccionamientoRead, status_code=201, dependencies=[WRITE_ACCESS])
def crear_fraccionamiento(data: FraccionamientoCreate, db: DbSession) -> object:
    payload = data.model_dump()
    payload["detalles"] = [detalle.model_dump() for detalle in data.detalles]
    return FraccionamientoService(db).crear_fraccionamiento(**payload)


@router.get("", response_model=list[FraccionamientoRead])
def listar_fraccionamientos(db: DbSession) -> list[object]:
    return FraccionamientoService(db).listar()


@router.get("/lote/{lote_id}", response_model=list[FraccionamientoRead])
def listar_fraccionamientos_por_lote(lote_id: int, db: DbSession) -> list[object]:
    return FraccionamientoService(db).listar_por_lote(lote_id)


@router.get("/fecha/{fecha}", response_model=list[FraccionamientoRead])
def listar_fraccionamientos_por_fecha(fecha: date, db: DbSession) -> list[object]:
    return FraccionamientoService(db).listar_por_fecha(fecha)


@router.get("/{fraccionamiento_id}", response_model=FraccionamientoRead)
def obtener_fraccionamiento(fraccionamiento_id: int, db: DbSession) -> object:
    return FraccionamientoService(db).obtener_por_id(fraccionamiento_id)
