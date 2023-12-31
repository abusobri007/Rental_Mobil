"""empty message

Revision ID: b02bf8fa96e7
Revises: 05e6b0be8822
Create Date: 2023-06-12 10:41:50.873048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b02bf8fa96e7'
down_revision = '05e6b0be8822'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirm_password', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('confirm_password')

    # ### end Alembic commands ###
