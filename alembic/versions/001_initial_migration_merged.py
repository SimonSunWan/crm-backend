"""Initial migration - Complete database schema

Revision ID: 001_initial_migration_merged
Revises: None
Create Date: 2025-01-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial_migration_merged'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """创建所有数据库表"""
    
    # User table
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_name', sa.String(), nullable=False, comment='用户名'),
        sa.Column('nick_name', sa.String(), nullable=True, comment='昵称'),
        sa.Column('phone', sa.String(), nullable=True, comment='手机号'),
        sa.Column('email', sa.String(), nullable=True, comment='邮箱'),
        sa.Column('avatar', sa.String(), nullable=True, comment='头像'),
        sa.Column('status', sa.Boolean(), default=True, nullable=True, comment='状态'),
        sa.Column('hashed_password', sa.String(), nullable=False, comment='密码'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('created_by', sa.String(100), nullable=True, comment='创建者'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_user_name'), 'user', ['user_name'], unique=True)

    # Role table
    op.create_table('role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('role_name', sa.String(50), nullable=False, comment='角色名称'),
        sa.Column('role_code', sa.String(50), nullable=False, comment='角色编码'),
        sa.Column('description', sa.Text(), nullable=True, comment='角色描述'),
        sa.Column('status', sa.Boolean(), default=True, nullable=True, comment='启用状态'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('created_by', sa.String(100), nullable=True, comment='创建者'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_id'), 'role', ['id'], unique=False)
    op.create_index(op.f('ix_role_role_code'), 'role', ['role_code'], unique=True)
    op.create_index(op.f('ix_role_role_name'), 'role', ['role_name'], unique=True)

    # Menu table
    op.create_table('menu',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False, comment='菜单名称'),
        sa.Column('path', sa.String(200), nullable=True, comment='路由地址'),
        sa.Column('icon', sa.String(100), nullable=True, comment='菜单图标'),
        sa.Column('sort', sa.Integer(), default=1, nullable=True, comment='菜单排序'),
        sa.Column('is_hide', sa.Boolean(), default=False, nullable=True, comment='是否隐藏'),
        sa.Column('is_keep_alive', sa.Boolean(), default=True, nullable=True, comment='是否缓存'),
        sa.Column('is_link', sa.Boolean(), default=False, nullable=True, comment='是否外链'),
        sa.Column('link', sa.String(500), nullable=True, comment='外部链接'),
        sa.Column('is_enable', sa.Boolean(), default=True, nullable=True, comment='是否启用'),
        sa.Column('menu_type', sa.String(20), default='menu', nullable=True, comment='菜单类型：menu-菜单，button-权限'),
        sa.Column('parent_id', sa.Integer(), nullable=True, comment='父菜单ID'),
        sa.Column('auth_mark', sa.String(100), nullable=True, comment='权限标识'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('created_by', sa.String(100), nullable=True, comment='创建者'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.ForeignKeyConstraint(['parent_id'], ['menu.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menu_id'), 'menu', ['id'], unique=False)
    op.create_index(op.f('ix_menu_name'), 'menu', ['name'], unique=True)
    op.create_index(op.f('ix_menu_path'), 'menu', ['path'], unique=False)

    # Dictionary type table
    op.create_table('dic_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False, comment='字典类型名称'),
        sa.Column('code', sa.String(), nullable=False, comment='字典类型编码'),
        sa.Column('description', sa.String(), nullable=True, comment='字典类型描述'),
        sa.Column('status', sa.Boolean(), default=True, nullable=True, comment='状态'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('created_by', sa.String(100), nullable=True, comment='创建者'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dic_type_code'), 'dic_type', ['code'], unique=True)
    op.create_index(op.f('ix_dic_type_id'), 'dic_type', ['id'], unique=False)
    op.create_index(op.f('ix_dic_type_name'), 'dic_type', ['name'], unique=True)

    # Dictionary enum table
    op.create_table('dic_enum',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=False, comment='字典类型ID'),
        sa.Column('parent_id', sa.Integer(), nullable=True, comment='父级枚举ID'),
        sa.Column('key_value', sa.String(), nullable=False, comment='键值'),
        sa.Column('dict_value', sa.String(), nullable=False, comment='字典值'),
        sa.Column('sort_order', sa.Integer(), default=0, nullable=True, comment='排序'),
        sa.Column('level', sa.Integer(), default=1, nullable=True, comment='层级'),
        sa.Column('path', sa.String(), nullable=True, comment='路径'),
        sa.Column('status', sa.Boolean(), default=True, nullable=True, comment='状态'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('created_by', sa.String(100), nullable=True, comment='创建者'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.ForeignKeyConstraint(['type_id'], ['dic_type.id'], ),
        sa.ForeignKeyConstraint(['parent_id'], ['dic_enum.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dic_enum_id'), 'dic_enum', ['id'], unique=False)

    # System setting table
    op.create_table('system_setting',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('setting_key', sa.String(), nullable=False, comment='配置键'),
        sa.Column('setting_value', sa.String(), nullable=False, comment='配置值'),
        sa.Column('setting_name', sa.String(), nullable=False, comment='配置名称'),
        sa.Column('setting_desc', sa.String(), nullable=True, comment='配置描述'),
        sa.Column('status', sa.Boolean(), default=True, nullable=True, comment='状态'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('created_by', sa.String(100), nullable=True, comment='创建者'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_system_setting_id'), 'system_setting', ['id'], unique=False)
    op.create_index(op.f('ix_system_setting_setting_key'), 'system_setting', ['setting_key'], unique=True)

    # Internal order table
    op.create_table('internal_order',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('customer', sa.String(), nullable=False, comment='客户'),
        sa.Column('vehicle_model', sa.String(), nullable=False, comment='车型'),
        sa.Column('repair_shop', sa.String(), nullable=False, comment='修理厂'),
        sa.Column('reporter_name', sa.String(), nullable=False, comment='报告人'),
        sa.Column('contact_info', sa.String(), nullable=False, comment='联系方式'),
        sa.Column('report_date', sa.Date(), nullable=False, comment='报告日期'),
        sa.Column('project_type', sa.String(), nullable=False, comment='项目类型'),
        sa.Column('project_stage', sa.String(), nullable=False, comment='项目阶段'),
        sa.Column('license_plate', sa.String(), nullable=True, comment='车牌号'),
        sa.Column('vin_number', sa.String(), nullable=False, comment='VIN号'),
        sa.Column('mileage', sa.Float(), default=0.0, nullable=True, comment='里程'),
        sa.Column('vehicle_location', sa.Text(), nullable=True, comment='车辆位置'),
        sa.Column('vehicle_date', sa.Date(), nullable=True, comment='车辆日期'),
        sa.Column('pack_code', sa.String(), nullable=True, comment='包装代码'),
        sa.Column('pack_date', sa.Date(), nullable=True, comment='包装日期'),
        sa.Column('under_warranty', sa.Boolean(), default=True, nullable=True, comment='保修期内'),
        sa.Column('fault_description', sa.Text(), nullable=True, comment='故障描述'),
        sa.Column('created_by', sa.Integer(), nullable=True, comment='创建者ID'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_internal_order_id'), 'internal_order', ['id'], unique=False)

    # External order table
    op.create_table('external_order',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('customer', sa.String(), nullable=False, comment='客户'),
        sa.Column('vehicle_model', sa.String(), nullable=False, comment='车型'),
        sa.Column('repair_shop', sa.String(), nullable=False, comment='修理厂'),
        sa.Column('reporter_name', sa.String(), nullable=False, comment='报告人'),
        sa.Column('contact_info', sa.String(), nullable=False, comment='联系方式'),
        sa.Column('report_date', sa.Date(), nullable=False, comment='报告日期'),
        sa.Column('project_type', sa.String(), nullable=False, comment='项目类型'),
        sa.Column('project_stage', sa.String(), nullable=False, comment='项目阶段'),
        sa.Column('license_plate', sa.String(), nullable=True, comment='车牌号'),
        sa.Column('vin_number', sa.String(), nullable=False, comment='VIN号'),
        sa.Column('mileage', sa.Float(), default=0.0, nullable=True, comment='里程'),
        sa.Column('vehicle_location', sa.Text(), nullable=True, comment='车辆位置'),
        sa.Column('vehicle_date', sa.Date(), nullable=True, comment='车辆日期'),
        sa.Column('pack_code', sa.String(), nullable=True, comment='包装代码'),
        sa.Column('pack_date', sa.Date(), nullable=True, comment='包装日期'),
        sa.Column('under_warranty', sa.Boolean(), default=False, nullable=True, comment='保修期内'),
        sa.Column('fault_description', sa.Text(), nullable=True, comment='故障描述'),
        sa.Column('created_by', sa.Integer(), nullable=True, comment='创建者ID'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_external_order_id'), 'external_order', ['id'], unique=False)

    # Internal order detail table
    op.create_table('internal_order_detail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=False, comment='订单ID'),
        sa.Column('repair_person', sa.String(), nullable=True, comment='修理人员'),
        sa.Column('repair_date', sa.Date(), nullable=True, comment='修理日期'),
        sa.Column('avic_responsibility', sa.Boolean(), default=True, nullable=True, comment='AVIC责任'),
        sa.Column('fault_classification', sa.String(), nullable=True, comment='故障分类'),
        sa.Column('fault_location', sa.String(), nullable=True, comment='故障位置'),
        sa.Column('part_category', sa.String(), nullable=True, comment='零件类别'),
        sa.Column('part_location', sa.String(), nullable=True, comment='零件位置'),
        sa.Column('repair_description', sa.Text(), nullable=True, comment='修理描述'),
        sa.Column('spare_part_location', sa.String(), nullable=True, comment='备件位置'),
        sa.Column('spare_parts', sa.JSON(), nullable=True, comment='备件'),
        sa.Column('costs', sa.JSON(), nullable=True, comment='费用'),
        sa.Column('labors', sa.JSON(), nullable=True, comment='人工'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('created_by', sa.String(100), nullable=True, comment='创建者'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.ForeignKeyConstraint(['order_id'], ['internal_order.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_internal_order_detail_id'), 'internal_order_detail', ['id'], unique=False)
    op.create_index(op.f('ix_internal_order_detail_order_id'), 'internal_order_detail', ['order_id'], unique=False)

    # External order detail table
    op.create_table('external_order_detail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=False, comment='订单ID'),
        sa.Column('repair_person', sa.String(), nullable=True, comment='修理人员'),
        sa.Column('repair_date', sa.Date(), nullable=True, comment='修理日期'),
        sa.Column('avic_responsibility', sa.Boolean(), default=False, nullable=True, comment='AVIC责任'),
        sa.Column('fault_classification', sa.String(), nullable=True, comment='故障分类'),
        sa.Column('fault_location', sa.String(), nullable=True, comment='故障位置'),
        sa.Column('part_category', sa.String(), nullable=True, comment='零件类别'),
        sa.Column('part_location', sa.String(), nullable=True, comment='零件位置'),
        sa.Column('repair_description', sa.Text(), nullable=True, comment='修理描述'),
        sa.Column('spare_part_location', sa.String(), nullable=True, comment='备件位置'),
        sa.Column('spare_parts', sa.JSON(), nullable=True, comment='备件'),
        sa.Column('costs', sa.JSON(), nullable=True, comment='费用'),
        sa.Column('labors', sa.JSON(), nullable=True, comment='人工'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('created_by', sa.String(100), nullable=True, comment='创建者'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.ForeignKeyConstraint(['order_id'], ['external_order.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_external_order_detail_id'), 'external_order_detail', ['id'], unique=False)
    op.create_index(op.f('ix_external_order_detail_order_id'), 'external_order_detail', ['order_id'], unique=False)

    # User role association table
    op.create_table('user_role',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )

    # Role menu association table
    op.create_table('role_menu',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('menu_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('role_id', 'menu_id')
    )


def downgrade() -> None:
    """删除所有数据库表"""
    op.drop_table('role_menu')
    op.drop_table('user_role')
    op.drop_table('external_order_detail')
    op.drop_table('internal_order_detail')
    op.drop_table('external_order')
    op.drop_table('internal_order')
    op.drop_table('system_setting')
    op.drop_table('dic_enum')
    op.drop_table('dic_type')
    op.drop_table('menu')
    op.drop_table('role')
    op.drop_table('user')
