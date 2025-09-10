"""rename_tables_to_singular

Revision ID: 93c0df211b63
Revises: 001_production_initial
Create Date: 2025-09-10 17:02:02.541663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93c0df211b63'
down_revision = '001_production_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 重命名表名从复数到单数
    op.rename_table('users', 'user')
    op.rename_table('roles', 'role')
    op.rename_table('menus', 'menu')
    op.rename_table('system_settings', 'system_setting')
    op.rename_table('internal_orders', 'internal_order')
    op.rename_table('internal_order_details', 'internal_order_detail')
    op.rename_table('external_orders', 'external_order')
    op.rename_table('external_order_details', 'external_order_detail')
    
    # 更新外键约束
    # 更新 menu 表的外键
    op.drop_constraint('fk_menu_parent', 'menu', type_='foreignkey')
    op.create_foreign_key('fk_menu_parent', 'menu', 'menu', ['parent_id'], ['id'])
    
    # 更新 external_order_detail 表的外键
    op.drop_constraint('external_order_details_order_id_fkey', 'external_order_detail', type_='foreignkey')
    op.create_foreign_key('external_order_detail_order_id_fkey', 'external_order_detail', 'external_order', ['order_id'], ['id'])


def downgrade() -> None:
    # 恢复外键约束到原来的表名
    # 恢复 external_order_detail 表的外键
    op.drop_constraint('external_order_detail_order_id_fkey', 'external_order_detail', type_='foreignkey')
    op.create_foreign_key('external_order_details_order_id_fkey', 'external_order_detail', 'external_orders', ['order_id'], ['id'])
    
    # 恢复 menu 表的外键
    op.drop_constraint('fk_menu_parent', 'menu', type_='foreignkey')
    op.create_foreign_key('fk_menu_parent', 'menu', 'menus', ['parent_id'], ['id'])
    
    # 重命名表名从单数回到复数
    op.rename_table('external_order_detail', 'external_order_details')
    op.rename_table('external_order', 'external_orders')
    op.rename_table('internal_order_detail', 'internal_order_details')
    op.rename_table('internal_order', 'internal_orders')
    op.rename_table('system_setting', 'system_settings')
    op.rename_table('menu', 'menus')
    op.rename_table('role', 'roles')
    op.rename_table('user', 'users')
