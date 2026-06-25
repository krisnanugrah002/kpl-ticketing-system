"""add booking id to ticket model

Revision ID: 8ccebf777d94
Revises: a8238945ed07
Create Date: 2026-06-25 17:39:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '8ccebf777d94'
down_revision: Union[str, None] = 'a8238945ed07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('tickets', sa.Column('booking_id', sa.UUID(), nullable=True))
    
    dummy_uuid = "00000000-0000-0000-0000-000000000000"
    op.execute(f"UPDATE tickets SET booking_id = '{dummy_uuid}' WHERE booking_id IS NULL")
    
    op.alter_column('tickets', 'booking_id', nullable=False)

def downgrade() -> None:
    op.drop_column('tickets', 'booking_id')