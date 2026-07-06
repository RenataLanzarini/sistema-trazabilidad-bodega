from app.repositories.base import BaseRepository
from app.repositories.bodega_repository import BodegaRepository
from app.repositories.calificacion_vino_repository import CalificacionVinoRepository
from app.repositories.causa_merma_repository import CausaMermaRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.deposito_repository import DepositoRepository
from app.repositories.estado_lote_repository import EstadoLoteRepository
from app.repositories.estado_pileta_repository import EstadoPiletaRepository
from app.repositories.fraccionamiento_repository import FraccionamientoRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.merma_repository import MermaRepository
from app.repositories.movimiento_fisico_repository import MovimientoFisicoRepository
from app.repositories.operacion_productiva_repository import OperacionProductivaRepository
from app.repositories.pileta_repository import PiletaRepository
from app.repositories.producto_terminado_repository import ProductoTerminadoRepository
from app.repositories.recepcion_uva_repository import RecepcionUvaRepository
from app.repositories.relacion_genealogica_lote_repository import (
    RelacionGenealogicaLoteRepository,
)
from app.repositories.rol_repository import RolRepository
from app.repositories.tarea_orden_trabajo_repository import TareaOrdenTrabajoRepository
from app.repositories.tipo_operacion_repository import TipoOperacionRepository
from app.repositories.tipo_producto_repository import TipoProductoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.variedad_repository import VariedadRepository
from app.repositories.venta_granel_repository import VentaGranelRepository

__all__ = [
    "BaseRepository",
    "BodegaRepository",
    "CalificacionVinoRepository",
    "CausaMermaRepository",
    "ClienteRepository",
    "DepositoRepository",
    "EstadoLoteRepository",
    "EstadoPiletaRepository",
    "FraccionamientoRepository",
    "LoteRepository",
    "MermaRepository",
    "MovimientoFisicoRepository",
    "OperacionProductivaRepository",
    "PiletaRepository",
    "ProductoTerminadoRepository",
    "RecepcionUvaRepository",
    "RelacionGenealogicaLoteRepository",
    "RolRepository",
    "TareaOrdenTrabajoRepository",
    "TipoOperacionRepository",
    "TipoProductoRepository",
    "UsuarioRepository",
    "VariedadRepository",
    "VentaGranelRepository",
]
