from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.order import (
    InternalOrderCreate, 
    InternalOrderResponse, 
    InternalOrderUpdate,
    ExternalOrderCreate,
    ExternalOrderResponse,
    ExternalOrderUpdate
)
from app.schemas.base import ApiResponse
from app.crud.order import internal_order_crud, external_order_crud

router = APIRouter()


@router.get("/internal/", response_model=ApiResponse)
def get_internal_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取保内工单列表"""
    try:
        orders = internal_order_crud.get_multi(db, skip=skip, limit=limit)
        order_responses = [InternalOrderResponse.model_validate(order) for order in orders]
        return ApiResponse(data=order_responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取保内工单列表失败: {str(e)}")


@router.post("/internal/", response_model=ApiResponse)
def create_internal_order(order: InternalOrderCreate, db: Session = Depends(get_db)):
    """创建保内工单"""
    try:
        created_order = internal_order_crud.create(db, order.model_dump())
        order_response = InternalOrderResponse.model_validate(created_order)
        return ApiResponse(message="保内工单创建成功", data=order_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建保内工单失败: {str(e)}")


@router.get("/internal/{order_id}", response_model=ApiResponse)
def get_internal_order(order_id: str, db: Session = Depends(get_db)):
    """获取单个保内工单"""
    try:
        order = internal_order_crud.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="保内工单未找到")
        order_response = InternalOrderResponse.model_validate(order)
        return ApiResponse(data=order_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取保内工单失败: {str(e)}")


@router.put("/internal/{order_id}", response_model=ApiResponse)
def update_internal_order(order_id: str, order_update: InternalOrderUpdate, db: Session = Depends(get_db)):
    """更新保内工单"""
    try:
        order = internal_order_crud.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="保内工单未找到")
        updated_order = internal_order_crud.update(db, order, order_update.model_dump(exclude_unset=True))
        order_response = InternalOrderResponse.model_validate(updated_order)
        return ApiResponse(message="保内工单更新成功", data=order_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新保内工单失败: {str(e)}")


@router.delete("/internal/{order_id}", response_model=ApiResponse)
def delete_internal_order(order_id: str, db: Session = Depends(get_db)):
    """删除保内工单"""
    try:
        order = internal_order_crud.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="保内工单未找到")
        internal_order_crud.delete(db, order)
        return ApiResponse(message="保内工单删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除保内工单失败: {str(e)}")


@router.get("/external/", response_model=ApiResponse)
def get_external_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取保外工单列表"""
    try:
        orders = external_order_crud.get_multi(db, skip=skip, limit=limit)
        order_responses = [ExternalOrderResponse.model_validate(order) for order in orders]
        return ApiResponse(data=order_responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取保外工单列表失败: {str(e)}")


@router.post("/external/", response_model=ApiResponse)
def create_external_order(order: ExternalOrderCreate, db: Session = Depends(get_db)):
    """创建保外工单"""
    try:
        created_order = external_order_crud.create(db, order.model_dump())
        order_response = ExternalOrderResponse.model_validate(created_order)
        return ApiResponse(message="保外工单创建成功", data=order_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建保外工单失败: {str(e)}")


@router.get("/external/{order_id}", response_model=ApiResponse)
def get_external_order(order_id: str, db: Session = Depends(get_db)):
    """获取单个保外工单"""
    try:
        order = external_order_crud.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="保外工单未找到")
        order_response = ExternalOrderResponse.model_validate(order)
        return ApiResponse(data=order_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取保外工单失败: {str(e)}")


@router.put("/external/{order_id}", response_model=ApiResponse)
def update_external_order(order_id: str, order_update: ExternalOrderUpdate, db: Session = Depends(get_db)):
    """更新保外工单"""
    try:
        order = external_order_crud.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="保外工单未找到")
        updated_order = external_order_crud.update(db, order, order_update.model_dump(exclude_unset=True))
        order_response = ExternalOrderResponse.model_validate(updated_order)
        return ApiResponse(message="保外工单更新成功", data=order_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新保外工单失败: {str(e)}")


@router.delete("/external/{order_id}", response_model=ApiResponse)
def delete_external_order(order_id: str, db: Session = Depends(get_db)):
    """删除保外工单"""
    try:
        order = external_order_crud.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="保外工单未找到")
        external_order_crud.delete(db, order)
        return ApiResponse(message="保外工单删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除保外工单失败: {str(e)}")
