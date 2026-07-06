from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.core.exceptions import NotFoundError
from app.repositories.bodega_repository import BodegaRepository
from app.repositories.calificacion_vino_repository import CalificacionVinoRepository
from app.repositories.causa_merma_repository import CausaMermaRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.deposito_repository import DepositoRepository
from app.repositories.estado_lote_repository import EstadoLoteRepository
from app.repositories.estado_pileta_repository import EstadoPiletaRepository
from app.repositories.rol_repository import RolRepository
from app.repositories.tarea_orden_trabajo_repository import TareaOrdenTrabajoRepository
from app.repositories.tipo_operacion_repository import TipoOperacionRepository
from app.repositories.tipo_producto_repository import TipoProductoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.variedad_repository import VariedadRepository
from app.schemas.catalogos import (
    BodegaRead,
    CalificacionVinoRead,
    CausaMermaRead,
    ClienteRead,
    DepositoRead,
    EstadoLoteRead,
    EstadoPiletaRead,
    RolRead,
    TareaOrdenTrabajoRead,
    TipoOperacionRead,
    TipoProductoRead,
    UsuarioRead,
    VariedadRead,
)


router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]


def _require_found(entity: object | None, message: str) -> object:
    if entity is None:
        raise NotFoundError(message)
    return entity


@router.get("/bodegas", response_model=list[BodegaRead], tags=["bodegas"])
def listar_bodegas(db: DbSession) -> list[object]:
    return BodegaRepository(db).list()


@router.get("/bodegas/nombre/{nombre}", response_model=BodegaRead, tags=["bodegas"])
def obtener_bodega_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        BodegaRepository(db).get_by_nombre(nombre),
        "Bodega no encontrada.",
    )


@router.get("/bodegas/{bodega_id}", response_model=BodegaRead, tags=["bodegas"])
def obtener_bodega(bodega_id: int, db: DbSession) -> object:
    return _require_found(BodegaRepository(db).get_by_id(bodega_id), "Bodega no encontrada.")


@router.get("/depositos", response_model=list[DepositoRead], tags=["depositos"])
def listar_depositos(db: DbSession) -> list[object]:
    return DepositoRepository(db).list()


@router.get("/depositos/nombre/{nombre}", response_model=DepositoRead, tags=["depositos"])
def obtener_deposito_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        DepositoRepository(db).get_by_nombre(nombre),
        "Deposito no encontrado.",
    )


@router.get("/depositos/{deposito_id}", response_model=DepositoRead, tags=["depositos"])
def obtener_deposito(deposito_id: int, db: DbSession) -> object:
    return _require_found(
        DepositoRepository(db).get_by_id(deposito_id),
        "Deposito no encontrado.",
    )


@router.get("/roles", response_model=list[RolRead], tags=["roles"])
def listar_roles(db: DbSession) -> list[object]:
    return RolRepository(db).list()


@router.get("/roles/nombre/{nombre}", response_model=RolRead, tags=["roles"])
def obtener_rol_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(RolRepository(db).get_by_nombre(nombre), "Rol no encontrado.")


@router.get("/roles/{rol_id}", response_model=RolRead, tags=["roles"])
def obtener_rol(rol_id: int, db: DbSession) -> object:
    return _require_found(RolRepository(db).get_by_id(rol_id), "Rol no encontrado.")


@router.get("/usuarios", response_model=list[UsuarioRead], tags=["usuarios"])
def listar_usuarios(db: DbSession) -> list[object]:
    return UsuarioRepository(db).list()


@router.get("/usuarios/email/{email}", response_model=UsuarioRead, tags=["usuarios"])
def obtener_usuario_por_email(email: str, db: DbSession) -> object:
    return _require_found(
        UsuarioRepository(db).get_by_email(email),
        "Usuario no encontrado.",
    )


@router.get("/usuarios/{usuario_id}", response_model=UsuarioRead, tags=["usuarios"])
def obtener_usuario(usuario_id: int, db: DbSession) -> object:
    return _require_found(
        UsuarioRepository(db).get_by_id(usuario_id),
        "Usuario no encontrado.",
    )


@router.get("/variedades", response_model=list[VariedadRead], tags=["variedades"])
def listar_variedades(db: DbSession) -> list[object]:
    return VariedadRepository(db).list()


@router.get("/variedades/nombre/{nombre}", response_model=VariedadRead, tags=["variedades"])
def obtener_variedad_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        VariedadRepository(db).get_by_nombre(nombre),
        "Variedad no encontrada.",
    )


@router.get("/variedades/{variedad_id}", response_model=VariedadRead, tags=["variedades"])
def obtener_variedad(variedad_id: int, db: DbSession) -> object:
    return _require_found(
        VariedadRepository(db).get_by_id(variedad_id),
        "Variedad no encontrada.",
    )


@router.get("/estados-lote", response_model=list[EstadoLoteRead], tags=["estados-lote"])
def listar_estados_lote(db: DbSession) -> list[object]:
    return EstadoLoteRepository(db).list()


@router.get("/estados-lote/nombre/{nombre}", response_model=EstadoLoteRead, tags=["estados-lote"])
def obtener_estado_lote_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        EstadoLoteRepository(db).get_by_nombre(nombre),
        "Estado de lote no encontrado.",
    )


@router.get("/estados-lote/{estado_lote_id}", response_model=EstadoLoteRead, tags=["estados-lote"])
def obtener_estado_lote(estado_lote_id: int, db: DbSession) -> object:
    return _require_found(
        EstadoLoteRepository(db).get_by_id(estado_lote_id),
        "Estado de lote no encontrado.",
    )


@router.get("/estados-pileta", response_model=list[EstadoPiletaRead], tags=["estados-pileta"])
def listar_estados_pileta(db: DbSession) -> list[object]:
    return EstadoPiletaRepository(db).list()


@router.get(
    "/estados-pileta/nombre/{nombre}",
    response_model=EstadoPiletaRead,
    tags=["estados-pileta"],
)
def obtener_estado_pileta_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        EstadoPiletaRepository(db).get_by_nombre(nombre),
        "Estado de pileta no encontrado.",
    )


@router.get(
    "/estados-pileta/{estado_pileta_id}",
    response_model=EstadoPiletaRead,
    tags=["estados-pileta"],
)
def obtener_estado_pileta(estado_pileta_id: int, db: DbSession) -> object:
    return _require_found(
        EstadoPiletaRepository(db).get_by_id(estado_pileta_id),
        "Estado de pileta no encontrado.",
    )


@router.get("/tipos-producto", response_model=list[TipoProductoRead], tags=["tipos-producto"])
def listar_tipos_producto(db: DbSession) -> list[object]:
    return TipoProductoRepository(db).list()


@router.get(
    "/tipos-producto/nombre/{nombre}",
    response_model=TipoProductoRead,
    tags=["tipos-producto"],
)
def obtener_tipo_producto_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        TipoProductoRepository(db).get_by_nombre(nombre),
        "Tipo de producto no encontrado.",
    )


@router.get(
    "/tipos-producto/{tipo_producto_id}",
    response_model=TipoProductoRead,
    tags=["tipos-producto"],
)
def obtener_tipo_producto(tipo_producto_id: int, db: DbSession) -> object:
    return _require_found(
        TipoProductoRepository(db).get_by_id(tipo_producto_id),
        "Tipo de producto no encontrado.",
    )


@router.get("/tipos-operacion", response_model=list[TipoOperacionRead], tags=["tipos-operacion"])
def listar_tipos_operacion(db: DbSession) -> list[object]:
    return TipoOperacionRepository(db).list()


@router.get(
    "/tipos-operacion/nombre/{nombre}",
    response_model=TipoOperacionRead,
    tags=["tipos-operacion"],
)
def obtener_tipo_operacion_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        TipoOperacionRepository(db).get_by_nombre(nombre),
        "Tipo de operacion no encontrado.",
    )


@router.get(
    "/tipos-operacion/{tipo_operacion_id}",
    response_model=TipoOperacionRead,
    tags=["tipos-operacion"],
)
def obtener_tipo_operacion(tipo_operacion_id: int, db: DbSession) -> object:
    return _require_found(
        TipoOperacionRepository(db).get_by_id(tipo_operacion_id),
        "Tipo de operacion no encontrado.",
    )


@router.get("/causas-merma", response_model=list[CausaMermaRead], tags=["causas-merma"])
def listar_causas_merma(db: DbSession) -> list[object]:
    return CausaMermaRepository(db).list()


@router.get("/causas-merma/nombre/{nombre}", response_model=CausaMermaRead, tags=["causas-merma"])
def obtener_causa_merma_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        CausaMermaRepository(db).get_by_nombre(nombre),
        "Causa de merma no encontrada.",
    )


@router.get("/causas-merma/{causa_merma_id}", response_model=CausaMermaRead, tags=["causas-merma"])
def obtener_causa_merma(causa_merma_id: int, db: DbSession) -> object:
    return _require_found(
        CausaMermaRepository(db).get_by_id(causa_merma_id),
        "Causa de merma no encontrada.",
    )


@router.get("/clientes", response_model=list[ClienteRead], tags=["clientes"])
def listar_clientes(db: DbSession) -> list[object]:
    return ClienteRepository(db).list()


@router.get("/clientes/nombre/{nombre}", response_model=ClienteRead, tags=["clientes"])
def obtener_cliente_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        ClienteRepository(db).get_by_nombre(nombre),
        "Cliente no encontrado.",
    )


@router.get("/clientes/{cliente_id}", response_model=ClienteRead, tags=["clientes"])
def obtener_cliente(cliente_id: int, db: DbSession) -> object:
    return _require_found(
        ClienteRepository(db).get_by_id(cliente_id),
        "Cliente no encontrado.",
    )


@router.get(
    "/calificaciones-vino",
    response_model=list[CalificacionVinoRead],
    tags=["calificaciones-vino"],
)
def listar_calificaciones_vino(db: DbSession) -> list[object]:
    return CalificacionVinoRepository(db).list()


@router.get(
    "/calificaciones-vino/nombre/{nombre}",
    response_model=CalificacionVinoRead,
    tags=["calificaciones-vino"],
)
def obtener_calificacion_vino_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        CalificacionVinoRepository(db).get_by_nombre(nombre),
        "Calificacion de vino no encontrada.",
    )


@router.get(
    "/calificaciones-vino/{calificacion_vino_id}",
    response_model=CalificacionVinoRead,
    tags=["calificaciones-vino"],
)
def obtener_calificacion_vino(calificacion_vino_id: int, db: DbSession) -> object:
    return _require_found(
        CalificacionVinoRepository(db).get_by_id(calificacion_vino_id),
        "Calificacion de vino no encontrada.",
    )


@router.get(
    "/tareas-orden-trabajo",
    response_model=list[TareaOrdenTrabajoRead],
    tags=["tareas-orden-trabajo"],
)
def listar_tareas_orden_trabajo(db: DbSession) -> list[object]:
    return TareaOrdenTrabajoRepository(db).list()


@router.get(
    "/tareas-orden-trabajo/nombre/{nombre}",
    response_model=TareaOrdenTrabajoRead,
    tags=["tareas-orden-trabajo"],
)
def obtener_tarea_orden_trabajo_por_nombre(nombre: str, db: DbSession) -> object:
    return _require_found(
        TareaOrdenTrabajoRepository(db).get_by_nombre(nombre),
        "Tarea de orden de trabajo no encontrada.",
    )


@router.get(
    "/tareas-orden-trabajo/{tarea_orden_trabajo_id}",
    response_model=TareaOrdenTrabajoRead,
    tags=["tareas-orden-trabajo"],
)
def obtener_tarea_orden_trabajo(tarea_orden_trabajo_id: int, db: DbSession) -> object:
    return _require_found(
        TareaOrdenTrabajoRepository(db).get_by_id(tarea_orden_trabajo_id),
        "Tarea de orden de trabajo no encontrada.",
    )
