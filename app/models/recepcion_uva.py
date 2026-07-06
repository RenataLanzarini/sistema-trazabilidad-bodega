from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class RecepcionUva(Base):
    """Ingreso formal de uva a la bodega documentado mediante CIU."""

    __tablename__ = "recepciones_uva"
    __table_args__ = (
        CheckConstraint("kilos_recibidos > 0", name="ck_recepciones_uva_kilos_positive"),
        UniqueConstraint(
            "bodega_id",
            "numero_ciu",
            "cosecha",
            name="uq_recepciones_uva_bodega_numero_ciu_cosecha",
        ),
        Index("ix_recepciones_uva_bodega_id", "bodega_id"),
        Index("ix_recepciones_uva_origen_uva_id", "origen_uva_id"),
        Index("ix_recepciones_uva_variedad_id", "variedad_id"),
        Index("ix_recepciones_uva_responsable_id", "responsable_id"),
        Index("ix_recepciones_uva_fecha", "fecha"),
        Index("ix_recepciones_uva_finca", "finca"),
        Index("ix_recepciones_uva_inv", "inv"),
        Index("ix_recepciones_uva_patente", "patente"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    bodega_id: Mapped[int] = mapped_column(ForeignKey("bodegas.id"), nullable=False)
    origen_uva_id: Mapped[int] = mapped_column(ForeignKey("origenes_uva.id"), nullable=False)
    variedad_id: Mapped[int] = mapped_column(ForeignKey("variedades.id"), nullable=False)
    responsable_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    numero_ciu: Mapped[str] = mapped_column(String(80), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    cosecha: Mapped[int] = mapped_column(nullable=False)
    kilos_recibidos: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    semana: Mapped[int | None] = mapped_column(nullable=True)
    rto: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    finca: Mapped[str | None] = mapped_column(String(150), nullable=True)
    inv: Mapped[str | None] = mapped_column(String(80), nullable=True)
    cambio: Mapped[str | None] = mapped_column(String(80), nullable=True)
    cuartel: Mapped[str | None] = mapped_column(String(80), nullable=True)
    tachos: Mapped[int | None] = mapped_column(nullable=True)
    chofer: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cuit_cuil: Mapped[str | None] = mapped_column(String(50), nullable=True)
    camion: Mapped[str | None] = mapped_column(String(120), nullable=True)
    modelo: Mapped[str | None] = mapped_column(String(120), nullable=True)
    patente: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bruto_kg: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    tara_kg: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    neto_kg: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    uva_real_kg: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    destino_vino: Mapped[str | None] = mapped_column(String(120), nullable=True)
    brix_real: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    tenor_azucar: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    vasija: Mapped[str | None] = mapped_column(String(80), nullable=True)
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

    bodega: Mapped["Bodega"] = relationship(back_populates="recepciones_uva")
    origen_uva: Mapped["OrigenUva"] = relationship(back_populates="recepciones_uva")
    variedad: Mapped["Variedad"] = relationship(back_populates="recepciones_uva")
    responsable: Mapped["Usuario"] = relationship(back_populates="recepciones_uva")
    lotes: Mapped[list["Lote"]] = relationship(back_populates="recepcion_uva")
