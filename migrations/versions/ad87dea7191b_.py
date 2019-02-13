"""empty message

Revision ID: ad87dea7191b
Revises: 0d455a0cc410
Create Date: 2019-02-13 20:51:51.601072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad87dea7191b'
down_revision = '0d455a0cc410'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paper_infos', sa.Column('average', sa.String(length=32), nullable=True))
    op.add_column('paper_infos', sa.Column('description', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_seen')
    op.drop_column('paper_infos', 'description')
    op.drop_column('paper_infos', 'average')
    # ### end Alembic commands ###
