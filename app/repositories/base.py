from typing import Generic, TypeVar

from sqlalchemy import exists as sqlalchemy_exists, select
from sqlalchemy.orm import Session

from app.database.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Repositorio base con operaciones tecnicas comunes sin manejo transaccional."""

    model: type[ModelType]

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id_: int) -> ModelType | None:
        return self.session.get(self.model, id_)

    def list(self, *, offset: int = 0, limit: int = 100) -> list[ModelType]:
        statement = select(self.model).offset(offset).limit(limit)
        return list(self.session.scalars(statement))

    def add(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        self.session.flush()
        return instance

    def remove(self, instance: ModelType) -> None:
        self.session.delete(instance)
        self.session.flush()

    def exists(self, id_: int) -> bool:
        statement = select(sqlalchemy_exists().where(self.model.id == id_))
        return bool(self.session.scalar(statement))
