"""add create_by and update_by to menu table

Revision ID: add_create_by_update_by_to_menu
Revises: 
Create Date: 2024-01-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_create_by_update_by_to_menu'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 添加 create_by 和 update_by 字段
    op.add_column('menus', sa.Column('create_by', sa.String(255), nullable=True, comment='创建者'))
    op.add_column('menus', sa.Column('update_by', sa.String(255), nullable=True, comment='更新者'))


def downgrade():
    # 删除添加的字段
    op.drop_column('menus', 'update_by')
    op.drop_column('menus', 'create_by')
