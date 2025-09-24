#!/usr/bin/env python3
"""
修复数据库序列问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_sequences():
    """修复序列"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            # 先检查序列是否存在，如果不存在则创建
            # 修复 dic_type 序列
            result = conn.execute(text("SELECT MAX(id) FROM dic_type"))
            max_id = result.scalar()
            if max_id:
                # 检查序列是否存在
                seq_check = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT 1 FROM pg_sequences 
                        WHERE schemaname = 'public' 
                        AND sequencename = 'dic_type_id_seq'
                    )
                """))
                seq_exists = seq_check.scalar()
                
                if not seq_exists:
                    # 创建序列
                    conn.execute(text(f"CREATE SEQUENCE dic_type_id_seq START {max_id + 1}"))
                    print("创建了 dic_type_id_seq 序列")
                else:
                    # 更新序列
                    conn.execute(text(f"SELECT setval('dic_type_id_seq', {max_id + 1}, false)"))
                    print(f"dic_type 序列已更新到: {max_id + 1}")
            
            # 修复 dic_enum 序列
            result = conn.execute(text("SELECT MAX(id) FROM dic_enum"))
            max_id = result.scalar()
            if max_id:
                # 检查序列是否存在
                seq_check = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT 1 FROM pg_sequences 
                        WHERE schemaname = 'public' 
                        AND sequencename = 'dic_enum_id_seq'
                    )
                """))
                seq_exists = seq_check.scalar()
                
                if not seq_exists:
                    # 创建序列
                    conn.execute(text(f"CREATE SEQUENCE dic_enum_id_seq START {max_id + 1}"))
                    print("创建了 dic_enum_id_seq 序列")
                else:
                    # 更新序列
                    conn.execute(text(f"SELECT setval('dic_enum_id_seq', {max_id + 1}, false)"))
                    print(f"dic_enum 序列已更新到: {max_id + 1}")
            
            trans.commit()
            print("序列修复完成")
            
        except Exception as e:
            trans.rollback()
            print(f"修复失败: {e}")
            sys.exit(1)

if __name__ == "__main__":
    fix_sequences()
