from sqlalchemy.orm import Session

from app.models.relacion_genealogica_lote import RelacionGenealogicaLote
from app.repositories.relacion_genealogica_lote_repository import (
    RelacionGenealogicaLoteRepository,
)


class TrazabilidadService:
    """Recorre relaciones genealogicas de lotes y prepara estructuras para grafo."""

    def __init__(self, session: Session) -> None:
        self.relacion_repository = RelacionGenealogicaLoteRepository(session)

    def obtener_padres(self, lote_id: int) -> list[RelacionGenealogicaLote]:
        return self.relacion_repository.list_padres(lote_id)

    def obtener_hijos(self, lote_id: int) -> list[RelacionGenealogicaLote]:
        return self.relacion_repository.list_hijos(lote_id)

    def recorrer_hacia_atras(self, lote_id: int) -> list[RelacionGenealogicaLote]:
        relaciones: list[RelacionGenealogicaLote] = []
        self._recorrer_padres(lote_id, relaciones, set())
        return relaciones

    def recorrer_hacia_adelante(self, lote_id: int) -> list[RelacionGenealogicaLote]:
        relaciones: list[RelacionGenealogicaLote] = []
        self._recorrer_hijos(lote_id, relaciones, set())
        return relaciones

    def construir_grafo_base(self, lote_id: int) -> dict[str, list[dict[str, object]]]:
        relaciones = [
            *self.recorrer_hacia_atras(lote_id),
            *self.recorrer_hacia_adelante(lote_id),
        ]
        nodos = {lote_id}
        aristas: list[dict[str, object]] = []

        for relacion in relaciones:
            nodos.add(relacion.lote_padre_id)
            nodos.add(relacion.lote_hijo_id)
            aristas.append(self._serializar_relacion(relacion))

        return {
            "nodos": [{"lote_id": nodo_id} for nodo_id in sorted(nodos)],
            "aristas": aristas,
        }

    def _recorrer_padres(
        self,
        lote_id: int,
        relaciones: list[RelacionGenealogicaLote],
        visitados: set[int],
    ) -> None:
        if lote_id in visitados:
            return
        visitados.add(lote_id)

        for relacion in self.obtener_padres(lote_id):
            relaciones.append(relacion)
            self._recorrer_padres(relacion.lote_padre_id, relaciones, visitados)

    def _recorrer_hijos(
        self,
        lote_id: int,
        relaciones: list[RelacionGenealogicaLote],
        visitados: set[int],
    ) -> None:
        if lote_id in visitados:
            return
        visitados.add(lote_id)

        for relacion in self.obtener_hijos(lote_id):
            relaciones.append(relacion)
            self._recorrer_hijos(relacion.lote_hijo_id, relaciones, visitados)

    def _serializar_relacion(self, relacion: RelacionGenealogicaLote) -> dict[str, object]:
        return {
            "relacion_id": relacion.id,
            "operacion_productiva_id": relacion.operacion_productiva_id,
            "lote_padre_id": relacion.lote_padre_id,
            "lote_hijo_id": relacion.lote_hijo_id,
            "litros_aportados": relacion.litros_aportados,
            "tipo_relacion": relacion.tipo_relacion,
        }
