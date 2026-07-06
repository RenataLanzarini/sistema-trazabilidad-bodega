from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OperacionProductiva(Base):
    """Cabecera de un evento productivo u operativo ocurrido en la bodega."""

    __tablename__ = "operaciones_productivas"
    __table_args__ = (
        Index("ix_operaciones_productivas_bodega_id", "bodega_id"),
        Index("ix_operaciones_productivas_tipo_operacion_id", "tipo_operacion_id"),
        Index("ix_operaciones_productivas_responsable_id", "responsable_id"),
        Index("ix_operaciones_productivas_fecha", "fecha"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    bodega_id: Mapped[int] = mapped_column(ForeignKey("bodegas.id"), nullable=False)
    tipo_operacion_id: Mapped[int] = mapped_column(
        ForeignKey("tipos_operacion.id"), nullable=False
    )
    responsable_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    anulada: Mapped[bool] = mapped_column(default=False, nullable=False)
    motivo_anulacion: Mapped[str | None] = mapped_column(String(255), nullable=True)
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

    bodega: Mapped["Bodega"] = relationship(back_populates="operaciones_productivas")
    tipo_operacion: Mapped["TipoOperacion"] = relationship(
        back_populates="operaciones_productivas"
    )
    responsable: Mapped["Usuario"] = relationship(back_populates="operaciones_productivas")
    movimientos_fisicos: Mapped[list["MovimientoFisico"]] = relationship(
        back_populates="operacion_productiva"
    )
    relaciones_genealogicas: Mapped[list["RelacionGenealogicaLote"]] = relationship(
        back_populates="operacion_productiva"
    )
