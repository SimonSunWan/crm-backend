"""Add seal_code to orders

Revision ID: 002_add_seal_code_to_orders
Revises: 001_initial_migration_merged
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_seal_code_to_orders'
down_revision = '001_initial_migration_merged'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """添加封签编码字段到工单表"""
    # 为保内工单表添加封签编码字段
    op.add_column('internal_order', sa.Column('seal_code', sa.String(), nullable=True, comment='封签编码'))
    
    # 为保外工单表添加封签编码字段
    op.add_column('external_order', sa.Column('seal_code', sa.String(), nullable=True, comment='封签编码'))


def downgrade() -> None:
    """删除封签编码字段"""
    # 删除保内工单表的封签编码字段
    op.drop_column('internal_order', 'seal_code')
    
    # 删除保外工单表的封签编码字段
    op.drop_column('external_order', 'seal_code')
