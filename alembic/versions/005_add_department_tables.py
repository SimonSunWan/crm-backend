"""Add department tables

Revision ID: 005_add_department_tables
Revises: 004_revert_repair_progress_to_fault_location
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005_add_department_tables'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """创建部门相关表"""
    # 部门表
    op.create_table(
        'department',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dept_name', sa.String(100), nullable=False, comment='部门名称'),
        sa.Column('dept_code', sa.String(50), nullable=False, comment='部门编码'),
        sa.Column('parent_id', sa.Integer(), nullable=True, comment='父部门ID'),
        sa.Column('level', sa.Integer(), default=1, nullable=True, comment='部门层级'),
        sa.Column('path', sa.String(500), nullable=True, comment='部门路径'),
        sa.Column('sort_order', sa.Integer(), default=0, nullable=True, comment='排序'),
        sa.Column('leader_id', sa.Integer(), nullable=True, comment='部门负责人ID'),
        sa.Column('status', sa.Boolean(), default=True, nullable=True, comment='启用状态'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('created_by', sa.String(100), nullable=True, comment='创建者'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.ForeignKeyConstraint(['leader_id'], ['user.id']),
        sa.ForeignKeyConstraint(['parent_id'], ['department.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index(op.f('ix_department_id'), 'department', ['id'], unique=False)
    op.create_index(op.f('ix_department_dept_code'), 'department', ['dept_code'], unique=True)

    # 用户部门关联表
    op.create_table(
        'user_department',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('dept_id', sa.Integer(), nullable=False),
        sa.Column('join_date', sa.String(20), nullable=True, comment='加入部门日期'),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=True, comment='是否在职'),
        sa.ForeignKeyConstraint(['dept_id'], ['department.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'dept_id')
    )


def downgrade() -> None:
    """删除部门相关表"""
    op.drop_table('user_department')
    op.drop_table('department')
