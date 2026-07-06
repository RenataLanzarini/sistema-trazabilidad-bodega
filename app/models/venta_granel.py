from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class VentaGranel(Base):
    """Venta comercial de producto a granel asociada a una operacion productiva."""

    __tablename__ = "ventas_granel"
    __table_args__ = (
        Index("ix_ventas_granel_operacion_productiva_id", "operacion_productiva_id"),
        Index("ix_ventas_granel_cliente_id", "cliente_id"),
        Index("ix_ventas_granel_responsable_id", "responsable_id"),
        Index("ix_ventas_granel_fecha", "fecha"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    operacion_productiva_id: Mapped[int] = mapped_column(
        ForeignKey("operaciones_productivas.id"), nullable=False
    )
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    responsable_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    documento: Mapped[str | None] = mapped_column(String(120), nullable=True)
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
        back_populates="ventas_granel"
    )
    cliente: Mapped["Cliente"] = relationship(back_populates="ventas_granel")
    responsable: Mapped["Usuario"] = relationship(back_populates="ventas_granel")
    detalles: Mapped[list["VentaGranelDetalle"]] = relationship(back_populates="venta_granel")
