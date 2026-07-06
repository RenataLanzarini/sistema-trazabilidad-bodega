from app.models.rol import Rol
from app.repositories.base import BaseRepository
from app.repositories.mixins import ActivosMixin, NombreLookupMixin


class RolRepository(NombreLookupMixin, ActivosMixin, BaseRepository[Rol]):
    model = Rol
