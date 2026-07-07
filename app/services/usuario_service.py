from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.core.security import hash_password
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.catalogos import UsuarioCreate


class UsuarioService:
    """Gestiona usuarios evitando persistir contrasenas en texto plano."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.usuario_repository = UsuarioRepository(session)

    def crear_usuario(self, data: UsuarioCreate) -> Usuario:
        if self.usuario_repository.get_by_email(data.email) is not None:
            raise ConflictError("Ya existe un usuario con ese email.")

        payload = data.model_dump(exclude={"password"})
        usuario = Usuario(
            **payload,
            password_hash=hash_password(data.password),
        )

        try:
            usuario = self.usuario_repository.add(usuario)
            self.session.commit()
            self.session.refresh(usuario)
            return usuario
        except Exception:
            self.session.rollback()
            raise
