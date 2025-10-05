"""remove dept_code field from department table

Revision ID: 27c7fdac2caf
Revises: 47fec55e9467
Create Date: 2025-10-05 10:29:39.467347

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '27c7fdac2caf'
down_revision = '47fec55e9467'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """删除部门编码字段"""
    # 删除部门编码字段的索引
    op.drop_index('ix_department_dept_code', table_name='department')
    
    # 删除部门编码字段
    op.drop_column('department', 'dept_code')


def downgrade() -> None:
    """回滚：恢复部门编码字段"""
    # 重新添加部门编码字段
    op.add_column('department', sa.Column('dept_code', sa.VARCHAR(length=50), nullable=False, comment='部门编码'))
    
    # 重新创建部门编码字段的索引
    op.create_index('ix_department_dept_code', 'department', ['dept_code'], unique=True)
