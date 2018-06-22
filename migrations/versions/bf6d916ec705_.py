"""empty message

Revision ID: bf6d916ec705
Revises: 47a82dc799a6
Create Date: 2018-06-22 06:07:37.276508

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bf6d916ec705'
down_revision = '47a82dc799a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test_charset')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_charset',
    sa.Column('id', mysql.BIGINT(display_width=20, unsigned=True), nullable=False),
    sa.Column('something', mysql.VARCHAR(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
