"""empty message

Revision ID: fe1719c2d77e
Revises: 2908bb615d8f
Create Date: 2023-03-27 00:49:57.049287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe1719c2d77e'
down_revision = '2908bb615d8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaksi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tgl_kembali', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaksi', schema=None) as batch_op:
        batch_op.drop_column('tgl_kembali')

    # ### end Alembic commands ###
