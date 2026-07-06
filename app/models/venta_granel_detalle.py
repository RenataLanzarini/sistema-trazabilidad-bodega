from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class VentaGranelDetalle(Base):
    """Detalle de lote, pileta y litros vendidos a granel."""

    __tablename__ = "venta_granel_detalles"
    __table_args__ = (
        CheckConstraint("litros > 0", name="ck_venta_granel_detalles_litros_positive"),
        Index("ix_venta_granel_detalles_venta_granel_id", "venta_granel_id"),
        Index("ix_venta_granel_detalles_lote_id", "lote_id"),
        Index("ix_venta_granel_detalles_pileta_id", "pileta_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    venta_granel_id: Mapped[int] = mapped_column(ForeignKey("ventas_granel.id"), nullable=False)
    lote_id: Mapped[int] = mapped_column(ForeignKey("lotes.id"), nullable=False)
    pileta_id: Mapped[int] = mapped_column(ForeignKey("piletas.id"), nullable=False)
    litros: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
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

    venta_granel: Mapped["VentaGranel"] = relationship(back_populates="detalles")
    lote: Mapped["Lote"] = relationship(back_populates="venta_granel_detalles")
    pileta: Mapped["Pileta"] = relationship(back_populates="venta_granel_detalles")
