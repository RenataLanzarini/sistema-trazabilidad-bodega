from sqlalchemy import select

from app.models.relacion_genealogica_lote import RelacionGenealogicaLote
from app.repositories.base import BaseRepository


class RelacionGenealogicaLoteRepository(BaseRepository[RelacionGenealogicaLote]):
    model = RelacionGenealogicaLote

    def list_padres(self, lote_hijo_id: int) -> list[RelacionGenealogicaLote]:
        statement = select(self.model).where(self.model.lote_hijo_id == lote_hijo_id)
        return list(self.session.scalars(statement))

    def list_hijos(self, lote_padre_id: int) -> list[RelacionGenealogicaLote]:
        statement = select(self.model).where(self.model.lote_padre_id == lote_padre_id)
        return list(self.session.scalars(statement))

    def list_by_operacion(
        self,
        operacion_productiva_id: int,
    ) -> list[RelacionGenealogicaLote]:
        statement = select(self.model).where(
            self.model.operacion_productiva_id == operacion_productiva_id
        )
        return list(self.session.scalars(statement))

    def list_by_lote_padre(self, lote_padre_id: int) -> list[RelacionGenealogicaLote]:
        statement = select(self.model).where(self.model.lote_padre_id == lote_padre_id)
        return list(self.session.scalars(statement))

    def list_by_lote_hijo(self, lote_hijo_id: int) -> list[RelacionGenealogicaLote]:
        statement = select(self.model).where(self.model.lote_hijo_id == lote_hijo_id)
        return list(self.session.scalars(statement))
