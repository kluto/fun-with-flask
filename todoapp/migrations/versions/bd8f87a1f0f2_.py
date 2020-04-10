"""empty message

Revision ID: bd8f87a1f0f2
Revises: 33d4d702b69e
Create Date: 2020-04-07 00:06:20.344492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd8f87a1f0f2'
down_revision = '33d4d702b69e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('todos', sa.Column('list_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'todos', 'todolists', ['list_id'], ['id'])
    op.execute("INSERT INTO todolists (name) VALUES ('Uncategorized');")
    op.execute('UPDATE todos SET list_id = 1 WHERE list_id IS NULL')
    op.alter_column('todos', 'list_id', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'list_id')
    op.drop_table('todolists')
    # ### end Alembic commands ###
