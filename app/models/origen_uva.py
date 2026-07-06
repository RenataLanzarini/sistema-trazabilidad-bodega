from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OrigenUva(Base):
    """Origen de uva propia o comprada a terceros."""

    __tablename__ = "origenes_uva"
    __table_args__ = (
        CheckConstraint("tipo IN ('propio', 'tercero')", name="ck_origenes_uva_tipo"),
        UniqueConstraint("nombre", "tipo", name="uq_origenes_uva_nombre_tipo"),
        UniqueConstraint("identificacion_fiscal", name="uq_origenes_uva_identificacion_fiscal"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
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

    recepciones_uva: Mapped[list["RecepcionUva"]] = relationship(back_populates="origen_uva")
