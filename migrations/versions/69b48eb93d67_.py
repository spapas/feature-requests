"""empty message

Revision ID: 69b48eb93d67
Revises: 
Create Date: 2018-11-09 15:30:52.349331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69b48eb93d67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    mysql_engine='InnoDB'
    )
    op.create_table('productarea',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    mysql_engine='InnoDB'
    )
    op.create_table('featurerequest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('client_priority', sa.Integer(), nullable=True),
    sa.Column('target_date', sa.Date(), nullable=True),
    sa.Column('product_area_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['product_area_id'], ['productarea.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('featurerequest')
    op.drop_table('productarea')
    op.drop_table('client')
    # ### end Alembic commands ###
