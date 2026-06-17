"""Create comment table

Revision ID: d5a463bf9802
Revises: f98071db1c79
Create Date: 2026-06-17 15:05:04.764431

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5a463bf9802'
down_revision: Union[str, Sequence[str], None] = 'f98071db1c79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_index(op.f('ix_comments_task_id'), 'comments', ['task_id'], unique=False)
    op.create_index(op.f('ix_comments_author_id'), 'comments', ['author_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_comments_author_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_task_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
