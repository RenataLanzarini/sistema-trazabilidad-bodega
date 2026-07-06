from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TareaOrdenTrabajo(Base):
    """Catalogo de tareas disponibles para ordenes de trabajo de bodega."""

    __tablename__ = "tareas_orden_trabajo"
    __table_args__ = (UniqueConstraint("nombre", name="uq_tareas_orden_trabajo_nombre"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    ordenes_trabajo: Mapped[list["OrdenTrabajo"]] = relationship(back_populates="tarea")
