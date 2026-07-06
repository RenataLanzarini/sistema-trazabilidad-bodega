from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Lote(Base):
    __tablename__ = "lotes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    variedad_id: Mapped[int] = mapped_column(ForeignKey("variedades.id"), nullable=False)
    fecha_creacion: Mapped[date] = mapped_column(Date, nullable=False)
    cosecha: Mapped[int | None] = mapped_column(nullable=True)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
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

    variedad: Mapped["Variedad"] = relationship(back_populates="lotes")
    movimientos: Mapped[list["Movimiento"]] = relationship(back_populates="lote")
