from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.corte_teorico import CorteTeorico
from app.models.corte_teorico_detalle import CorteTeoricoDetalle
from app.repositories.corte_teorico_repository import CorteTeoricoRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.operacion_productiva_repository import OperacionProductivaRepository
from app.repositories.pileta_repository import PiletaRepository
from app.repositories.usuario_repository import UsuarioRepository


class CorteTeoricoService:
    """Gestiona simulaciones de corte sin impacto en stock ni genealogia real."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.corte_repository = CorteTeoricoRepository(session)
        self.usuario_repository = UsuarioRepository(session)
        self.operacion_repository = OperacionProductivaRepository(session)
        self.pileta_repository = PiletaRepository(session)
        self.lote_repository = LoteRepository(session)

    def crear_corte_teorico(
        self,
        *,
        responsable_id: int | None = None,
        operacion_productiva_id: int | None = None,
        codigo_externo: str | None = None,
        fecha: date | None = None,
        nombre: str | None = None,
        observaciones: str | None = None,
        detalles: list[dict[str, Any]] | None = None,
    ) -> CorteTeorico:
        self._validar_corte(
            responsable_id=responsable_id,
            operacion_productiva_id=operacion_productiva_id,
        )

        corte = CorteTeorico(
            responsable_id=responsable_id,
            operacion_productiva_id=operacion_productiva_id,
            codigo_externo=codigo_externo,
            fecha=fecha,
            nombre=nombre,
            observaciones=observaciones,
        )

        try:
            corte = self.corte_repository.add(corte)
            for detalle_data in detalles or []:
                self._crear_detalle(
                    corte_teorico_id=corte.id,
                    detalle_data=detalle_data,
                )

            self.session.commit()
            self.session.refresh(corte)
            return corte
        except Exception:
            self.session.rollback()
            raise

    def listar(self) -> list[CorteTeorico]:
        return self.corte_repository.list()

    def obtener_por_id(self, corte_teorico_id: int) -> CorteTeorico:
        corte = self.corte_repository.get_by_id(corte_teorico_id)
        if corte is None:
            raise NotFoundError("Corte teorico no encontrado.")
        return corte

    def obtener_detalles_por_corte(
        self,
        corte_teorico_id: int,
    ) -> list[CorteTeoricoDetalle]:
        return self.corte_repository.list_detalles_by_corte(corte_teorico_id)

    def crear_detalle_corte(
        self,
        corte_teorico_id: int,
        *,
        pileta_id: int | None = None,
        lote_id: int | None = None,
        codigo_externo: str | None = None,
        volumen_al_corte: Decimal | None = None,
        varietal_snapshot: str | None = None,
        volumen_actual_snapshot: Decimal | None = None,
        alcohol: Decimal | None = None,
        acidez_volatil: Decimal | None = None,
        acidez_total: Decimal | None = None,
        ph: Decimal | None = None,
        so2_libre: Decimal | None = None,
        so2_total: Decimal | None = None,
    ) -> CorteTeoricoDetalle:
        if self.corte_repository.get_by_id(corte_teorico_id) is None:
            raise NotFoundError("Corte teorico no encontrado.")

        try:
            detalle = self._crear_detalle(
                corte_teorico_id=corte_teorico_id,
                detalle_data={
                    "pileta_id": pileta_id,
                    "lote_id": lote_id,
                    "codigo_externo": codigo_externo,
                    "volumen_al_corte": volumen_al_corte,
                    "varietal_snapshot": varietal_snapshot,
                    "volumen_actual_snapshot": volumen_actual_snapshot,
                    "alcohol": alcohol,
                    "acidez_volatil": acidez_volatil,
                    "acidez_total": acidez_total,
                    "ph": ph,
                    "so2_libre": so2_libre,
                    "so2_total": so2_total,
                },
            )
            self.session.commit()
            self.session.refresh(detalle)
            return detalle
        except Exception:
            self.session.rollback()
            raise

    def listar_por_fecha(
        self,
        fecha_desde: date,
        fecha_hasta: date | None = None,
    ) -> list[CorteTeorico]:
        return self.corte_repository.list_by_fecha(fecha_desde, fecha_hasta)

    def listar_por_responsable(self, responsable_id: int) -> list[CorteTeorico]:
        return self.corte_repository.list_by_responsable(responsable_id)

    def vincular_operacion_productiva(
        self,
        corte_teorico_id: int,
        operacion_productiva_id: int | None,
    ) -> CorteTeorico:
        if (
            operacion_productiva_id is not None
            and self.operacion_repository.get_by_id(operacion_productiva_id) is None
        ):
            raise NotFoundError("Operacion productiva no encontrada.")

        corte = self.corte_repository.get_by_id(corte_teorico_id)
        if corte is None:
            raise NotFoundError("Corte teorico no encontrado.")
        corte.operacion_productiva_id = operacion_productiva_id

        try:
            self.session.commit()
            self.session.refresh(corte)
            return corte
        except Exception:
            self.session.rollback()
            raise

    def _crear_detalle(
        self,
        *,
        corte_teorico_id: int,
        detalle_data: dict[str, Any],
    ) -> CorteTeoricoDetalle:
        pileta_id = detalle_data.get("pileta_id")
        lote_id = detalle_data.get("lote_id")
        self._validar_detalle(
            pileta_id=int(pileta_id) if pileta_id is not None else None,
            lote_id=int(lote_id) if lote_id is not None else None,
        )

        detalle = CorteTeoricoDetalle(
            corte_teorico_id=corte_teorico_id,
            pileta_id=int(pileta_id) if pileta_id is not None else None,
            lote_id=int(lote_id) if lote_id is not None else None,
            codigo_externo=detalle_data.get("codigo_externo"),
            volumen_al_corte=self._decimal_or_none(detalle_data.get("volumen_al_corte")),
            varietal_snapshot=detalle_data.get("varietal_snapshot"),
            volumen_actual_snapshot=self._decimal_or_none(
                detalle_data.get("volumen_actual_snapshot")
            ),
            alcohol=self._decimal_or_none(detalle_data.get("alcohol")),
            acidez_volatil=self._decimal_or_none(detalle_data.get("acidez_volatil")),
            acidez_total=self._decimal_or_none(detalle_data.get("acidez_total")),
            ph=self._decimal_or_none(detalle_data.get("ph")),
            so2_libre=self._decimal_or_none(detalle_data.get("so2_libre")),
            so2_total=self._decimal_or_none(detalle_data.get("so2_total")),
        )
        return self.corte_repository.add_detalle(detalle)

    def _validar_corte(
        self,
        *,
        responsable_id: int | None,
        operacion_productiva_id: int | None,
    ) -> None:
        if (
            responsable_id is not None
            and self.usuario_repository.get_by_id(responsable_id) is None
        ):
            raise NotFoundError("Usuario responsable no encontrado.")
        if (
            operacion_productiva_id is not None
            and self.operacion_repository.get_by_id(operacion_productiva_id) is None
        ):
            raise NotFoundError("Operacion productiva no encontrada.")

    def _validar_detalle(
        self,
        *,
        pileta_id: int | None,
        lote_id: int | None,
    ) -> None:
        if pileta_id is not None and self.pileta_repository.get_by_id(pileta_id) is None:
            raise NotFoundError("Pileta no encontrada.")
        if lote_id is not None and self.lote_repository.get_by_id(lote_id) is None:
            raise NotFoundError("Lote no encontrado.")

    def _decimal_or_none(self, value: object) -> Decimal | None:
        if value is None:
            return None
        return Decimal(str(value))
