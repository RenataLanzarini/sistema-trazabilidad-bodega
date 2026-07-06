from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Pileta(Base):
    __tablename__ = "piletas"
    __table_args__ = (
        CheckConstraint("capacidad_litros > 0", name="ck_piletas_capacidad_litros_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    capacidad_litros: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    estado_id: Mapped[int] = mapped_column(ForeignKey("estados_pileta.id"), nullable=False)
    ubicacion: Mapped[str | None] = mapped_column(String(120), nullable=True)
    material: Mapped[str | None] = mapped_column(String(80), nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    activa: Mapped[bool] = mapped_column(default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    estado: Mapped["EstadoPileta"] = relationship(back_populates="piletas")
    movimientos_origen: Mapped[list["Movimiento"]] = relationship(
        back_populates="pileta_origen", foreign_keys="Movimiento.pileta_origen_id"
    )
    movimientos_destino: Mapped[list["Movimiento"]] = relationship(
        back_populates="pileta_destino", foreign_keys="Movimiento.pileta_destino_id"
    )
