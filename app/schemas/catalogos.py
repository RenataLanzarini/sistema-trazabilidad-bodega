from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BodegaRead(ORMBase):
    id: int
    nombre: str
    razon_social: str | None
    identificacion_fiscal: str | None
    ubicacion: str | None
    activa: bool
    created_at: datetime
    updated_at: datetime


class DepositoRead(ORMBase):
    id: int
    bodega_id: int
    nombre: str
    tipo: str | None
    descripcion: str | None
    activo: bool
    created_at: datetime
    updated_at: datetime


class RolRead(ORMBase):
    id: int
    nombre: str
    descripcion: str | None
    activo: bool
    created_at: datetime
    updated_at: datetime


class UsuarioRead(ORMBase):
    id: int
    bodega_id: int
    rol_id: int
    nombre: str
    email: str
    telefono: str | None
    activo: bool
    created_at: datetime
    updated_at: datetime


class VariedadRead(ORMBase):
    id: int
    nombre: str
    descripcion: str | None
    activa: bool
    created_at: datetime
    updated_at: datetime


class EstadoLoteRead(ORMBase):
    id: int
    nombre: str
    descripcion: str | None
    activo: bool
    created_at: datetime
    updated_at: datetime


class EstadoPiletaRead(ORMBase):
    id: int
    nombre: str
    descripcion: str | None
    activo: bool
    created_at: datetime
    updated_at: datetime


class TipoProductoRead(ORMBase):
    id: int
    nombre: str
    descripcion: str | None
    activo: bool
    created_at: datetime
    updated_at: datetime


class TipoOperacionRead(ORMBase):
    id: int
    nombre: str
    descripcion: str | None
    activo: bool
    created_at: datetime
    updated_at: datetime


class CausaMermaRead(ORMBase):
    id: int
    nombre: str
    descripcion: str | None
    activa: bool
    created_at: datetime
    updated_at: datetime


class ClienteRead(ORMBase):
    id: int
    nombre: str
    identificacion_fiscal: str | None
    ubicacion: str | None
    activo: bool
    created_at: datetime
    updated_at: datetime


class CalificacionVinoRead(ORMBase):
    id: int
    nombre: str
    descripcion: str | None
    activa: bool
    created_at: datetime
    updated_at: datetime


class TareaOrdenTrabajoRead(ORMBase):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime
