from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AnalisisEnologico(Base):
    """Analisis de laboratorio registrado para una pileta y/o lote."""

    __tablename__ = "analisis_enologicos"
    __table_args__ = (
        Index("ix_analisis_enologicos_fecha", "fecha"),
        Index("ix_analisis_enologicos_lote_id", "lote_id"),
        Index("ix_analisis_enologicos_pileta_id", "pileta_id"),
        Index("ix_analisis_enologicos_bodega_id", "bodega_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    bodega_id: Mapped[int] = mapped_column(ForeignKey("bodegas.id"), nullable=False)
    lote_id: Mapped[int | None] = mapped_column(ForeignKey("lotes.id"), nullable=True)
    pileta_id: Mapped[int | None] = mapped_column(ForeignKey("piletas.id"), nullable=True)

    codigo_externo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fecha: Mapped[date | None] = mapped_column(Date, nullable=True)
    capacidad_litros: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    tipo: Mapped[str | None] = mapped_column(String(150), nullable=True)
    alcohol: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    azucar: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    volatil: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    acidez_total: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    ph: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    anhidrido_libre: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    anhidrido_total: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    extracto_seco: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    absorbancia_420: Mapped[Decimal | None] = mapped_column(Numeric(8, 3), nullable=True)
    absorbancia_520: Mapped[Decimal | None] = mapped_column(Numeric(8, 3), nullable=True)
    absorbancia_620: Mapped[Decimal | None] = mapped_column(Numeric(8, 3), nullable=True)
    intensidad: Mapped[Decimal | None] = mapped_column(Numeric(8, 3), nullable=True)
    indice: Mapped[Decimal | None] = mapped_column(Numeric(8, 3), nullable=True)
    suma_420_520_620: Mapped[Decimal | None] = mapped_column(Numeric(8, 3), nullable=True)
    brix: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    oxigeno: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
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

    bodega: Mapped["Bodega"] = relationship(back_populates="analisis_enologicos")
    lote: Mapped["Lote | None"] = relationship(back_populates="analisis_enologicos")
    pileta: Mapped["Pileta | None"] = relationship(back_populates="analisis_enologicos")
