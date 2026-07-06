from app.models.estado_lote import EstadoLote
from app.repositories.base import BaseRepository
from app.repositories.mixins import ActivosMixin, NombreLookupMixin


class EstadoLoteRepository(NombreLookupMixin, ActivosMixin, BaseRepository[EstadoLote]):
    model = EstadoLote
