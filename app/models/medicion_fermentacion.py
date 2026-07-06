from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Index, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class MedicionFermentacion(Base):
    """Medicion de Baume y temperatura durante la fermentacion."""

    __tablename__ = "mediciones_fermentacion"
    __table_args__ = (
        Index("ix_mediciones_fermentacion_bodega_id", "bodega_id"),
        Index("ix_mediciones_fermentacion_fecha", "fecha"),
        Index("ix_mediciones_fermentacion_lote_id", "lote_id"),
        Index("ix_mediciones_fermentacion_pileta_id", "pileta_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    bodega_id: Mapped[int] = mapped_column(ForeignKey("bodegas.id"), nullable=False)
    pileta_id: Mapped[int | None] = mapped_column(ForeignKey("piletas.id"), nullable=True)
    lote_id: Mapped[int | None] = mapped_column(ForeignKey("lotes.id"), nullable=True)

    codigo_externo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fecha: Mapped[date | None] = mapped_column(Date, nullable=True)
    turno: Mapped[str | None] = mapped_column(String(50), nullable=True)
    grado_baume: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    temperatura: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    bodega: Mapped["Bodega"] = relationship(back_populates="mediciones_fermentacion")
    pileta: Mapped["Pileta | None"] = relationship(back_populates="mediciones_fermentacion")
    lote: Mapped["Lote | None"] = relationship(back_populates="mediciones_fermentacion")
