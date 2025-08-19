from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.schemas.base import CamelCaseModel


class CustomerBase(CamelCaseModel):

    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class CustomerCreate(CamelCaseModel):

    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class CustomerUpdate(CamelCaseModel):

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class CustomerResponse(CustomerBase):

    id: int
    created_by: Optional[int] = None
    create_time: datetime
    update_time: Optional[datetime] = None
