"""Add foreign key constraints

Revision ID: 002_add_foreign_keys
Revises: 93c0df211b63
Create Date: 2025-01-27 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_add_foreign_keys'
down_revision = '93c0df211b63'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """添加外键约束"""
    
    # 为user_role关联表添加外键约束
    op.create_foreign_key(
        'fk_user_role_user_id',
        'user_role',
        'user',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )
    
    op.create_foreign_key(
        'fk_user_role_role_id',
        'user_role',
        'role',
        ['role_id'],
        ['id'],
        ondelete='CASCADE'
    )
    
    # 为role_menu关联表添加外键约束
    op.create_foreign_key(
        'fk_role_menu_role_id',
        'role_menu',
        'role',
        ['role_id'],
        ['id'],
        ondelete='CASCADE'
    )
    
    op.create_foreign_key(
        'fk_role_menu_menu_id',
        'role_menu',
        'menu',
        ['menu_id'],
        ['id'],
        ondelete='CASCADE'
    )
    
    # 为internal_order添加created_by外键约束
    op.create_foreign_key(
        'fk_internal_order_created_by',
        'internal_order',
        'user',
        ['created_by'],
        ['id'],
        ondelete='SET NULL'
    )
    
    # 为external_order添加created_by外键约束
    op.create_foreign_key(
        'fk_external_order_created_by',
        'external_order',
        'user',
        ['created_by'],
        ['id'],
        ondelete='SET NULL'
    )
    
    # 为internal_order_detail添加order_id外键约束
    op.create_foreign_key(
        'fk_internal_order_detail_order_id',
        'internal_order_detail',
        'internal_order',
        ['order_id'],
        ['id'],
        ondelete='CASCADE'
    )
    
    # 为external_order_detail添加order_id外键约束
    op.create_foreign_key(
        'fk_external_order_detail_order_id',
        'external_order_detail',
        'external_order',
        ['order_id'],
        ['id'],
        ondelete='CASCADE'
    )
    
    # 为dic_enum添加type_id外键约束
    op.create_foreign_key(
        'fk_dic_enum_type_id',
        'dic_enum',
        'dic_type',
        ['type_id'],
        ['id'],
        ondelete='CASCADE'
    )
    
    # 为dic_enum添加parent_id外键约束（自引用）
    op.create_foreign_key(
        'fk_dic_enum_parent_id',
        'dic_enum',
        'dic_enum',
        ['parent_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """删除外键约束"""
    
    # 删除所有添加的外键约束
    op.drop_constraint('fk_dic_enum_parent_id', 'dic_enum', type_='foreignkey')
    op.drop_constraint('fk_dic_enum_type_id', 'dic_enum', type_='foreignkey')
    op.drop_constraint('fk_external_order_detail_order_id', 'external_order_detail', type_='foreignkey')
    op.drop_constraint('fk_internal_order_detail_order_id', 'internal_order_detail', type_='foreignkey')
    op.drop_constraint('fk_external_order_created_by', 'external_order', type_='foreignkey')
    op.drop_constraint('fk_internal_order_created_by', 'internal_order', type_='foreignkey')
    op.drop_constraint('fk_role_menu_menu_id', 'role_menu', type_='foreignkey')
    op.drop_constraint('fk_role_menu_role_id', 'role_menu', type_='foreignkey')
    op.drop_constraint('fk_user_role_role_id', 'user_role', type_='foreignkey')
    op.drop_constraint('fk_user_role_user_id', 'user_role', type_='foreignkey')
