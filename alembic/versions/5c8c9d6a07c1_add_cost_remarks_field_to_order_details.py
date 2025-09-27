"""add_cost_remarks_field_to_order_details

Revision ID: 5c8c9d6a07c1
Revises: 7a97613a3325
Create Date: 2025-09-27 17:52:16.208120

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5c8c9d6a07c1'
down_revision = '7a97613a3325'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 为保内工单详情表添加cost_remarks字段
    op.add_column('internal_order_detail', sa.Column('cost_remarks', postgresql.JSON(astext_type=sa.Text()), nullable=True, comment='费用使用备注'))
    
    # 为保外工单详情表添加cost_remarks字段
    op.add_column('external_order_detail', sa.Column('cost_remarks', postgresql.JSON(astext_type=sa.Text()), nullable=True, comment='费用使用备注'))


def downgrade() -> None:
    # 删除保内工单详情表的cost_remarks字段
    op.drop_column('internal_order_detail', 'cost_remarks')
    
    # 删除保外工单详情表的cost_remarks字段
    op.drop_column('external_order_detail', 'cost_remarks')
