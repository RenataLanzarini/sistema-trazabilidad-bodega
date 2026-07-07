from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.catalogos import UsuarioRead
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: DbSession) -> TokenResponse:
    access_token = AuthService(db).login(data.email, data.password)
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UsuarioRead)
def obtener_usuario_actual(
    current_user: Annotated[Usuario, Depends(get_current_user)],
) -> Usuario:
    return current_user
