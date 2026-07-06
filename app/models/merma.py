from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Merma(Base):
    """Perdida de volumen asociada a una operacion productiva."""

    __tablename__ = "mermas"
    __table_args__ = (
        CheckConstraint("litros > 0", name="ck_mermas_litros_positive"),
        Index("ix_mermas_operacion_productiva_id", "operacion_productiva_id"),
        Index("ix_mermas_lote_id", "lote_id"),
        Index("ix_mermas_pileta_id", "pileta_id"),
        Index("ix_mermas_causa_merma_id", "causa_merma_id"),
        Index("ix_mermas_responsable_id", "responsable_id"),
        Index("ix_mermas_fecha", "fecha"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    operacion_productiva_id: Mapped[int] = mapped_column(
        ForeignKey("operaciones_productivas.id"), nullable=False
    )
    lote_id: Mapped[int] = mapped_column(ForeignKey("lotes.id"), nullable=False)
    pileta_id: Mapped[int | None] = mapped_column(ForeignKey("piletas.id"), nullable=True)
    causa_merma_id: Mapped[int] = mapped_column(ForeignKey("causas_merma.id"), nullable=False)
    responsable_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    litros: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
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

    operacion_productiva: Mapped["OperacionProductiva"] = relationship(back_populates="mermas")
    lote: Mapped["Lote"] = relationship(back_populates="mermas")
    pileta: Mapped["Pileta | None"] = relationship(back_populates="mermas")
    causa_merma: Mapped["CausaMerma"] = relationship(back_populates="mermas")
    responsable: Mapped["Usuario"] = relationship(back_populates="mermas")
