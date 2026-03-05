"""add recyclables table

Revision ID: ad1a76efb0b0
Revises: a7ad07793fbc
Create Date: 2026-03-04 13:54:36.659717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad1a76efb0b0'
down_revision: Union[str, Sequence[str], None] = 'a7ad07793fbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # rename username -> company_name (keeps existing values)
    op.alter_column(
        "users",
        "username",
        new_column_name="company_name",
        existing_type=sa.VARCHAR(length=450),
        existing_nullable=False,
    )


def downgrade() -> None:
    # rename company_name -> username
    op.alter_column(
        "users",
        "company_name",
        new_column_name="username",
        existing_type=sa.VARCHAR(length=450),
        existing_nullable=False,
    )