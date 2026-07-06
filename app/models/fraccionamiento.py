from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Fraccionamiento(Base):
    """Proceso que convierte producto a granel en una partida fraccionada."""

    __tablename__ = "fraccionamientos"
    __table_args__ = (
        Index("ix_fraccionamientos_operacion_productiva_id", "operacion_productiva_id"),
        Index("ix_fraccionamientos_responsable_id", "responsable_id"),
        Index("ix_fraccionamientos_fecha", "fecha"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    operacion_productiva_id: Mapped[int] = mapped_column(
        ForeignKey("operaciones_productivas.id"), nullable=False
    )
    responsable_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
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
        back_populates="fraccionamientos"
    )
    responsable: Mapped["Usuario"] = relationship(back_populates="fraccionamientos")
    detalles: Mapped[list["FraccionamientoDetalle"]] = relationship(
        back_populates="fraccionamiento"
    )
    productos_terminados: Mapped[list["ProductoTerminado"]] = relationship(
        back_populates="fraccionamiento"
    )
