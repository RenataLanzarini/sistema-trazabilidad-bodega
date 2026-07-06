from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Cliente(Base):
    """Cliente o destino comercial de ventas y despachos."""

    __tablename__ = "clientes"
    __table_args__ = (
        UniqueConstraint("nombre", name="uq_clientes_nombre"),
        UniqueConstraint("identificacion_fiscal", name="uq_clientes_identificacion_fiscal"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    identificacion_fiscal: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ubicacion: Mapped[str | None] = mapped_column(String(255), nullable=True)
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
