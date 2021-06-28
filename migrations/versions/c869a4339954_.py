"""empty message

Revision ID: c869a4339954
Revises: a9d0ab8c9eaa
Create Date: 2021-06-28 06:06:15.063218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c869a4339954'
down_revision = 'a9d0ab8c9eaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('credits', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'credits')
    # ### end Alembic commands ###
