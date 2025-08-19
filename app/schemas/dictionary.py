from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DictionaryTypeBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DictionaryTypeCreate(DictionaryTypeBase):
    pass


class DictionaryTypeUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


class DictionaryTypeResponse(DictionaryTypeBase):
    id: int
    status: bool
    create_by: Optional[str] = Field(default=None, alias='createBy')
    create_time: Optional[datetime] = Field(default=None, alias='createTime')
    update_by: Optional[str] = Field(default=None, alias='updateBy')
    update_time: Optional[datetime] = Field(default=None, alias='updateTime')

    class Config:
        from_attributes = True
        populate_by_name = True


class DictionaryEnumBase(BaseModel):
    type_id: int = Field(alias='typeId')
    key_value: str = Field(alias='keyValue')
    dict_value: str = Field(alias='dictValue')
    sort_order: Optional[int] = Field(default=0, alias='sortOrder')

    class Config:
        populate_by_name = True


class DictionaryEnumCreate(DictionaryEnumBase):
    pass


class DictionaryEnumUpdate(BaseModel):
    key_value: Optional[str] = Field(default=None, alias='keyValue')
    dict_value: Optional[str] = Field(default=None, alias='dictValue')
    sort_order: Optional[int] = Field(default=None, alias='sortOrder')
    status: Optional[bool] = None

    class Config:
        populate_by_name = True


class DictionaryEnumResponse(DictionaryEnumBase):
    id: int
    status: bool
    create_by: Optional[str] = Field(default=None, alias='createBy')
    create_time: Optional[datetime] = Field(default=None, alias='createTime')
    update_by: Optional[str] = Field(default=None, alias='updateBy')
    update_time: Optional[datetime] = Field(default=None, alias='updateTime')

    class Config:
        from_attributes = True
        populate_by_name = True


class DictionaryTypeWithEnumsResponse(DictionaryTypeResponse):
    enums: List[DictionaryEnumResponse] = []
