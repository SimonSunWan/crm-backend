import os
import sys
from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context

# 设置环境变量以避免编码问题
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base
from app.models import user, dictionary
from app.core.config import settings

config = context.config

if config.config_file_name is not None:

    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():

    return settings.DATABASE_URL

def run_migrations_offline() -> None:

    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():

        context.run_migrations()

def run_migrations_online() -> None:

    # 直接使用 create_engine
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():

            context.run_migrations()

if context.is_offline_mode():

    run_migrations_offline()
else:

    run_migrations_online()
