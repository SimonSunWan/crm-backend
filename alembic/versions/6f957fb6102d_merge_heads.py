"""merge heads

Revision ID: 6f957fb6102d
Revises: add_menu_table, update_user_status_to_dict
Create Date: 2025-08-20 14:10:06.253219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f957fb6102d'
down_revision = ('add_menu_table', 'update_user_status_to_dict')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
