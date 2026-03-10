from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '9545f1b2a676'
down_revision: Union[str, Sequence[str], None] = '47f4fdf026b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.drop_table('user_home_link')
    op.drop_table('home')
    op.add_column('recyclable_items', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'recyclable_items', 'companies', ['company_id'], ['id'])

def downgrade():
    op.drop_constraint(None, 'recyclable_items', type_='foreignkey')
    op.drop_column('recyclable_items', 'company_id')