"""优化菜单表结构：删除冗余字段，新增is_link字段

Revision ID: c293cfa96ab9
Revises: 5dcf4c45a68f
Create Date: 2025-09-06 08:50:17.884852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c293cfa96ab9'
down_revision = '5dcf4c45a68f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加新字段 is_link
    op.add_column('menus', sa.Column('is_link', sa.Boolean(), nullable=False, server_default='false', comment='是否外链'))
    
    # 删除不需要的字段
    op.drop_column('menus', 'component')
    op.drop_column('menus', 'redirect')
    op.drop_column('menus', 'title')
    op.drop_column('menus', 'is_iframe')
    op.drop_column('menus', 'auth_sort')
    op.drop_column('menus', 'auth_name')


def downgrade() -> None:
    # 恢复删除的字段
    op.add_column('menus', sa.Column('auth_name', sa.String(100), nullable=True, comment='权限名称'))
    op.add_column('menus', sa.Column('auth_sort', sa.Integer(), nullable=True, comment='权限排序'))
    op.add_column('menus', sa.Column('is_iframe', sa.Boolean(), nullable=True, comment='是否内嵌'))
    op.add_column('menus', sa.Column('title', sa.String(100), nullable=False, comment='菜单标题'))
    op.add_column('menus', sa.Column('redirect', sa.String(200), nullable=True, comment='重定向地址'))
    op.add_column('menus', sa.Column('component', sa.String(200), nullable=True, comment='组件路径'))
    
    # 删除新添加的字段
    op.drop_column('menus', 'is_link')
