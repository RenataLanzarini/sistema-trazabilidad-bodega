from collections.abc import Callable
from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user_payload(
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> dict[str, Any]:
    if token is None:
        raise UnauthorizedError("Credenciales de autenticacion requeridas.")
    return decode_access_token(token)


def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> Usuario:
    payload = get_current_user_payload(token)
    subject = payload.get("sub")

    try:
        usuario_id = int(str(subject))
    except (TypeError, ValueError) as exc:
        raise UnauthorizedError("Token de autenticacion invalido.") from exc

    usuario = UsuarioRepository(db).get_by_id(usuario_id)
    if usuario is None:
        raise UnauthorizedError("Usuario autenticado no encontrado.")
    if not usuario.activo:
        raise UnauthorizedError("Usuario inactivo.")
    return usuario


def require_active_user(
    current_user: Annotated[Usuario, Depends(get_current_user)],
) -> Usuario:
    if not current_user.activo:
        raise UnauthorizedError("Usuario inactivo.")
    return current_user


def require_roles(*roles: str) -> Callable[[Usuario], Usuario]:
    allowed_roles = {_normalize_role(role) for role in roles if role.strip()}

    def dependency(
        current_user: Annotated[Usuario, Depends(require_active_user)],
    ) -> Usuario:
        if not allowed_roles:
            raise ForbiddenError("No hay roles autorizados configurados.")

        user_role = current_user.rol
        if user_role is None or not user_role.activo:
            raise ForbiddenError("Rol de usuario no autorizado.")

        role_name = _normalize_role(user_role.nombre)
        if role_name not in allowed_roles:
            raise ForbiddenError("Permisos insuficientes.")

        return current_user

    return dependency


def require_admin() -> Callable[[Usuario], Usuario]:
    return require_roles("Administrador", "Administrador/Dueño", "admin")


def _normalize_role(role: str) -> str:
    return role.strip().casefold()
