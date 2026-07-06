from typing import TypeVar

from sqlalchemy import select

from app.database.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class NombreLookupMixin:
    def get_by_nombre(self, nombre: str) -> ModelType | None:
        statement = select(self.model).where(self.model.nombre == nombre)
        return self.session.scalar(statement)


class ActivosMixin:
    active_field = "activo"

    def list_activos(self) -> list[ModelType]:
        field = getattr(self.model, self.active_field)
        statement = select(self.model).where(field.is_(True))
        return list(self.session.scalars(statement))
