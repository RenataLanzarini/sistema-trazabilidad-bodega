from app.models.tipo_operacion import TipoOperacion
from app.repositories.base import BaseRepository
from app.repositories.mixins import ActivosMixin, NombreLookupMixin


class TipoOperacionRepository(NombreLookupMixin, ActivosMixin, BaseRepository[TipoOperacion]):
    model = TipoOperacion
