from sqlalchemy import select

from app.models.usuario import Usuario
from app.repositories.base import BaseRepository
from app.repositories.mixins import ActivosMixin


class UsuarioRepository(ActivosMixin, BaseRepository[Usuario]):
    model = Usuario

    def get_by_email(self, email: str) -> Usuario | None:
        statement = select(self.model).where(self.model.email == email)
        return self.session.scalar(statement)

    def list_by_bodega(self, bodega_id: int) -> list[Usuario]:
        statement = select(self.model).where(self.model.bodega_id == bodega_id)
        return list(self.session.scalars(statement))
