from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Deposito(Base):
    """Ubicacion fisica dentro de una bodega."""

    __tablename__ = "depositos"
    __table_args__ = (
        UniqueConstraint("bodega_id", "nombre", name="uq_depositos_bodega_nombre"),
        Index("ix_depositos_bodega_id", "bodega_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    bodega_id: Mapped[int] = mapped_column(ForeignKey("bodegas.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
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

    bodega: Mapped["Bodega"] = relationship(back_populates="depositos")
    piletas: Mapped[list["Pileta"]] = relationship(back_populates="deposito")
