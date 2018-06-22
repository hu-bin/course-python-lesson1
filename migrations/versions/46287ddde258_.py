"""empty message

Revision ID: 46287ddde258
Revises: 170ad42e94eb
Create Date: 2018-06-21 03:46:44.201702

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '46287ddde258'
down_revision = '170ad42e94eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department_permission',
    sa.Column('id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('department_id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('permission_id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('leader_only', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('department_tree',
    sa.Column('id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('parent_path', mysql.VARCHAR(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employee_department',
    sa.Column('employee_id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('department_id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.PrimaryKeyConstraint('employee_id')
    )
    op.add_column('department', sa.Column('name', mysql.VARCHAR(length=64), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('department', 'name')
    op.drop_table('employee_department')
    op.drop_table('department_tree')
    op.drop_table('department_permission')
    # ### end Alembic commands ###
