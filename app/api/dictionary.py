from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.dictionary import (
    DictionaryTypeCreate, DictionaryTypeResponse, DictionaryTypeUpdate,
    DictionaryEnumCreate, DictionaryEnumResponse, DictionaryEnumUpdate,
    DictionaryTypeWithEnumsResponse
)
from app.schemas.base import ApiResponse
from app.crud.dictionary import dictionary_type_crud, dictionary_enum_crud
from app.models.user import User

router = APIRouter()


def get_current_user_dependency(authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    """获取当前登录用户的依赖函数"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="无效的认证头")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="无效的token或用户不存在")
    if not user.status:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return user


# 字典类型相关接口
@router.get("/types", response_model=ApiResponse)
def get_dictionary_types(current: int = 1, size: int = 100, db: Session = Depends(get_db)):
    """获取字典类型列表"""
    try:
        skip = (current - 1) * size
        types = dictionary_type_crud.get_multi(db, skip=skip, limit=size)
        
        total = db.query(dictionary_type_crud.model).count()
        
        type_responses = [DictionaryTypeResponse.model_validate(type_obj) for type_obj in types]
        
        response_data = {
            "records": type_responses,
            "total": total,
            "current": current,
            "size": size
        }
        
        return ApiResponse(data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取字典类型列表失败: {str(e)}")


@router.post("/types", response_model=ApiResponse)
def create_dictionary_type(type_data: DictionaryTypeCreate, db: Session = Depends(get_db)):
    """创建字典类型"""
    try:
        # 检查名称和编码是否已存在
        if dictionary_type_crud.get_by_name(db, type_data.name):
            raise HTTPException(status_code=400, detail="字典类型名称已存在")
        if dictionary_type_crud.get_by_code(db, type_data.code):
            raise HTTPException(status_code=400, detail="字典类型编码已存在")
        
        created_type = dictionary_type_crud.create(db, type_data.model_dump())
        return ApiResponse(message="字典类型创建成功", data=DictionaryTypeResponse.model_validate(created_type))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建字典类型失败: {str(e)}")


@router.get("/types/{type_id}", response_model=ApiResponse)
def get_dictionary_type(type_id: int, db: Session = Depends(get_db)):
    """获取单个字典类型"""
    try:
        type_obj = dictionary_type_crud.get_or_404(db, type_id, "字典类型未找到")
        return ApiResponse(data=DictionaryTypeResponse.model_validate(type_obj))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取字典类型失败: {str(e)}")


@router.put("/types/{type_id}", response_model=ApiResponse)
def update_dictionary_type(type_id: int, type_update: DictionaryTypeUpdate, db: Session = Depends(get_db)):
    """更新字典类型"""
    try:
        type_obj = dictionary_type_crud.get_or_404(db, type_id, "字典类型未找到")
        
        # 检查名称和编码是否重复
        if type_update.name and type_update.name != type_obj.name:
            if dictionary_type_crud.get_by_name(db, type_update.name):
                raise HTTPException(status_code=400, detail="字典类型名称已存在")
        if type_update.code and type_update.code != type_obj.code:
            if dictionary_type_crud.get_by_code(db, type_update.code):
                raise HTTPException(status_code=400, detail="字典类型编码已存在")
        
        updated_type = dictionary_type_crud.update(db, type_obj, type_update.model_dump(exclude_unset=True))
        return ApiResponse(message="字典类型更新成功", data=DictionaryTypeResponse.model_validate(updated_type))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新字典类型失败: {str(e)}")


@router.delete("/types/{type_id}", response_model=ApiResponse)
def delete_dictionary_type(type_id: int, db: Session = Depends(get_db)):
    """删除字典类型"""
    try:
        type_obj = dictionary_type_crud.get_or_404(db, type_id, "字典类型未找到")
        dictionary_type_crud.delete(db, type_obj)
        return ApiResponse(message="字典类型删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除字典类型失败: {str(e)}")


# 字典枚举相关接口
@router.get("/enums", response_model=ApiResponse)
def get_dictionary_enums(type_id: int, current: int = 1, size: int = 100, db: Session = Depends(get_db)):
    """获取字典枚举列表"""
    try:
        skip = (current - 1) * size
        enums = dictionary_enum_crud.get_by_type_id(db, type_id, skip=skip, limit=size)
        
        total = db.query(dictionary_enum_crud.model).filter(
            dictionary_enum_crud.model.type_id == type_id,
            dictionary_enum_crud.model.status == True
        ).count()
        
        enum_responses = [DictionaryEnumResponse.model_validate(enum_obj) for enum_obj in enums]
        
        response_data = {
            "records": enum_responses,
            "total": total,
            "current": current,
            "size": size
        }
        
        return ApiResponse(data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取字典枚举列表失败: {str(e)}")


@router.post("/enums", response_model=ApiResponse)
def create_dictionary_enum(enum_data: DictionaryEnumCreate, db: Session = Depends(get_db)):
    """创建字典枚举"""
    try:
        # 检查键值是否已存在
        if dictionary_enum_crud.get_by_type_id_and_key(db, enum_data.type_id, enum_data.key_value):
            raise HTTPException(status_code=400, detail="键值已存在")
        
        created_enum = dictionary_enum_crud.create(db, enum_data.model_dump())
        return ApiResponse(message="字典枚举创建成功", data=DictionaryEnumResponse.model_validate(created_enum))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建字典枚举失败: {str(e)}")


@router.get("/enums/{enum_id}", response_model=ApiResponse)
def get_dictionary_enum(enum_id: int, db: Session = Depends(get_db)):
    """获取单个字典枚举"""
    try:
        enum_obj = dictionary_enum_crud.get_or_404(db, enum_id, "字典枚举未找到")
        return ApiResponse(data=DictionaryEnumResponse.model_validate(enum_obj))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取字典枚举失败: {str(e)}")


@router.put("/enums/{enum_id}", response_model=ApiResponse)
def update_dictionary_enum(enum_id: int, enum_update: DictionaryEnumUpdate, db: Session = Depends(get_db)):
    """更新字典枚举"""
    try:
        enum_obj = dictionary_enum_crud.get_or_404(db, enum_id, "字典枚举未找到")
        
        # 检查键值是否重复
        if enum_update.key_value and enum_update.key_value != enum_obj.key_value:
            if dictionary_enum_crud.get_by_type_id_and_key(db, enum_obj.type_id, enum_update.key_value):
                raise HTTPException(status_code=400, detail="键值已存在")
        
        updated_enum = dictionary_enum_crud.update(db, enum_obj, enum_update.model_dump(exclude_unset=True))
        return ApiResponse(message="字典枚举更新成功", data=DictionaryEnumResponse.model_validate(updated_enum))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新字典枚举失败: {str(e)}")


@router.delete("/enums/{enum_id}", response_model=ApiResponse)
def delete_dictionary_enum(enum_id: int, db: Session = Depends(get_db)):
    """删除字典枚举"""
    try:
        enum_obj = dictionary_enum_crud.get_or_404(db, enum_id, "字典枚举未找到")
        dictionary_enum_crud.delete(db, enum_obj)
        return ApiResponse(message="字典枚举删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除字典枚举失败: {str(e)}")
