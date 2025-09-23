"""add_is_end_to_orders

Revision ID: 7a97613a3325
Revises: 004
Create Date: 2025-09-23 22:43:35.376020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a97613a3325'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加 is_end 字段到 internal_order 表
    op.add_column('internal_order', sa.Column('is_end', sa.Boolean(), nullable=False, server_default='false', comment='是否完成所有步骤'))
    
    # 添加 is_end 字段到 external_order 表
    op.add_column('external_order', sa.Column('is_end', sa.Boolean(), nullable=False, server_default='false', comment='是否完成所有步骤'))


def downgrade() -> None:
    # 删除 is_end 字段
    op.drop_column('external_order', 'is_end')
    op.drop_column('internal_order', 'is_end')
