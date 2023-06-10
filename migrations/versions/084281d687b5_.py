"""empty message

Revision ID: 084281d687b5
Revises: e05c66472cd5
Create Date: 2023-06-09 22:14:30.460077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '084281d687b5'
down_revision = 'e05c66472cd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mobil_disewa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('search_term', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mobil_disewa', schema=None) as batch_op:
        batch_op.drop_column('search_term')

    # ### end Alembic commands ###
