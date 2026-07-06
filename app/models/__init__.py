from app.models.analisis_enologico import AnalisisEnologico
from app.models.bodega import Bodega
from app.models.calificacion_vino import CalificacionVino
from app.models.causa_merma import CausaMerma
from app.models.cliente import Cliente
from app.models.corte_teorico import CorteTeorico
from app.models.corte_teorico_detalle import CorteTeoricoDetalle
from app.models.deposito import Deposito
from app.models.estado_pileta import EstadoPileta
from app.models.estado_lote import EstadoLote
from app.models.fraccionamiento import Fraccionamiento
from app.models.fraccionamiento_detalle import FraccionamientoDetalle
from app.models.lote import Lote
from app.models.medicion_fermentacion import MedicionFermentacion
from app.models.merma import Merma
from app.models.movimiento_fisico import MovimientoFisico
from app.models.operacion_productiva import OperacionProductiva
from app.models.orden_trabajo import OrdenTrabajo
from app.models.origen_uva import OrigenUva
from app.models.pileta import Pileta
from app.models.producto_terminado import ProductoTerminado
from app.models.recepcion_uva import RecepcionUva
from app.models.relacion_genealogica_lote import RelacionGenealogicaLote
from app.models.rol import Rol
from app.models.tarea_orden_trabajo import TareaOrdenTrabajo
from app.models.tipo_operacion import TipoOperacion
from app.models.tipo_producto import TipoProducto
from app.models.usuario import Usuario
from app.models.variedad import Variedad
from app.models.venta_granel import VentaGranel
from app.models.venta_granel_detalle import VentaGranelDetalle

__all__ = [
    "Bodega",
    "AnalisisEnologico",
    "CalificacionVino",
    "CausaMerma",
    "Cliente",
    "CorteTeorico",
    "CorteTeoricoDetalle",
    "Deposito",
    "EstadoPileta",
    "EstadoLote",
    "Fraccionamiento",
    "FraccionamientoDetalle",
    "Lote",
    "MedicionFermentacion",
    "Merma",
    "MovimientoFisico",
    "OperacionProductiva",
    "OrdenTrabajo",
    "OrigenUva",
    "Pileta",
    "ProductoTerminado",
    "RecepcionUva",
    "RelacionGenealogicaLote",
    "Rol",
    "TareaOrdenTrabajo",
    "TipoOperacion",
    "TipoProducto",
    "Usuario",
    "Variedad",
    "VentaGranel",
    "VentaGranelDetalle",
]
