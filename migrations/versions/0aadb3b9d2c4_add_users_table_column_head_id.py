"""add users table column head_id

Revision ID: 0aadb3b9d2c4
Revises: fb97fe782979
Create Date: 2018-06-22 16:21:21.157000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0aadb3b9d2c4'
down_revision = 'fb97fe782979'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('head_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'head_id')
    # ### end Alembic commands ###
