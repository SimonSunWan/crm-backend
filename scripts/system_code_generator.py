import asyncio
import random
import string
from datetime import datetime
from app.core.database import SessionLocal
from app.crud.system_settings import system_setting_crud


def generate_system_code():
    """生成六位数字+字母的随机组合，区分大小写"""
    characters = string.ascii_letters + string.digits  # 包含大小写字母和数字
    return ''.join(random.choices(characters, k=6))


async def update_system_code():
    """更新系统码"""
    db = SessionLocal()
    try:
        new_code = generate_system_code()
        
        # 检查系统码配置是否存在
        existing_setting = system_setting_crud.get_by_key(db, setting_key="REGISTER_SYSTEM_CODE")
        
        if existing_setting:
            # 如果存在，更新系统码
            updated_setting = system_setting_crud.update_by_key(
                db, 
                setting_key="REGISTER_SYSTEM_CODE", 
                setting_value=new_code,
                update_by="system"
            )
            if updated_setting:
                pass
            else:
                pass
        else:
            # 如果不存在，创建系统码配置
            system_code_data = {
                "setting_key": "REGISTER_SYSTEM_CODE",
                "setting_value": new_code,
                "setting_name": "注册系统码",
                "setting_desc": "用户注册和忘记密码时需要的系统验证码",
                "status": True,
                "create_by": "system"
            }
            created_setting = system_setting_crud.create(db, system_code_data)
            if created_setting:
                pass
            else:
                pass
                
    except Exception as e:
        pass
    finally:
        db.close()


async def system_code_scheduler():
    """系统码定时更新任务"""
    
    # 立即执行一次
    await update_system_code()
    
    # 每10分钟执行一次
    while True:
        await asyncio.sleep(600)  # 600秒 = 10分钟
        await update_system_code()


if __name__ == "__main__":
    asyncio.run(system_code_scheduler())
