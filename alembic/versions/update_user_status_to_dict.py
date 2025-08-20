"""update user status to dict

Revision ID: update_user_status_to_dict
Revises: e736852c7081
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'update_user_status_to_dict'
down_revision = 'e736852c7081'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """升级：将用户状态字段从boolean改为string"""
    # 1. 添加新的status_string字段
    op.add_column('users', sa.Column('status_string', sa.String(), nullable=True))
    
    # 2. 更新数据：将boolean值转换为string值
    op.execute("""
        UPDATE users 
        SET status_string = CASE 
            WHEN status = true THEN '1' 
            WHEN status = false THEN '2' 
            ELSE '1' 
        END
        WHERE status IN (true, false)
    """)
    
    # 3. 删除旧的status字段
    op.drop_column('users', 'status')
    
    # 4. 重命名新字段为status
    op.alter_column('users', 'status_string', new_column_name='status')


def downgrade() -> None:
    """降级：将用户状态字段从string改回boolean"""
    # 1. 添加新的status_boolean字段
    op.add_column('users', sa.Column('status_boolean', sa.Boolean(), nullable=True))
    
    # 2. 更新数据：将string值转换为boolean值
    op.execute("""
        UPDATE users 
        SET status_boolean = CASE 
            WHEN status = '1' THEN true 
            WHEN status = '2' THEN false 
            ELSE true 
        END
        WHERE status IN ('1', '2')
    """)
    
    # 3. 删除旧的status字段
    op.drop_column('users', 'status')
    
    # 4. 重命名新字段为status
    op.alter_column('users', 'status_boolean', new_column_name='status')
