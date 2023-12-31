"""empty message

Revision ID: 590761f0a04b
Revises: 91851803dc9d
Create Date: 2023-06-02 14:16:09.466161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '590761f0a04b'
down_revision = '91851803dc9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mobil_disewa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_updated', sa.String(length=50), nullable=True))

    with op.batch_alter_table('pemesanan', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_updated', sa.String(length=50), nullable=True))

    with op.batch_alter_table('transaksi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_updated', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaksi', schema=None) as batch_op:
        batch_op.drop_column('last_updated')

    with op.batch_alter_table('pemesanan', schema=None) as batch_op:
        batch_op.drop_column('last_updated')

    with op.batch_alter_table('mobil_disewa', schema=None) as batch_op:
        batch_op.drop_column('last_updated')

    # ### end Alembic commands ###
