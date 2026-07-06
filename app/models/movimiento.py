from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Movimiento(Base):
    __tablename__ = "movimientos"
    __table_args__ = (
        CheckConstraint("litros > 0", name="ck_movimientos_litros_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    tipo_movimiento_id: Mapped[int] = mapped_column(
        ForeignKey("tipos_movimiento.id"), nullable=False
    )
    lote_id: Mapped[int] = mapped_column(ForeignKey("lotes.id"), nullable=False, index=True)
    pileta_origen_id: Mapped[int | None] = mapped_column(
        ForeignKey("piletas.id"), nullable=True, index=True
    )
    pileta_destino_id: Mapped[int | None] = mapped_column(
        ForeignKey("piletas.id"), nullable=True, index=True
    )
    litros: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
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

    tipo_movimiento: Mapped["TipoMovimiento"] = relationship(back_populates="movimientos")
    lote: Mapped["Lote"] = relationship(back_populates="movimientos")
    pileta_origen: Mapped["Pileta | None"] = relationship(
        back_populates="movimientos_origen", foreign_keys=[pileta_origen_id]
    )
    pileta_destino: Mapped["Pileta | None"] = relationship(
        back_populates="movimientos_destino", foreign_keys=[pileta_destino_id]
    )
    usuario: Mapped["Usuario"] = relationship(back_populates="movimientos")
