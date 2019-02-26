"""empty message

Revision ID: ac492d9f1b6e
Revises: 271834fdb118
Create Date: 2019-02-25 10:39:39.357831

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ac492d9f1b6e'
down_revision = '271834fdb118'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'confirmed',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('users', 'is_admin',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'is_admin',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('users', 'confirmed',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    # ### end Alembic commands ###