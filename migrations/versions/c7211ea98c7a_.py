"""empty message

Revision ID: c7211ea98c7a
Revises: 83054b9c3ae1
Create Date: 2023-03-27 12:37:59.783318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7211ea98c7a'
down_revision = '83054b9c3ae1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaksi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('harga_sewa', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('denda_per_hari', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaksi', schema=None) as batch_op:
        batch_op.drop_column('denda_per_hari')
        batch_op.drop_column('harga_sewa')

    # ### end Alembic commands ###
