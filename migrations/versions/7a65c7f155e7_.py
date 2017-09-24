"""empty message

Revision ID: 7a65c7f155e7
Revises: a969b13a85fd
Create Date: 2017-09-22 22:23:14.909253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a65c7f155e7'
down_revision = 'a969b13a85fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('alert_time', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('phone', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone')
    op.drop_column('event', 'alert_time')
    # ### end Alembic commands ###