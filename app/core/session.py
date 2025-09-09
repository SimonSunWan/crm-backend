from contextlib import contextmanager
from sqlalchemy.orm import Session
from app.core.database import SessionLocal


@contextmanager
def get_db_session():
    """数据库会话上下文管理器"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_transaction():
    """获取数据库事务"""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
