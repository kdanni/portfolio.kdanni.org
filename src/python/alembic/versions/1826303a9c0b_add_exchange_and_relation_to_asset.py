"""Add Exchange and relation to Asset

Revision ID: 1826303a9c0b
Revises: 7f4b26bc090f
Create Date: 2025-11-21 21:20:48.545587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1826303a9c0b'
down_revision: Union[str, Sequence[str], None] = '7f4b26bc090f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'exchanges',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('mic_code', sa.String(length=20), nullable=False),
        sa.Column('currency', sa.String(length=10), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('length(mic_code) > 0', name='check_mic_code_length'),
        sa.CheckConstraint('length(name) > 0', name='check_exchange_name_length'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('mic_code'),
    )

    op.add_column('assets', sa.Column('exchange_id', sa.Integer(), nullable=True))

    connection = op.get_bind()
    default_exchange_id = connection.execute(
        sa.text(
            """
            INSERT INTO exchanges (name, mic_code, currency, is_active)
            VALUES (:name, :mic_code, :currency, :is_active)
            RETURNING id
            """
        ),
        {
            "name": "Unknown Exchange",
            "mic_code": "UNKWN",
            "currency": "USD",
            "is_active": True,
        },
    ).scalar_one()

    connection.execute(
        sa.text("UPDATE assets SET exchange_id = :exchange_id WHERE exchange_id IS NULL"),
        {"exchange_id": default_exchange_id},
    )

    op.alter_column('assets', 'exchange_id', existing_type=sa.Integer(), nullable=False)
    op.create_foreign_key(
        'fk_assets_exchange_id_exchanges',
        'assets',
        'exchanges',
        ['exchange_id'],
        ['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_assets_exchange_id_exchanges', 'assets', type_='foreignkey')
    op.drop_column('assets', 'exchange_id')
    op.drop_table('exchanges')
