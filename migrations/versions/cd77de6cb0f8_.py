"""empty message

Revision ID: cd77de6cb0f8
Revises: cdac3a982b71
Create Date: 2023-03-29 00:50:27.578747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd77de6cb0f8'
down_revision = 'cdac3a982b71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaksi', schema=None) as batch_op:
        batch_op.alter_column('pemesanan_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaksi', schema=None) as batch_op:
        batch_op.alter_column('pemesanan_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
