from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.crud import CRUDBase
from app.models.system_settings import SystemSetting


class CRUDSystemSetting(CRUDBase[SystemSetting]):
    def get_by_key(self, db: Session, *, setting_key: str) -> Optional[SystemSetting]:
        return db.query(SystemSetting).filter(SystemSetting.setting_key == setting_key).first()
    
    def get_value_by_key(self, db: Session, *, setting_key: str) -> Optional[str]:
        setting = self.get_by_key(db, setting_key=setting_key)
        return setting.setting_value if setting else None
    
    def update_by_key(self, db: Session, *, setting_key: str, setting_value: str, update_by: str = None) -> Optional[SystemSetting]:
        setting = self.get_by_key(db, setting_key=setting_key)
        if setting:
            setting.setting_value = setting_value
            if update_by:
                setting.update_by = update_by
            db.commit()
            db.refresh(setting)
        return setting
    
    def get_active_settings(self, db: Session) -> List[SystemSetting]:
        return db.query(SystemSetting).filter(SystemSetting.status == True).all()


system_setting_crud = CRUDSystemSetting(SystemSetting)
