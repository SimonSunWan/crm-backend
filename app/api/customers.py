from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.schemas.base import ApiResponse
from app.crud.customer import customer_crud

router = APIRouter()


@router.get("/", response_model=ApiResponse)
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取客户列表"""
    try:
        customers = customer_crud.get_multi(db, skip=skip, limit=limit)
        return ApiResponse(data=customers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取客户列表失败: {str(e)}")


@router.post("/", response_model=ApiResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """创建客户"""
    try:
        created_customer = customer_crud.create(db, customer.model_dump())
        return ApiResponse(message="客户创建成功", data=created_customer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建客户失败: {str(e)}")


@router.get("/{customer_id}", response_model=ApiResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """获取单个客户"""
    try:
        customer = customer_crud.get_or_404(db, customer_id, "客户未找到")
        return ApiResponse(data=customer)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取客户失败: {str(e)}")


@router.put("/{customer_id}", response_model=ApiResponse)
def update_customer(customer_id: int, customer_update: CustomerUpdate, db: Session = Depends(get_db)):
    """更新客户"""
    try:
        customer = customer_crud.get_or_404(db, customer_id, "客户未找到")
        updated_customer = customer_crud.update(db, customer, customer_update.model_dump(exclude_unset=True))
        return ApiResponse(message="客户更新成功", data=updated_customer)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新客户失败: {str(e)}")


@router.delete("/{customer_id}", response_model=ApiResponse)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """删除客户"""
    try:
        customer = customer_crud.get_or_404(db, customer_id, "客户未找到")
        customer_crud.delete(db, customer)
        return ApiResponse(message="客户删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除客户失败: {str(e)}")
