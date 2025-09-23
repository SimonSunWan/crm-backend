"""update_external_order_fields

Revision ID: 003_update_external_order_fields
Revises: 002_add_seal_code_to_orders
Create Date: 2025-09-23 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003_update_external_order_fields'
down_revision = '002_add_seal_code_to_orders'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 修改external_order表
    op.add_column('external_order', sa.Column('insurer', sa.String(), nullable=False, server_default=''))
    op.add_column('external_order', sa.Column('assessor', sa.String(), nullable=False, server_default=''))
    op.drop_column('external_order', 'project_type')
    op.drop_column('external_order', 'project_stage')
    
    # 修改external_order_detail表
    op.add_column('external_order_detail', sa.Column('repair_progress', sa.String(), nullable=True))
    op.drop_column('external_order_detail', 'fault_classification')
    op.drop_column('external_order_detail', 'fault_location')
    op.drop_column('external_order_detail', 'part_category')
    op.drop_column('external_order_detail', 'part_location')


def downgrade() -> None:
    # 恢复external_order表
    op.add_column('external_order', sa.Column('project_type', sa.String(), nullable=False, server_default=''))
    op.add_column('external_order', sa.Column('project_stage', sa.String(), nullable=False, server_default=''))
    op.drop_column('external_order', 'assessor')
    op.drop_column('external_order', 'insurer')
    
    # 恢复external_order_detail表
    op.add_column('external_order_detail', sa.Column('part_location', sa.String(), nullable=True))
    op.add_column('external_order_detail', sa.Column('part_category', sa.String(), nullable=True))
    op.add_column('external_order_detail', sa.Column('fault_location', sa.String(), nullable=True))
    op.add_column('external_order_detail', sa.Column('fault_classification', sa.String(), nullable=True))
    op.drop_column('external_order_detail', 'repair_progress')
