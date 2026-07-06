from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OrdenTrabajo(Base):
    """Orden operativa de trabajo registrada para tareas de bodega."""

    __tablename__ = "ordenes_trabajo"
    __table_args__ = (
        Index("ix_ordenes_trabajo_codigo_externo", "codigo_externo"),
        Index("ix_ordenes_trabajo_numero", "numero"),
        Index("ix_ordenes_trabajo_fecha", "fecha"),
        Index("ix_ordenes_trabajo_tarea_orden_trabajo_id", "tarea_orden_trabajo_id"),
        Index("ix_ordenes_trabajo_pileta_id", "pileta_id"),
        Index("ix_ordenes_trabajo_lote_id", "lote_id"),
        Index("ix_ordenes_trabajo_operario_id", "operario_id"),
        Index("ix_ordenes_trabajo_operacion_productiva_id", "operacion_productiva_id"),
        Index("ix_ordenes_trabajo_pileta_origen_id", "pileta_origen_id"),
        Index("ix_ordenes_trabajo_pileta_destino_id", "pileta_destino_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tarea_orden_trabajo_id: Mapped[int | None] = mapped_column(
        ForeignKey("tareas_orden_trabajo.id"), nullable=True
    )
    pileta_id: Mapped[int | None] = mapped_column(ForeignKey("piletas.id"), nullable=True)
    lote_id: Mapped[int | None] = mapped_column(ForeignKey("lotes.id"), nullable=True)
    operario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    operacion_productiva_id: Mapped[int | None] = mapped_column(
        ForeignKey("operaciones_productivas.id"), nullable=True
    )
    pileta_origen_id: Mapped[int | None] = mapped_column(ForeignKey("piletas.id"), nullable=True)
    pileta_destino_id: Mapped[int | None] = mapped_column(ForeignKey("piletas.id"), nullable=True)

    codigo_externo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    numero: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fecha: Mapped[date | None] = mapped_column(Date, nullable=True)
    volumen_lleno: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    variedad: Mapped[str | None] = mapped_column(String(150), nullable=True)
    anio: Mapped[int | None] = mapped_column(nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    insumo: Mapped[str | None] = mapped_column(String(150), nullable=True)
    cantidad: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    col1: Mapped[str | None] = mapped_column(String(120), nullable=True)
    litros_a_trasegar: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    lleno_disponible: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    litros_por_cm: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    pasada_a_trazabilidad: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    completada: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    fecha_completada: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    observaciones_completada: Mapped[str | None] = mapped_column(Text, nullable=True)
    so2l_real: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    tarea: Mapped["TareaOrdenTrabajo | None"] = relationship(
        back_populates="ordenes_trabajo"
    )
    pileta: Mapped["Pileta | None"] = relationship(
        back_populates="ordenes_trabajo",
        foreign_keys=[pileta_id],
    )
    lote: Mapped["Lote | None"] = relationship(back_populates="ordenes_trabajo")
    operario: Mapped["Usuario | None"] = relationship(back_populates="ordenes_trabajo")
    operacion_productiva: Mapped["OperacionProductiva | None"] = relationship(
        back_populates="ordenes_trabajo"
    )
    pileta_origen: Mapped["Pileta | None"] = relationship(
        back_populates="ordenes_trabajo_origen",
        foreign_keys=[pileta_origen_id],
    )
    pileta_destino: Mapped["Pileta | None"] = relationship(
        back_populates="ordenes_trabajo_destino",
        foreign_keys=[pileta_destino_id],
    )
