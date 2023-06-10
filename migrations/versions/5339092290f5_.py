"""empty message

Revision ID: 5339092290f5
Revises: 6088b899e9a5
Create Date: 2023-05-13 11:20:46.644106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5339092290f5'
down_revision = '6088b899e9a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mobil_dipinjam', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pemesanan_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'pemesanan', ['pemesanan_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mobil_dipinjam', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('pemesanan_id')

    # ### end Alembic commands ###
