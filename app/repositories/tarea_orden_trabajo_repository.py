from app.models.tarea_orden_trabajo import TareaOrdenTrabajo
from app.repositories.base import BaseRepository
from app.repositories.mixins import NombreLookupMixin


class TareaOrdenTrabajoRepository(NombreLookupMixin, BaseRepository[TareaOrdenTrabajo]):
    model = TareaOrdenTrabajo
