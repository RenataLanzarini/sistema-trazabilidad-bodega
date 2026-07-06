from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Pileta(Base):
    """Contenedor fisico de vino, mosto u otros productos trazables."""

    __tablename__ = "piletas"
    __table_args__ = (
        CheckConstraint("capacidad_litros > 0", name="ck_piletas_capacidad_litros_positive"),
        CheckConstraint("litros_por_cm > 0", name="ck_piletas_litros_por_cm_positive"),
        UniqueConstraint("bodega_id", "codigo", name="uq_piletas_bodega_codigo"),
        Index("ix_piletas_bodega_id", "bodega_id"),
        Index("ix_piletas_deposito_id", "deposito_id"),
        Index("ix_piletas_estado_pileta_id", "estado_pileta_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    bodega_id: Mapped[int] = mapped_column(ForeignKey("bodegas.id"), nullable=False)
    deposito_id: Mapped[int] = mapped_column(ForeignKey("depositos.id"), nullable=False)
    estado_pileta_id: Mapped[int] = mapped_column(ForeignKey("estados_pileta.id"), nullable=False)
    codigo: Mapped[str] = mapped_column(String(80), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    capacidad_litros: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    litros_por_cm: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    material: Mapped[str | None] = mapped_column(String(80), nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    activa: Mapped[bool] = mapped_column(default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    bodega: Mapped["Bodega"] = relationship(back_populates="piletas")
    deposito: Mapped["Deposito"] = relationship(back_populates="piletas")
    estado: Mapped["EstadoPileta"] = relationship(back_populates="piletas")
    movimientos_origen: Mapped[list["MovimientoFisico"]] = relationship(
        back_populates="pileta_origen",
        foreign_keys="MovimientoFisico.pileta_origen_id",
    )
    movimientos_destino: Mapped[list["MovimientoFisico"]] = relationship(
        back_populates="pileta_destino",
        foreign_keys="MovimientoFisico.pileta_destino_id",
    )
    mermas: Mapped[list["Merma"]] = relationship(back_populates="pileta")
    fraccionamiento_detalles: Mapped[list["FraccionamientoDetalle"]] = relationship(
        back_populates="pileta"
    )
    venta_granel_detalles: Mapped[list["VentaGranelDetalle"]] = relationship(
        back_populates="pileta"
    )
    analisis_enologicos: Mapped[list["AnalisisEnologico"]] = relationship(
        back_populates="pileta"
    )
    mediciones_fermentacion: Mapped[list["MedicionFermentacion"]] = relationship(
        back_populates="pileta"
    )
    ordenes_trabajo: Mapped[list["OrdenTrabajo"]] = relationship(
        back_populates="pileta",
        foreign_keys="OrdenTrabajo.pileta_id",
    )
    ordenes_trabajo_origen: Mapped[list["OrdenTrabajo"]] = relationship(
        back_populates="pileta_origen",
        foreign_keys="OrdenTrabajo.pileta_origen_id",
    )
    ordenes_trabajo_destino: Mapped[list["OrdenTrabajo"]] = relationship(
        back_populates="pileta_destino",
        foreign_keys="OrdenTrabajo.pileta_destino_id",
    )
