"""Refactor Asset to Listing model

Revision ID: 9223aea760a1
Revises: 1826303a9c0b
Create Date: 2025-11-21 21:40:52.098174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9223aea760a1'
down_revision: Union[str, Sequence[str], None] = '1826303a9c0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'listings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('asset_id', sa.Integer(), nullable=False),
        sa.Column('exchange_id', sa.Integer(), nullable=False),
        sa.Column('ticker', sa.String(length=20), nullable=False),
        sa.Column('currency', sa.String(length=10), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('length(ticker) > 0', name='check_ticker_length'),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['exchange_id'], ['exchanges.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticker', 'exchange_id', name='uq_listing_ticker_exchange')
    )

    connection = op.get_bind()
    connection.execute(
        sa.text(
            """
            INSERT INTO listings (asset_id, exchange_id, ticker, currency, is_active, created_at, updated_at)
            SELECT id, exchange_id, ticker, :currency, is_active, created_at, updated_at
            FROM assets
            WHERE ticker IS NOT NULL
            """
        ),
        {"currency": "USD"},
    )

    op.drop_constraint('fk_assets_exchange_id_exchanges', 'assets', type_='foreignkey')
    op.drop_constraint('uq_assets_ticker', 'assets', type_='unique')
    op.drop_constraint('check_ticker_length', 'assets', type_='check')
    op.drop_column('assets', 'exchange_id')
    op.drop_column('assets', 'ticker')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('assets', sa.Column('exchange_id', sa.Integer(), autoincrement=False, nullable=True))
    op.add_column('assets', sa.Column('ticker', sa.String(length=20), autoincrement=False, nullable=True))

    connection = op.get_bind()
    connection.execute(
        sa.text(
            """
            WITH first_listing AS (
                SELECT DISTINCT ON (asset_id) asset_id, ticker, exchange_id
                FROM listings
                ORDER BY asset_id, id
            )
            UPDATE assets
            SET ticker = first_listing.ticker,
                exchange_id = first_listing.exchange_id
            FROM first_listing
            WHERE assets.id = first_listing.asset_id
            """
        )
    )

    op.alter_column('assets', 'ticker', existing_type=sa.String(length=20), nullable=False)
    op.alter_column('assets', 'exchange_id', existing_type=sa.Integer(), nullable=False)
    op.create_check_constraint('check_ticker_length', 'assets', 'length(ticker) > 0')
    op.create_unique_constraint('uq_assets_ticker', 'assets', ['ticker'])
    op.create_foreign_key(
        'fk_assets_exchange_id_exchanges',
        'assets',
        'exchanges',
        ['exchange_id'],
        ['id'],
    )

    op.drop_table('listings')
