from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.models.orden_trabajo import OrdenTrabajo
from app.repositories.lote_repository import LoteRepository
from app.repositories.operacion_productiva_repository import OperacionProductivaRepository
from app.repositories.orden_trabajo_repository import OrdenTrabajoRepository
from app.repositories.pileta_repository import PiletaRepository
from app.repositories.tarea_orden_trabajo_repository import TareaOrdenTrabajoRepository
from app.repositories.usuario_repository import UsuarioRepository


class OrdenTrabajoService:
    """Gestiona ordenes operativas sin impacto directo en stock."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.orden_repository = OrdenTrabajoRepository(session)
        self.tarea_repository = TareaOrdenTrabajoRepository(session)
        self.pileta_repository = PiletaRepository(session)
        self.lote_repository = LoteRepository(session)
        self.usuario_repository = UsuarioRepository(session)
        self.operacion_repository = OperacionProductivaRepository(session)

    def crear_orden_trabajo(
        self,
        *,
        tarea_orden_trabajo_id: int | None = None,
        pileta_id: int | None = None,
        lote_id: int | None = None,
        operario_id: int | None = None,
        operacion_productiva_id: int | None = None,
        pileta_origen_id: int | None = None,
        pileta_destino_id: int | None = None,
        codigo_externo: str | None = None,
        numero: str | None = None,
        fecha: date | None = None,
        volumen_lleno: Decimal | None = None,
        variedad: str | None = None,
        anio: int | None = None,
        observaciones: str | None = None,
        insumo: str | None = None,
        cantidad: Decimal | None = None,
        col1: str | None = None,
        litros_a_trasegar: Decimal | None = None,
        lleno_disponible: Decimal | None = None,
        litros_por_cm: Decimal | None = None,
        pasada_a_trazabilidad: bool | None = None,
        completada: bool | None = None,
        fecha_completada: datetime | None = None,
        observaciones_completada: str | None = None,
        so2l_real: Decimal | None = None,
    ) -> OrdenTrabajo:
        self._validar_referencias(
            tarea_orden_trabajo_id=tarea_orden_trabajo_id,
            pileta_id=pileta_id,
            lote_id=lote_id,
            operario_id=operario_id,
            operacion_productiva_id=operacion_productiva_id,
            pileta_origen_id=pileta_origen_id,
            pileta_destino_id=pileta_destino_id,
        )
        self._validar_completada(completada, fecha_completada)

        orden = OrdenTrabajo(
            tarea_orden_trabajo_id=tarea_orden_trabajo_id,
            pileta_id=pileta_id,
            lote_id=lote_id,
            operario_id=operario_id,
            operacion_productiva_id=operacion_productiva_id,
            pileta_origen_id=pileta_origen_id,
            pileta_destino_id=pileta_destino_id,
            codigo_externo=codigo_externo,
            numero=numero,
            fecha=fecha,
            volumen_lleno=volumen_lleno,
            variedad=variedad,
            anio=anio,
            observaciones=observaciones,
            insumo=insumo,
            cantidad=cantidad,
            col1=col1,
            litros_a_trasegar=litros_a_trasegar,
            lleno_disponible=lleno_disponible,
            litros_por_cm=litros_por_cm,
            pasada_a_trazabilidad=pasada_a_trazabilidad,
            completada=completada,
            fecha_completada=fecha_completada,
            observaciones_completada=observaciones_completada,
            so2l_real=so2l_real,
        )

        try:
            orden = self.orden_repository.add(orden)
            self.session.commit()
            self.session.refresh(orden)
            return orden
        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, orden_trabajo_id: int) -> OrdenTrabajo:
        orden = self.orden_repository.get_by_id(orden_trabajo_id)
        if orden is None:
            raise NotFoundError("Orden de trabajo no encontrada.")
        return orden

    def listar_pendientes(self) -> list[OrdenTrabajo]:
        return self.orden_repository.list_pendientes()

    def listar_completadas(self) -> list[OrdenTrabajo]:
        return self.orden_repository.list_completadas()

    def listar_por_operario(self, operario_id: int) -> list[OrdenTrabajo]:
        return self.orden_repository.list_by_operario(operario_id)

    def listar_por_pileta(self, pileta_id: int) -> list[OrdenTrabajo]:
        return self.orden_repository.list_by_pileta(pileta_id)

    def listar_por_lote(self, lote_id: int) -> list[OrdenTrabajo]:
        return self.orden_repository.list_by_lote(lote_id)

    def marcar_completada(
        self,
        orden_trabajo_id: int,
        *,
        fecha_completada: datetime,
        observaciones_completada: str | None = None,
    ) -> OrdenTrabajo:
        if fecha_completada is None:
            raise BusinessRuleError("Una OT completada debe tener fecha de completado.")

        orden = self.obtener_por_id(orden_trabajo_id)
        orden.completada = True
        orden.fecha_completada = fecha_completada
        orden.observaciones_completada = observaciones_completada

        try:
            self.session.commit()
            self.session.refresh(orden)
            return orden
        except Exception:
            self.session.rollback()
            raise

    def vincular_operacion_productiva(
        self,
        orden_trabajo_id: int,
        operacion_productiva_id: int | None,
    ) -> OrdenTrabajo:
        if (
            operacion_productiva_id is not None
            and self.operacion_repository.get_by_id(operacion_productiva_id) is None
        ):
            raise NotFoundError("Operacion productiva no encontrada.")

        orden = self.obtener_por_id(orden_trabajo_id)
        orden.operacion_productiva_id = operacion_productiva_id

        try:
            self.session.commit()
            self.session.refresh(orden)
            return orden
        except Exception:
            self.session.rollback()
            raise

    def _validar_referencias(
        self,
        *,
        tarea_orden_trabajo_id: int | None,
        pileta_id: int | None,
        lote_id: int | None,
        operario_id: int | None,
        operacion_productiva_id: int | None,
        pileta_origen_id: int | None,
        pileta_destino_id: int | None,
    ) -> None:
        if (
            tarea_orden_trabajo_id is not None
            and self.tarea_repository.get_by_id(tarea_orden_trabajo_id) is None
        ):
            raise NotFoundError("Tarea de orden de trabajo no encontrada.")
        if pileta_id is not None and self.pileta_repository.get_by_id(pileta_id) is None:
            raise NotFoundError("Pileta no encontrada.")
        if lote_id is not None and self.lote_repository.get_by_id(lote_id) is None:
            raise NotFoundError("Lote no encontrado.")
        if operario_id is not None and self.usuario_repository.get_by_id(operario_id) is None:
            raise NotFoundError("Operario no encontrado.")
        if (
            operacion_productiva_id is not None
            and self.operacion_repository.get_by_id(operacion_productiva_id) is None
        ):
            raise NotFoundError("Operacion productiva no encontrada.")
        if (
            pileta_origen_id is not None
            and self.pileta_repository.get_by_id(pileta_origen_id) is None
        ):
            raise NotFoundError("Pileta origen no encontrada.")
        if (
            pileta_destino_id is not None
            and self.pileta_repository.get_by_id(pileta_destino_id) is None
        ):
            raise NotFoundError("Pileta destino no encontrada.")
        if pileta_origen_id is not None and pileta_origen_id == pileta_destino_id:
            raise BusinessRuleError("La pileta origen y destino deben ser distintas.")

    def _validar_completada(
        self,
        completada: bool | None,
        fecha_completada: datetime | None,
    ) -> None:
        if completada is True and fecha_completada is None:
            raise BusinessRuleError("Una OT completada debe tener fecha de completado.")
