"""empty message

Revision ID: 3e5f39b50490
Revises: daee99a31248
Create Date: 2023-05-13 16:46:10.003471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e5f39b50490'
down_revision = 'daee99a31248'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mobil_disewa', schema=None) as batch_op:
        batch_op.alter_column('tgl_sewa',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('tgl_kembali',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mobil_disewa', schema=None) as batch_op:
        batch_op.alter_column('tgl_kembali',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('tgl_sewa',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
