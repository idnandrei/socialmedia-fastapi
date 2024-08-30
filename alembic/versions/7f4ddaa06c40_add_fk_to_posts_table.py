"""add fk to posts table

Revision ID: 7f4ddaa06c40
Revises: d16f10139c37
Create Date: 2024-08-30 16:58:42.516861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f4ddaa06c40'
down_revision: Union[str, None] = 'd16f10139c37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', 
                          source_table="posts", 
                          referent_table="users", 
                          local_cols=['owner_id'], 
                          remote_cols=['id'], 
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
