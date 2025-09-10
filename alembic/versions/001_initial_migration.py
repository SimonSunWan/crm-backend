"""Initial migration - Revision ID: 001_initial_migration"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # User table
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('user_name', sa.String(), nullable=False),
        sa.Column('nick_name', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('avatar', sa.String(), nullable=True),
        sa.Column('status', sa.Boolean(), default=True, nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_user_name'), 'user', ['user_name'], unique=True)

    # Role table
    op.create_table('role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('role_name', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('role_code', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Boolean(), default=True, nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_id'), 'role', ['id'], unique=False)
    op.create_index(op.f('ix_role_role_code'), 'role', ['role_code'], unique=True)
    op.create_index(op.f('ix_role_role_name'), 'role', ['role_name'], unique=True)

    # Menu table
    op.create_table('menu',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('path', sa.String(200), nullable=True),
        sa.Column('icon', sa.String(100), nullable=True),
        sa.Column('sort', sa.Integer(), default=1, nullable=True),
        sa.Column('is_hide', sa.Boolean(), default=False, nullable=True),
        sa.Column('is_keep_alive', sa.Boolean(), default=True, nullable=True),
        sa.Column('is_link', sa.Boolean(), default=False, nullable=True),
        sa.Column('link', sa.String(500), nullable=True),
        sa.Column('is_enable', sa.Boolean(), default=True, nullable=True),
        sa.Column('menu_type', sa.String(20), default='menu', nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('auth_mark', sa.String(100), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['menu.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menu_id'), 'menu', ['id'], unique=False)
    op.create_index(op.f('ix_menu_name'), 'menu', ['name'], unique=True)
    op.create_index(op.f('ix_menu_path'), 'menu', ['path'], unique=False)

    # Dictionary type table
    op.create_table('dic_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('code', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.Boolean(), default=True, nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dic_type_code'), 'dic_type', ['code'], unique=True)
    op.create_index(op.f('ix_dic_type_id'), 'dic_type', ['id'], unique=False)
    op.create_index(op.f('ix_dic_type_name'), 'dic_type', ['name'], unique=True)

    # Dictionary enum table
    op.create_table('dic_enum',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('key_value', sa.String(), nullable=False),
        sa.Column('dict_value', sa.String(), nullable=False),
        sa.Column('sort_order', sa.Integer(), default=0, nullable=True),
        sa.Column('level', sa.Integer(), default=1, nullable=True),
        sa.Column('path', sa.String(), nullable=True),
        sa.Column('status', sa.Boolean(), default=True, nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(['type_id'], ['dic_type.id'], ),
        sa.ForeignKeyConstraint(['parent_id'], ['dic_enum.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dic_enum_id'), 'dic_enum', ['id'], unique=False)

    # System setting table
    op.create_table('system_setting',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('setting_key', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('setting_value', sa.String(), nullable=False),
        sa.Column('setting_name', sa.String(), nullable=False),
        sa.Column('setting_desc', sa.String(), nullable=True),
        sa.Column('status', sa.Boolean(), default=True, nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_system_setting_id'), 'system_setting', ['id'], unique=False)
    op.create_index(op.f('ix_system_setting_setting_key'), 'system_setting', ['setting_key'], unique=True)

    # Internal order table
    op.create_table('internal_order',
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
        sa.Column('mileage', sa.Float(), default=0.0, nullable=True),
        sa.Column('vehicle_location', sa.Text(), nullable=True),
        sa.Column('vehicle_date', sa.Date(), nullable=True),
        sa.Column('pack_code', sa.String(), nullable=True),
        sa.Column('pack_date', sa.Date(), nullable=True),
        sa.Column('under_warranty', sa.Boolean(), default=True, nullable=True),
        sa.Column('fault_description', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_internal_order_id'), 'internal_order', ['id'], unique=False)

    # External order table
    op.create_table('external_order',
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
        sa.Column('mileage', sa.Float(), default=0.0, nullable=True),
        sa.Column('vehicle_location', sa.Text(), nullable=True),
        sa.Column('vehicle_date', sa.Date(), nullable=True),
        sa.Column('pack_code', sa.String(), nullable=True),
        sa.Column('pack_date', sa.Date(), nullable=True),
        sa.Column('under_warranty', sa.Boolean(), default=False, nullable=True),
        sa.Column('fault_description', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_external_order_id'), 'external_order', ['id'], unique=False)

    # Internal order detail table
    op.create_table('internal_order_detail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=False),
        sa.Column('repair_person', sa.String(), nullable=True),
        sa.Column('repair_date', sa.Date(), nullable=True),
        sa.Column('avic_responsibility', sa.Boolean(), default=True, nullable=True),
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
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(['order_id'], ['internal_order.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_internal_order_detail_id'), 'internal_order_detail', ['id'], unique=False)
    op.create_index(op.f('ix_internal_order_detail_order_id'), 'internal_order_detail', ['order_id'], unique=False)

    # External order detail table
    op.create_table('external_order_detail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=False),
        sa.Column('repair_person', sa.String(), nullable=True),
        sa.Column('repair_date', sa.Date(), nullable=True),
        sa.Column('avic_responsibility', sa.Boolean(), default=False, nullable=True),
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
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True),
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
