from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class RelacionGenealogicaLote(Base):
    """Relacion historica padre-hijo entre lotes para soportar genealogia trazable."""

    __tablename__ = "relaciones_genealogicas_lote"
    __table_args__ = (
        CheckConstraint(
            "litros_aportados > 0",
            name="ck_relaciones_genealogicas_lote_litros_positive",
        ),
        CheckConstraint(
            "lote_padre_id <> lote_hijo_id",
            name="ck_relaciones_genealogicas_lote_padre_hijo_distintos",
        ),
        UniqueConstraint(
            "operacion_productiva_id",
            "lote_padre_id",
            "lote_hijo_id",
            name="uq_relaciones_genealogicas_lote_operacion_padre_hijo",
        ),
        Index(
            "ix_relaciones_genealogicas_lote_operacion_productiva_id",
            "operacion_productiva_id",
        ),
        Index("ix_relaciones_genealogicas_lote_lote_padre_id", "lote_padre_id"),
        Index("ix_relaciones_genealogicas_lote_lote_hijo_id", "lote_hijo_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    operacion_productiva_id: Mapped[int] = mapped_column(
        ForeignKey("operaciones_productivas.id"), nullable=False
    )
    lote_padre_id: Mapped[int] = mapped_column(ForeignKey("lotes.id"), nullable=False)
    lote_hijo_id: Mapped[int] = mapped_column(ForeignKey("lotes.id"), nullable=False)
    litros_aportados: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tipo_relacion: Mapped[str] = mapped_column(String(50), nullable=False)
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
        back_populates="relaciones_genealogicas"
    )
    lote_padre: Mapped["Lote"] = relationship(
        back_populates="relaciones_como_padre",
        foreign_keys=[lote_padre_id],
    )
    lote_hijo: Mapped["Lote"] = relationship(
        back_populates="relaciones_como_hijo",
        foreign_keys=[lote_hijo_id],
    )
