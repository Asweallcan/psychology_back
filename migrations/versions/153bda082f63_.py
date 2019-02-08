"""empty message

Revision ID: 153bda082f63
Revises: ec3e5f5ad97c
Create Date: 2019-02-07 19:05:01.384484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '153bda082f63'
down_revision = 'ec3e5f5ad97c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_paper_infos_id'), 'paper_infos', ['id'], unique=False)
    op.create_index(op.f('ix_paper_infos_table_name'), 'paper_infos', ['table_name'], unique=False)
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('register_time', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.drop_index('username', table_name='users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('username', 'users', ['username'], unique=True)
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_column('users', 'register_time')
    op.drop_column('users', 'last_seen')
    op.drop_index(op.f('ix_paper_infos_table_name'), table_name='paper_infos')
    op.drop_index(op.f('ix_paper_infos_id'), table_name='paper_infos')
    # ### end Alembic commands ###
