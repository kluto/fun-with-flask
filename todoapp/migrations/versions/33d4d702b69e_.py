"""empty message

Revision ID: 33d4d702b69e
Revises: 659874e200a4
Create Date: 2020-04-06 04:10:46.904775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33d4d702b69e'
down_revision = '659874e200a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    
    op.execute('UPDATE todos SET completed = False WHERE completed IS NULL')
    op.alter_column('todos', 'completed', nullable=False)
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
