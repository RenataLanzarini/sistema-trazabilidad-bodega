from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, verify_password
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository


class AuthService:
    """Gestiona autenticacion JWT sin aplicar permisos ni proteger endpoints."""

    def __init__(self, session: Session) -> None:
        self.usuario_repository = UsuarioRepository(session)

    def authenticate_user(self, email: str, password: str) -> Usuario:
        usuario = self.usuario_repository.get_by_email(email)
        if usuario is None:
            raise UnauthorizedError("Credenciales invalidas.")
        if not usuario.activo:
            raise UnauthorizedError("Usuario inactivo.")

        if usuario.password_hash is None or not verify_password(
            password,
            usuario.password_hash,
        ):
            raise UnauthorizedError("Credenciales invalidas.")

        return usuario

    def login(self, email: str, password: str) -> str:
        usuario = self.authenticate_user(email, password)
        return create_access_token(
            subject=str(usuario.id),
            additional_claims={
                "email": usuario.email,
                "rol_id": usuario.rol_id,
                "bodega_id": usuario.bodega_id,
            },
        )
