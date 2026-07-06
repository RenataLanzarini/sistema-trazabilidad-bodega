from app.models.tipo_producto import TipoProducto
from app.repositories.base import BaseRepository
from app.repositories.mixins import ActivosMixin, NombreLookupMixin


class TipoProductoRepository(NombreLookupMixin, ActivosMixin, BaseRepository[TipoProducto]):
    model = TipoProducto
