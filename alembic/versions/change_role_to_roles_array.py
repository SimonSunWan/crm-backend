"""change role to roles array field

Revision ID: change_role_to_roles_array
Revises: abe24ca26c78
Create Date: 2025-01-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'change_role_to_roles_array'
down_revision = 'abe24ca26c78'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. 添加新的 roles 列
    op.add_column('users', sa.Column('roles', postgresql.ARRAY(sa.String()), nullable=True))
    
    # 2. 迁移现有数据：将 role 字段的值转换为 roles 数组
    connection = op.get_bind()
    users = connection.execute(sa.text("SELECT id, role FROM users WHERE role IS NOT NULL"))
    
    for user in users:
        if user.role:
            # 将单个角色转换为数组格式
            roles_array = [user.role]
            connection.execute(
                sa.text("UPDATE users SET roles = :roles WHERE id = :id"),
                {"roles": roles_array, "id": user.id}
            )
    
    # 3. 删除旧的 role 列
    op.drop_column('users', 'role')


def downgrade() -> None:
    # 1. 重新添加 role 列
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))
    
    # 2. 迁移数据：将 roles 数组的第一个值作为 role
    connection = op.get_bind()
    users = connection.execute(sa.text("SELECT id, roles FROM users WHERE roles IS NOT NULL"))
    
    for user in users:
        if user.roles and len(user.roles) > 0:
            # 取数组中的第一个角色
            first_role = user.roles[0]
            connection.execute(
                sa.text("UPDATE users SET role = :role WHERE id = :id"),
                {"role": first_role, "id": user.id}
            )
    
    # 3. 删除 roles 列
    op.drop_column('users', 'roles')
