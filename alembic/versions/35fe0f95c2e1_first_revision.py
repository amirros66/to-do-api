"""First revision

Revision ID: 35fe0f95c2e1
Revises: 
Create Date: 2024-01-04 15:30:18.455824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35fe0f95c2e1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None: #function responsible for creating the tables and its columns
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lists',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lists_id'), 'lists', ['id'], unique=False)
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None: #function responsible for deleting tables
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_lists_id'), table_name='lists')
    op.drop_table('lists')
    # ### end Alembic commands ###


#Once revision is ready, it's time to upgrade which is what actually 
#creates the tables on the database. Using this command:
# pipenv run alembic upgrade head (the head means the most recent revision)