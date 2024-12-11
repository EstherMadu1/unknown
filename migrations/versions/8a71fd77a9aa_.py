"""empty message

Revision ID: 8a71fd77a9aa
Revises: b0edb7d4f81e
Create Date: 2024-12-10 04:46:14.355267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a71fd77a9aa'
down_revision = 'b0edb7d4f81e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('farmers', schema=None) as batch_op:
        batch_op.alter_column('date_registered',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               nullable=True)

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('order_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               nullable=True)

    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.alter_column('date_paid',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.alter_column('date_paid',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               nullable=False)

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('order_date',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               nullable=False)

    with op.batch_alter_table('farmers', schema=None) as batch_op:
        batch_op.alter_column('date_registered',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               nullable=False)

    # ### end Alembic commands ###
