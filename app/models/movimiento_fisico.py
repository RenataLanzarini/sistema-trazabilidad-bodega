from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class MovimientoFisico(Base):
    """Movimiento fisico de litros que constituye la fuente de verdad del stock."""

    __tablename__ = "movimientos_fisicos"
    __table_args__ = (
        CheckConstraint("litros > 0", name="ck_movimientos_fisicos_litros_positive"),
        Index("ix_movimientos_fisicos_operacion_productiva_id", "operacion_productiva_id"),
        Index("ix_movimientos_fisicos_lote_id", "lote_id"),
        Index("ix_movimientos_fisicos_pileta_origen_id", "pileta_origen_id"),
        Index("ix_movimientos_fisicos_pileta_destino_id", "pileta_destino_id"),
        Index("ix_movimientos_fisicos_responsable_id", "responsable_id"),
        Index("ix_movimientos_fisicos_fecha", "fecha"),
        Index("ix_movimientos_fisicos_codigo_externo", "codigo_externo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    operacion_productiva_id: Mapped[int] = mapped_column(
        ForeignKey("operaciones_productivas.id"), nullable=False
    )
    lote_id: Mapped[int] = mapped_column(ForeignKey("lotes.id"), nullable=False)
    pileta_origen_id: Mapped[int | None] = mapped_column(ForeignKey("piletas.id"), nullable=True)
    pileta_destino_id: Mapped[int | None] = mapped_column(ForeignKey("piletas.id"), nullable=True)
    responsable_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    codigo_externo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    litros: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    operacion_productiva: Mapped["OperacionProductiva"] = relationship(
        back_populates="movimientos_fisicos"
    )
    lote: Mapped["Lote"] = relationship(back_populates="movimientos_fisicos")
    pileta_origen: Mapped["Pileta | None"] = relationship(
        back_populates="movimientos_origen",
        foreign_keys=[pileta_origen_id],
    )
    pileta_destino: Mapped["Pileta | None"] = relationship(
        back_populates="movimientos_destino",
        foreign_keys=[pileta_destino_id],
    )
    responsable: Mapped["Usuario"] = relationship(back_populates="movimientos_fisicos")
