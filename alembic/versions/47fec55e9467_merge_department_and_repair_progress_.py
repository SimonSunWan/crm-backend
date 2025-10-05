"""merge_department_and_repair_progress_branches

Revision ID: 47fec55e9467
Revises: 005_add_department_tables, add_repair_progress_field
Create Date: 2025-10-04 21:55:11.164012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47fec55e9467'
down_revision = ('005_add_department_tables', 'add_repair_progress_field')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
