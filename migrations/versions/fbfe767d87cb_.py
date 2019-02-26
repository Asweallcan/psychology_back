"""empty message

Revision ID: fbfe767d87cb
Revises: 8ad981edd4a1
Create Date: 2019-02-24 23:27:12.991486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbfe767d87cb'
down_revision = '8ad981edd4a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('grades_ibfk_1', 'grades', type_='foreignkey')
    op.drop_constraint('grades_ibfk_2', 'grades', type_='foreignkey')
    op.create_foreign_key(None, 'grades', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'grades', 'papers', ['paper_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('rb_users_papers_ibfk_2', 'rb_users_papers', type_='foreignkey')
    op.drop_constraint('rb_users_papers_ibfk_1', 'rb_users_papers', type_='foreignkey')
    op.create_foreign_key(None, 'rb_users_papers', 'papers', ['paper_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'rb_users_papers', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rb_users_papers', type_='foreignkey')
    op.drop_constraint(None, 'rb_users_papers', type_='foreignkey')
    op.create_foreign_key('rb_users_papers_ibfk_1', 'rb_users_papers', 'users', ['user_id'], ['id'])
    op.create_foreign_key('rb_users_papers_ibfk_2', 'rb_users_papers', 'papers', ['paper_id'], ['id'])
    op.drop_constraint(None, 'grades', type_='foreignkey')
    op.drop_constraint(None, 'grades', type_='foreignkey')
    op.create_foreign_key('grades_ibfk_2', 'grades', 'papers', ['paper_id'], ['id'])
    op.create_foreign_key('grades_ibfk_1', 'grades', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###