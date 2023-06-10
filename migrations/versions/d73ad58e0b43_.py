"""empty message

Revision ID: d73ad58e0b43
Revises: 64205da3ad17
Create Date: 2023-05-17 00:29:26.528593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd73ad58e0b43'
down_revision = '64205da3ad17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mobil', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nomor_plat', sa.String(length=10), nullable=True))

    with op.batch_alter_table('pemesanan', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nomor_plat', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pemesanan', schema=None) as batch_op:
        batch_op.drop_column('nomor_plat')

    with op.batch_alter_table('mobil', schema=None) as batch_op:
        batch_op.drop_column('nomor_plat')

    # ### end Alembic commands ###
