"""add medicion fermentacion table

Revision ID: 1d5a4b938f85
Revises: 6c6c4f1f5242
Create Date: 2026-07-06 10:54:20.494304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '1d5a4b938f85'
down_revision: Union[str, None] = '6c6c4f1f5242'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'mediciones_fermentacion',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bodega_id', sa.Integer(), nullable=False),
        sa.Column('pileta_id', sa.Integer(), nullable=True),
        sa.Column('lote_id', sa.Integer(), nullable=True),
        sa.Column('codigo_externo', sa.String(length=80), nullable=True),
        sa.Column('fecha', sa.Date(), nullable=True),
        sa.Column('turno', sa.String(length=50), nullable=True),
        sa.Column('grado_baume', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column('temperatura', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['bodega_id'], ['bodegas.id']),
        sa.ForeignKeyConstraint(['lote_id'], ['lotes.id']),
        sa.ForeignKeyConstraint(['pileta_id'], ['piletas.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'ix_mediciones_fermentacion_bodega_id',
        'mediciones_fermentacion',
        ['bodega_id'],
        unique=False,
    )
    op.create_index(
        'ix_mediciones_fermentacion_fecha',
        'mediciones_fermentacion',
        ['fecha'],
        unique=False,
    )
    op.create_index(
        'ix_mediciones_fermentacion_lote_id',
        'mediciones_fermentacion',
        ['lote_id'],
        unique=False,
    )
    op.create_index(
        'ix_mediciones_fermentacion_pileta_id',
        'mediciones_fermentacion',
        ['pileta_id'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index('ix_mediciones_fermentacion_pileta_id', table_name='mediciones_fermentacion')
    op.drop_index('ix_mediciones_fermentacion_lote_id', table_name='mediciones_fermentacion')
    op.drop_index('ix_mediciones_fermentacion_fecha', table_name='mediciones_fermentacion')
    op.drop_index('ix_mediciones_fermentacion_bodega_id', table_name='mediciones_fermentacion')
    op.drop_table('mediciones_fermentacion')
