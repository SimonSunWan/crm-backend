from typing import List, Optional

from app.schemas.base import CamelCaseModel


class DictionaryTypeBase(CamelCaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DictionaryTypeCreate(DictionaryTypeBase):
    pass


class DictionaryTypeUpdate(CamelCaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


class DictionaryTypeResponse(DictionaryTypeBase):
    id: int
    status: bool


class DictionaryEnumBase(CamelCaseModel):
    type_id: int
    parent_id: Optional[int] = None
    key_value: str
    dict_value: str
    sort_order: Optional[int] = 0
    level: Optional[int] = 1
    path: Optional[str] = None


class DictionaryEnumCreate(DictionaryEnumBase):
    pass


class DictionaryEnumUpdate(CamelCaseModel):
    parent_id: Optional[int] = None
    key_value: Optional[str] = None
    dict_value: Optional[str] = None
    sort_order: Optional[int] = None
    level: Optional[int] = None
    path: Optional[str] = None
    status: Optional[bool] = None


class DictionaryEnumResponse(DictionaryEnumBase):
    id: int
    status: bool
    children: Optional[List["DictionaryEnumResponse"]] = []
    has_children: Optional[bool] = False


class DictionaryTypeWithEnumsResponse(DictionaryTypeResponse):
    enums: List[DictionaryEnumResponse] = []
