from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Bodega(Base):
    """Unidad productiva o empresa bodeguera del sistema."""

    __tablename__ = "bodegas"
    __table_args__ = (
        UniqueConstraint("nombre", name="uq_bodegas_nombre"),
        UniqueConstraint("identificacion_fiscal", name="uq_bodegas_identificacion_fiscal"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    razon_social: Mapped[str | None] = mapped_column(String(180), nullable=True)
    identificacion_fiscal: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ubicacion: Mapped[str | None] = mapped_column(String(255), nullable=True)
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

    depositos: Mapped[list["Deposito"]] = relationship(back_populates="bodega")
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="bodega")
    piletas: Mapped[list["Pileta"]] = relationship(back_populates="bodega")
    recepciones_uva: Mapped[list["RecepcionUva"]] = relationship(back_populates="bodega")
    lotes: Mapped[list["Lote"]] = relationship(back_populates="bodega")
    analisis_enologicos: Mapped[list["AnalisisEnologico"]] = relationship(
        back_populates="bodega"
    )
    mediciones_fermentacion: Mapped[list["MedicionFermentacion"]] = relationship(
        back_populates="bodega"
    )
    operaciones_productivas: Mapped[list["OperacionProductiva"]] = relationship(
        back_populates="bodega"
    )
