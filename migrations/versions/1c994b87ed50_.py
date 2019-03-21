"""empty message

Revision ID: 1c994b87ed50
Revises: 1e9562a251d5
Create Date: 2019-03-07 19:50:16.848925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c994b87ed50'
down_revision = '1e9562a251d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grades', sa.Column('above_percent', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('grades', 'above_percent')
    # ### end Alembic commands ###