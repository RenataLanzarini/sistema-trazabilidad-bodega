from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class CorteTeoricoDetalle(Base):
    """Componente de una simulacion de corte con snapshots analiticos del momento."""

    __tablename__ = "corte_teorico_detalles"
    __table_args__ = (
        Index("ix_corte_teorico_detalles_corte_teorico_id", "corte_teorico_id"),
        Index("ix_corte_teorico_detalles_lote_id", "lote_id"),
        Index("ix_corte_teorico_detalles_pileta_id", "pileta_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    corte_teorico_id: Mapped[int] = mapped_column(ForeignKey("cortes_teoricos.id"), nullable=False)
    pileta_id: Mapped[int | None] = mapped_column(ForeignKey("piletas.id"), nullable=True)
    lote_id: Mapped[int | None] = mapped_column(ForeignKey("lotes.id"), nullable=True)

    codigo_externo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    volumen_al_corte: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    varietal_snapshot: Mapped[str | None] = mapped_column(String(150), nullable=True)
    volumen_actual_snapshot: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    alcohol: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    acidez_volatil: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    acidez_total: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    ph: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    so2_libre: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    so2_total: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    corte_teorico: Mapped["CorteTeorico"] = relationship(back_populates="detalles")
    pileta: Mapped["Pileta | None"] = relationship(back_populates="corte_teorico_detalles")
    lote: Mapped["Lote | None"] = relationship(back_populates="corte_teorico_detalles")
