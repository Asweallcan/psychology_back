"""empty message

Revision ID: 418a55c3d0e4
Revises: ecf8bba7ee40
Create Date: 2019-03-05 20:32:32.666956

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '418a55c3d0e4'
down_revision = 'ecf8bba7ee40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grades', sa.Column('finished', sa.Boolean(), nullable=True))
    op.drop_column('papers', 'finished')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('papers', sa.Column('finished', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('grades', 'finished')
    # ### end Alembic commands ###