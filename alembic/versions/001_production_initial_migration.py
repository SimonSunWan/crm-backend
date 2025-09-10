"""Production initial migration - Revision ID: 001_production_initial"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_production_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('user_name', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('avatar', sa.String(), nullable=True),
        sa.Column('status', sa.Boolean(), nullable=True),
        sa.Column('roles', sa.Text(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_user_name'), 'users', ['user_name'], unique=True)

    # Roles table
    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('role_name', sa.String(), nullable=False),
        sa.Column('role_code', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.Boolean(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=False)
    op.create_index(op.f('ix_roles_role_code'), 'roles', ['role_code'], unique=True)
    op.create_index(op.f('ix_roles_role_name'), 'roles', ['role_name'], unique=True)

    # Menus table
    op.create_table('menus',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False, comment='菜单名称'),
        sa.Column('path', sa.String(length=200), nullable=True, comment='路由地址'),
        sa.Column('component', sa.String(length=200), nullable=True, comment='组件路径'),
        sa.Column('redirect', sa.String(length=200), nullable=True, comment='重定向地址'),
        sa.Column('title', sa.String(length=100), nullable=False, comment='菜单标题'),
        sa.Column('icon', sa.String(length=100), nullable=True, comment='菜单图标'),
        sa.Column('sort', sa.Integer(), nullable=True, comment='排序'),
        sa.Column('is_hide', sa.Boolean(), nullable=True, comment='是否隐藏'),
        sa.Column('is_keep_alive', sa.Boolean(), nullable=True, comment='是否缓存'),
        sa.Column('is_link', sa.Boolean(), nullable=True, comment='是否外链'),
        sa.Column('link', sa.String(length=500), nullable=True, comment='外链地址'),
        sa.Column('is_enable', sa.Boolean(), nullable=True, comment='是否启用'),
        sa.Column('menu_type', sa.String(length=20), nullable=True, comment='菜单类型'),
        sa.Column('parent_id', sa.Integer(), nullable=True, comment='父级ID'),
        sa.Column('auth_mark', sa.String(length=100), nullable=True, comment='权限标识'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['menus.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menus_id'), 'menus', ['id'], unique=False)
    op.create_index(op.f('ix_menus_name'), 'menus', ['name'], unique=True)
    op.create_index(op.f('ix_menus_path'), 'menus', ['path'], unique=False)

    # Dictionary types table
    op.create_table('dic_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False, comment='字典类型名称'),
        sa.Column('code', sa.String(), nullable=False, comment='字典类型编码'),
        sa.Column('description', sa.String(), nullable=True, comment='字典类型描述'),
        sa.Column('status', sa.Boolean(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dic_types_code'), 'dic_types', ['code'], unique=True)
    op.create_index(op.f('ix_dic_types_id'), 'dic_types', ['id'], unique=False)
    op.create_index(op.f('ix_dic_types_name'), 'dic_types', ['name'], unique=True)

    # Dictionary enums table
    op.create_table('dic_enums',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=False, comment='字典类型ID'),
        sa.Column('key_value', sa.String(), nullable=False, comment='键值'),
        sa.Column('dict_value', sa.String(), nullable=False, comment='字典值'),
        sa.Column('sort_order', sa.Integer(), nullable=True, comment='排序'),
        sa.Column('status', sa.Boolean(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['type_id'], ['dic_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dic_enums_id'), 'dic_enums', ['id'], unique=False)

    # System settings table
    op.create_table('system_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('setting_key', sa.String(), nullable=False),
        sa.Column('setting_value', sa.Text(), nullable=False),
        sa.Column('setting_name', sa.String(), nullable=False),
        sa.Column('setting_desc', sa.String(), nullable=True),
        sa.Column('setting_type', sa.String(), nullable=True),
        sa.Column('status', sa.Boolean(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_system_settings_id'), 'system_settings', ['id'], unique=False)
    op.create_index(op.f('ix_system_settings_setting_key'), 'system_settings', ['setting_key'], unique=True)

    # Internal orders table
    op.create_table('internal_orders',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('customer', sa.String(), nullable=False),
        sa.Column('vehicle_model', sa.String(), nullable=False),
        sa.Column('repair_shop', sa.String(), nullable=False),
        sa.Column('reporter_name', sa.String(), nullable=False),
        sa.Column('contact_info', sa.String(), nullable=False),
        sa.Column('report_date', sa.Date(), nullable=False),
        sa.Column('project_type', sa.String(), nullable=False),
        sa.Column('project_stage', sa.String(), nullable=False),
        sa.Column('license_plate', sa.String(), nullable=True),
        sa.Column('vin_number', sa.String(), nullable=False),
        sa.Column('mileage', sa.Float(), nullable=True),
        sa.Column('vehicle_location', sa.Text(), nullable=True),
        sa.Column('vehicle_date', sa.Date(), nullable=True),
        sa.Column('pack_code', sa.String(), nullable=True),
        sa.Column('pack_date', sa.Date(), nullable=True),
        sa.Column('under_warranty', sa.Boolean(), nullable=True),
        sa.Column('fault_description', sa.Text(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_internal_orders_id'), 'internal_orders', ['id'], unique=False)

    # External orders table
    op.create_table('external_orders',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('customer', sa.String(), nullable=False),
        sa.Column('vehicle_model', sa.String(), nullable=False),
        sa.Column('repair_shop', sa.String(), nullable=False),
        sa.Column('reporter_name', sa.String(), nullable=False),
        sa.Column('contact_info', sa.String(), nullable=False),
        sa.Column('report_date', sa.Date(), nullable=False),
        sa.Column('project_type', sa.String(), nullable=False),
        sa.Column('project_stage', sa.String(), nullable=False),
        sa.Column('license_plate', sa.String(), nullable=True),
        sa.Column('vin_number', sa.String(), nullable=False),
        sa.Column('mileage', sa.Float(), nullable=True),
        sa.Column('vehicle_location', sa.Text(), nullable=True),
        sa.Column('vehicle_date', sa.Date(), nullable=True),
        sa.Column('pack_code', sa.String(), nullable=True),
        sa.Column('pack_date', sa.Date(), nullable=True),
        sa.Column('under_warranty', sa.Boolean(), nullable=True),
        sa.Column('fault_description', sa.Text(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_external_orders_id'), 'external_orders', ['id'], unique=False)

    # Internal order details table
    op.create_table('internal_order_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=False),
        sa.Column('repair_person', sa.String(), nullable=True),
        sa.Column('repair_date', sa.Date(), nullable=True),
        sa.Column('avic_responsibility', sa.Boolean(), nullable=True),
        sa.Column('fault_classification', sa.String(), nullable=True),
        sa.Column('fault_location', sa.String(), nullable=True),
        sa.Column('part_category', sa.String(), nullable=True),
        sa.Column('part_location', sa.String(), nullable=True),
        sa.Column('repair_description', sa.Text(), nullable=True),
        sa.Column('spare_part_location', sa.String(), nullable=True),
        sa.Column('spare_parts', sa.JSON(), nullable=True),
        sa.Column('costs', sa.JSON(), nullable=True),
        sa.Column('labors', sa.JSON(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['order_id'], ['internal_orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_internal_order_details_id'), 'internal_order_details', ['id'], unique=False)
    op.create_index(op.f('ix_internal_order_details_order_id'), 'internal_order_details', ['order_id'], unique=False)

    # External order details table
    op.create_table('external_order_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=False),
        sa.Column('repair_person', sa.String(), nullable=True),
        sa.Column('repair_date', sa.Date(), nullable=True),
        sa.Column('avic_responsibility', sa.Boolean(), nullable=True),
        sa.Column('fault_classification', sa.String(), nullable=True),
        sa.Column('fault_location', sa.String(), nullable=True),
        sa.Column('part_category', sa.String(), nullable=True),
        sa.Column('part_location', sa.String(), nullable=True),
        sa.Column('repair_description', sa.Text(), nullable=True),
        sa.Column('spare_part_location', sa.String(), nullable=True),
        sa.Column('spare_parts', sa.JSON(), nullable=True),
        sa.Column('costs', sa.JSON(), nullable=True),
        sa.Column('labors', sa.JSON(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['order_id'], ['external_orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_external_order_details_id'), 'external_order_details', ['id'], unique=False)
    op.create_index(op.f('ix_external_order_details_order_id'), 'external_order_details', ['order_id'], unique=False)

    # User role association table
    op.create_table('user_role',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )

    # Role menu association table
    op.create_table('role_menu',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('menu_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('role_id', 'menu_id')
    )


def downgrade() -> None:
    op.drop_table('role_menu')
    op.drop_table('user_role')
    op.drop_table('external_order_details')
    op.drop_table('internal_order_details')
    op.drop_table('external_orders')
    op.drop_table('internal_orders')
    op.drop_table('system_settings')
    op.drop_table('dic_enums')
    op.drop_table('dic_types')
    op.drop_table('menus')
    op.drop_table('roles')
    op.drop_table('users')
