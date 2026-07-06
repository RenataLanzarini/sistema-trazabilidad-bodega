from app.models.estado_pileta import EstadoPileta
from app.repositories.base import BaseRepository
from app.repositories.mixins import ActivosMixin, NombreLookupMixin


class EstadoPiletaRepository(NombreLookupMixin, ActivosMixin, BaseRepository[EstadoPileta]):
    model = EstadoPileta
