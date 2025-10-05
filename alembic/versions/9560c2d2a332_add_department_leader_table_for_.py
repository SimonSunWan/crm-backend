"""add department_leader table for multiple leaders support

Revision ID: 9560c2d2a332
Revises: 27c7fdac2caf
Create Date: 2025-10-05 10:57:16.074153

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9560c2d2a332'
down_revision = '27c7fdac2caf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """添加部门负责人关联表，支持多负责人"""
    # 创建部门负责人关联表
    op.create_table(
        'department_leader',
        sa.Column('dept_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=True, comment='是否为主要负责人'),
        sa.ForeignKeyConstraint(['dept_id'], ['department.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('dept_id', 'user_id')
    )
    
    # 迁移现有数据：将现有的leader_id数据迁移到新表
    op.execute("""
        INSERT INTO department_leader (dept_id, user_id, is_primary)
        SELECT id, leader_id, true
        FROM department 
        WHERE leader_id IS NOT NULL
    """)
    
    # 删除旧的leader_id列
    op.drop_column('department', 'leader_id')


def downgrade() -> None:
    """回滚：恢复单负责人模式"""
    # 重新添加leader_id列
    op.add_column('department', sa.Column('leader_id', sa.Integer(), nullable=True, comment='部门负责人ID'))
    
    # 迁移数据：将主要负责人数据迁移回leader_id列
    op.execute("""
        UPDATE department 
        SET leader_id = (
            SELECT user_id 
            FROM department_leader 
            WHERE department_leader.dept_id = department.id 
            AND is_primary = true 
            LIMIT 1
        )
    """)
    
    # 添加外键约束
    op.create_foreign_key('department_leader_id_fkey', 'department', 'user', ['leader_id'], ['id'])
    
    # 删除部门负责人关联表
    op.drop_table('department_leader')
