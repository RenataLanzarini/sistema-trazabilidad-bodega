from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Lote(Base):
    """Unidad trazable principal de vino, mosto u otro producto intermedio."""

    __tablename__ = "lotes"
    __table_args__ = (
        UniqueConstraint("bodega_id", "codigo", name="uq_lotes_bodega_codigo"),
        Index("ix_lotes_bodega_id", "bodega_id"),
        Index("ix_lotes_recepcion_uva_id", "recepcion_uva_id"),
        Index("ix_lotes_tipo_producto_id", "tipo_producto_id"),
        Index("ix_lotes_estado_lote_id", "estado_lote_id"),
        Index("ix_lotes_variedad_principal_id", "variedad_principal_id"),
        Index("ix_lotes_fecha_nacimiento", "fecha_nacimiento"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    bodega_id: Mapped[int] = mapped_column(ForeignKey("bodegas.id"), nullable=False)
    tipo_producto_id: Mapped[int] = mapped_column(ForeignKey("tipos_producto.id"), nullable=False)
    estado_lote_id: Mapped[int] = mapped_column(ForeignKey("estados_lote.id"), nullable=False)
    recepcion_uva_id: Mapped[int | None] = mapped_column(
        ForeignKey("recepciones_uva.id"), nullable=True
    )
    variedad_principal_id: Mapped[int | None] = mapped_column(
        ForeignKey("variedades.id"), nullable=True
    )
    codigo: Mapped[str] = mapped_column(String(80), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    cosecha: Mapped[int | None] = mapped_column(nullable=True)
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

    bodega: Mapped["Bodega"] = relationship(back_populates="lotes")
    tipo_producto: Mapped["TipoProducto"] = relationship(back_populates="lotes")
    estado_lote: Mapped["EstadoLote"] = relationship(back_populates="lotes")
    recepcion_uva: Mapped["RecepcionUva | None"] = relationship(back_populates="lotes")
    variedad_principal: Mapped["Variedad | None"] = relationship(back_populates="lotes")
    movimientos_fisicos: Mapped[list["MovimientoFisico"]] = relationship(back_populates="lote")
    relaciones_como_padre: Mapped[list["RelacionGenealogicaLote"]] = relationship(
        back_populates="lote_padre",
        foreign_keys="RelacionGenealogicaLote.lote_padre_id",
    )
    relaciones_como_hijo: Mapped[list["RelacionGenealogicaLote"]] = relationship(
        back_populates="lote_hijo",
        foreign_keys="RelacionGenealogicaLote.lote_hijo_id",
    )
    mermas: Mapped[list["Merma"]] = relationship(back_populates="lote")
