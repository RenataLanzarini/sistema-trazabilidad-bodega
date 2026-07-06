from sqlalchemy import select

from app.models.lote import Lote
from app.repositories.base import BaseRepository


class LoteRepository(BaseRepository[Lote]):
    model = Lote

    def get_by_codigo(self, codigo: str) -> Lote | None:
        statement = select(self.model).where(self.model.codigo == codigo)
        return self.session.scalar(statement)

    def list_by_bodega(self, bodega_id: int) -> list[Lote]:
        statement = select(self.model).where(self.model.bodega_id == bodega_id)
        return list(self.session.scalars(statement))

    def list_by_estado(self, estado_lote_id: int) -> list[Lote]:
        statement = select(self.model).where(self.model.estado_lote_id == estado_lote_id)
        return list(self.session.scalars(statement))

    def list_by_recepcion_uva(self, recepcion_uva_id: int) -> list[Lote]:
        statement = select(self.model).where(self.model.recepcion_uva_id == recepcion_uva_id)
        return list(self.session.scalars(statement))

    def list_by_variedad(self, variedad_principal_id: int) -> list[Lote]:
        statement = select(self.model).where(
            self.model.variedad_principal_id == variedad_principal_id
        )
        return list(self.session.scalars(statement))

    def list_activos(self) -> list[Lote]:
        statement = select(self.model).where(self.model.activo.is_(True))
        return list(self.session.scalars(statement))
