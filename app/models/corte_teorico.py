from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class CorteTeorico(Base):
    """Simulacion de corte planificada sin impacto en stock ni trazabilidad real."""

    __tablename__ = "cortes_teoricos"
    __table_args__ = (
        Index("ix_cortes_teoricos_codigo_externo", "codigo_externo"),
        Index("ix_cortes_teoricos_fecha", "fecha"),
        Index("ix_cortes_teoricos_responsable_id", "responsable_id"),
        Index("ix_cortes_teoricos_operacion_productiva_id", "operacion_productiva_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    responsable_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    operacion_productiva_id: Mapped[int | None] = mapped_column(
        ForeignKey("operaciones_productivas.id"), nullable=True
    )

    codigo_externo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fecha: Mapped[date | None] = mapped_column(Date, nullable=True)
    nombre: Mapped[str | None] = mapped_column(String(150), nullable=True)
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

    responsable: Mapped["Usuario | None"] = relationship(back_populates="cortes_teoricos")
    operacion_productiva: Mapped["OperacionProductiva | None"] = relationship(
        back_populates="cortes_teoricos"
    )
    detalles: Mapped[list["CorteTeoricoDetalle"]] = relationship(
        back_populates="corte_teorico"
    )
