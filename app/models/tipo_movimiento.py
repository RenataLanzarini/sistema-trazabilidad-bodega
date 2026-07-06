from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TipoMovimiento(Base):
    __tablename__ = "tipos_movimiento"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    afecta_stock: Mapped[bool] = mapped_column(default=True, nullable=False)
    requiere_origen: Mapped[bool] = mapped_column(default=False, nullable=False)
    requiere_destino: Mapped[bool] = mapped_column(default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    movimientos: Mapped[list["Movimiento"]] = relationship(back_populates="tipo_movimiento")
