"""caca

Revision ID: 25cf200facff
Revises: 4646e2bec603
Create Date: 2024-11-12 13:20:48.264380

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '25cf200facff'
down_revision = '4646e2bec603'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.drop_column('ADD_special_instructions')

    with op.batch_alter_table('packages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('PCK_special_delivery_instructions', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('packages', schema=None) as batch_op:
        batch_op.drop_column('PCK_special_delivery_instructions')

    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ADD_special_instructions', mysql.VARCHAR(length=200), nullable=True))

    # ### end Alembic commands ###
