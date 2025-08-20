"""add_user_role_association_table

Revision ID: 1a5d49a84516
Revises: 6f957fb6102d
Create Date: 2025-08-20 15:46:35.209885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a5d49a84516'
down_revision = '6f957fb6102d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建用户角色关联表
    op.create_table('user_role',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    
    # 删除users表中的roles数组字段
    op.drop_column('users', 'roles')


def downgrade() -> None:
    # 恢复users表中的roles数组字段
    op.add_column('users', sa.Column('roles', sa.ARRAY(sa.String()), nullable=True))
    
    # 删除用户角色关联表
    op.drop_table('user_role')
