"""empty message

Revision ID: 95ea9655388f
Revises: b414ca393731
Create Date: 2023-05-27 15:47:28.628501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95ea9655388f'
down_revision = 'b414ca393731'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_transaksi')
    with op.batch_alter_table('transaksi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tgl_sewa', sa.DateTime(), nullable=True))
        batch_op.drop_column('tanggal_transaksi')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaksi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tanggal_transaksi', sa.DATETIME(), nullable=False))
        batch_op.drop_column('tgl_sewa')

    op.create_table('_alembic_tmp_transaksi',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nama', sa.INTEGER(), nullable=False),
    sa.Column('metode_pembayaran', sa.VARCHAR(length=20), nullable=False),
    sa.Column('total_biaya', sa.INTEGER(), nullable=False),
    sa.Column('denda', sa.INTEGER(), nullable=True),
    sa.Column('pemesanan_id', sa.INTEGER(), nullable=False),
    sa.Column('tgl_kembali', sa.DATETIME(), nullable=True),
    sa.Column('harga_sewa', sa.INTEGER(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('denda_per_hari', sa.INTEGER(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('jumlah_hari', sa.INTEGER(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('dp', sa.INTEGER(), nullable=True),
    sa.Column('tgl_sewa', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['pemesanan_id'], ['pemesanan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
