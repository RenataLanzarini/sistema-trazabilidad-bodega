from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TipoProducto(Base):
    """Catalogo de tipos de producto trazable."""

    __tablename__ = "tipos_producto"
    __table_args__ = (UniqueConstraint("nombre", name="uq_tipos_producto_nombre"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    lotes: Mapped[list["Lote"]] = relationship(back_populates="tipo_producto")
    productos_terminados: Mapped[list["ProductoTerminado"]] = relationship(
        back_populates="tipo_producto"
    )
