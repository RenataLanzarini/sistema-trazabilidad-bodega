from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class FraccionamientoDetalle(Base):
    """Detalle de lotes y piletas consumidos por un fraccionamiento."""

    __tablename__ = "fraccionamiento_detalles"
    __table_args__ = (
        CheckConstraint(
            "litros_consumidos > 0",
            name="ck_fraccionamiento_detalles_litros_consumidos_positive",
        ),
        Index("ix_fraccionamiento_detalles_fraccionamiento_id", "fraccionamiento_id"),
        Index("ix_fraccionamiento_detalles_lote_id", "lote_id"),
        Index("ix_fraccionamiento_detalles_pileta_id", "pileta_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    fraccionamiento_id: Mapped[int] = mapped_column(
        ForeignKey("fraccionamientos.id"), nullable=False
    )
    lote_id: Mapped[int] = mapped_column(ForeignKey("lotes.id"), nullable=False)
    pileta_id: Mapped[int] = mapped_column(ForeignKey("piletas.id"), nullable=False)
    litros_consumidos: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
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

    fraccionamiento: Mapped["Fraccionamiento"] = relationship(back_populates="detalles")
    lote: Mapped["Lote"] = relationship(back_populates="fraccionamiento_detalles")
    pileta: Mapped["Pileta"] = relationship(back_populates="fraccionamiento_detalles")
