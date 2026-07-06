from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ProductoTerminado(Base):
    """Partida de producto terminado trazable hasta su lote de origen."""

    __tablename__ = "productos_terminados"
    __table_args__ = (
        CheckConstraint(
            "cantidad_unidades > 0",
            name="ck_productos_terminados_cantidad_unidades_positive",
        ),
        CheckConstraint(
            "volumen_unidad_ml > 0",
            name="ck_productos_terminados_volumen_unidad_ml_positive",
        ),
        CheckConstraint(
            "litros_totales > 0",
            name="ck_productos_terminados_litros_totales_positive",
        ),
        UniqueConstraint("codigo", name="uq_productos_terminados_codigo"),
        Index("ix_productos_terminados_fraccionamiento_id", "fraccionamiento_id"),
        Index("ix_productos_terminados_tipo_producto_id", "tipo_producto_id"),
        Index("ix_productos_terminados_lote_id", "lote_id"),
        Index("ix_productos_terminados_fecha_produccion", "fecha_produccion"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    fraccionamiento_id: Mapped[int] = mapped_column(
        ForeignKey("fraccionamientos.id"), nullable=False
    )
    tipo_producto_id: Mapped[int] = mapped_column(ForeignKey("tipos_producto.id"), nullable=False)
    lote_id: Mapped[int] = mapped_column(ForeignKey("lotes.id"), nullable=False)
    codigo: Mapped[str] = mapped_column(String(80), nullable=False)
    cantidad_unidades: Mapped[int] = mapped_column(Integer, nullable=False)
    volumen_unidad_ml: Mapped[int] = mapped_column(Integer, nullable=False)
    litros_totales: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    fecha_produccion: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
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

    fraccionamiento: Mapped["Fraccionamiento"] = relationship(
        back_populates="productos_terminados"
    )
    tipo_producto: Mapped["TipoProducto"] = relationship(
        back_populates="productos_terminados"
    )
    lote: Mapped["Lote"] = relationship(back_populates="productos_terminados")
