"""rename_dictionary_tables_to_singular

Revision ID: 29d593506090
Revises: 93c0df211b63
Create Date: 2025-09-10 17:08:01.082899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29d593506090'
down_revision = '93c0df211b63'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 重命名字典表名从复数到单数
    op.rename_table('dic_types', 'dic_type')
    op.rename_table('dic_enums', 'dic_enum')
    
    # 更新外键约束
    # 更新 dic_enum 表的外键
    op.drop_constraint('dic_enums_parent_id_fkey', 'dic_enum', type_='foreignkey')
    op.create_foreign_key('dic_enum_parent_id_fkey', 'dic_enum', 'dic_enum', ['parent_id'], ['id'])


def downgrade() -> None:
    # 恢复外键约束到原来的表名
    # 恢复 dic_enum 表的外键
    op.drop_constraint('dic_enum_parent_id_fkey', 'dic_enum', type_='foreignkey')
    op.create_foreign_key('dic_enums_parent_id_fkey', 'dic_enum', 'dic_enums', ['parent_id'], ['id'])
    
    # 重命名表名从单数回到复数
    op.rename_table('dic_enum', 'dic_enums')
    op.rename_table('dic_type', 'dic_types')
