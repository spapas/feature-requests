"""empty message

Revision ID: cb3172a4f209
Revises: a55c6dbb5d6c
Create Date: 2018-11-08 17:06:59.901125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb3172a4f209'
down_revision = 'a55c6dbb5d6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('title', table_name='featurerequest')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('title', 'featurerequest', ['title'], unique=True)
    # ### end Alembic commands ###