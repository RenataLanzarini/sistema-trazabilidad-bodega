from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Usuario(Base):
    """Usuario responsable de operaciones y auditoria del sistema."""

    __tablename__ = "usuarios"
    __table_args__ = (
        UniqueConstraint("email", name="uq_usuarios_email"),
        Index("ix_usuarios_bodega_id", "bodega_id"),
        Index("ix_usuarios_rol_id", "rol_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    bodega_id: Mapped[int] = mapped_column(ForeignKey("bodegas.id"), nullable=False)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(50), nullable=True)
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

    bodega: Mapped["Bodega"] = relationship(back_populates="usuarios")
    rol: Mapped["Rol"] = relationship(back_populates="usuarios")
    recepciones_uva: Mapped[list["RecepcionUva"]] = relationship(back_populates="responsable")
    operaciones_productivas: Mapped[list["OperacionProductiva"]] = relationship(
        back_populates="responsable"
    )
    movimientos_fisicos: Mapped[list["MovimientoFisico"]] = relationship(
        back_populates="responsable"
    )
    mermas: Mapped[list["Merma"]] = relationship(back_populates="responsable")
    fraccionamientos: Mapped[list["Fraccionamiento"]] = relationship(
        back_populates="responsable"
    )
    ventas_granel: Mapped[list["VentaGranel"]] = relationship(back_populates="responsable")
    ordenes_trabajo: Mapped[list["OrdenTrabajo"]] = relationship(back_populates="operario")
    cortes_teoricos: Mapped[list["CorteTeorico"]] = relationship(back_populates="responsable")
