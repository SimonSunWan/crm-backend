from pydantic import BaseModel, Field, field_serializer
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

    class Config:
        from_attributes = True
        populate_by_name = True


class DictionaryEnumBase(BaseModel):
    type_id: int = Field(alias='typeId')
    parent_id: Optional[int] = Field(default=None, alias='parentId')
    key_value: str = Field(alias='keyValue')
    dict_value: str = Field(alias='dictValue')
    sort_order: Optional[int] = Field(default=0, alias='sortOrder')
    level: Optional[int] = Field(default=1)
    path: Optional[str] = None

    class Config:
        populate_by_name = True


class DictionaryEnumCreate(DictionaryEnumBase):
    pass


class DictionaryEnumUpdate(BaseModel):
    parent_id: Optional[int] = Field(default=None, alias='parentId')
    key_value: Optional[str] = Field(default=None, alias='keyValue')
    dict_value: Optional[str] = Field(default=None, alias='dictValue')
    sort_order: Optional[int] = Field(default=None, alias='sortOrder')
    level: Optional[int] = None
    path: Optional[str] = None
    status: Optional[bool] = None

    class Config:
        populate_by_name = True


class DictionaryEnumResponse(DictionaryEnumBase):
    id: int
    status: bool
    children: Optional[List['DictionaryEnumResponse']] = []
    hasChildren: Optional[bool] = False

    class Config:
        from_attributes = True
        populate_by_name = True


class DictionaryTypeWithEnumsResponse(DictionaryTypeResponse):
    enums: List[DictionaryEnumResponse] = []
