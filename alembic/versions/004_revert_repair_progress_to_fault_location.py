"""revert repair_progress to fault_location

Revision ID: 004
Revises: 003
Create Date: 2025-01-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003_update_external_order_fields'
branch_labels = None
depends_on = None


def upgrade():
    # 将 repair_progress 字段重命名为 fault_location
    op.alter_column('external_order_detail', 'repair_progress', new_column_name='fault_location', comment='故障位置')


def downgrade():
    # 将 fault_location 字段重命名为 repair_progress
    op.alter_column('external_order_detail', 'fault_location', new_column_name='repair_progress', comment='维修进度')
