from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.crud.order import external_order_crud, internal_order_crud
from app.models.user import User
from app.schemas.base import ApiResponse
from app.schemas.order import (
    ExternalOrderCreate,
    ExternalOrderResponse,
    ExternalOrderUpdate,
    InternalOrderCreate,
    InternalOrderResponse,
    InternalOrderUpdate,
)

router = APIRouter()


@router.get("/internal/", response_model=ApiResponse)
def get_internal_orders(
    current: int = 1,
    size: int = 20,
    orderNo: str = None,
    customer: str = None,
    vehicleModel: str = None,
    repairShop: str = None,
    reporterName: str = None,
    dateRange: list = None,
    createdBy: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取保内工单列表"""
    try:
        skip = (current - 1) * size

        # 构建基础查询
        query = db.query(internal_order_crud.model)

        # 根据createdBy参数过滤
        if createdBy is not None:
            query = query.filter(internal_order_crud.model.created_by == createdBy)

        # 添加筛选条件
        if orderNo:
            query = query.filter(internal_order_crud.model.id.contains(orderNo))

        if customer:
            query = query.filter(internal_order_crud.model.customer.contains(customer))

        if vehicleModel:
            query = query.filter(
                internal_order_crud.model.vehicle_model.contains(vehicleModel)
            )

        if repairShop:
            query = query.filter(
                internal_order_crud.model.repair_shop.contains(repairShop)
            )

        if reporterName:
            query = query.filter(
                internal_order_crud.model.reporter_name.contains(reporterName)
            )

        if dateRange and len(dateRange) == 2:
            start_date, end_date = dateRange
            if start_date and end_date:
                query = query.filter(
                    internal_order_crud.model.report_date >= start_date,
                    internal_order_crud.model.report_date <= end_date,
                )

        # 获取总数
        total = query.count()

        # 按创建时间倒序排序并获取分页数据
        orders = (
            query.order_by(internal_order_crud.model.create_time.desc())
            .offset(skip)
            .limit(size)
            .all()
        )
        order_responses = [
            InternalOrderResponse.model_validate(order) for order in orders
        ]

        # 返回包含分页信息的响应
        response_data = {
            "records": order_responses,
            "total": total,
            "current": current,
            "size": size,
        }

        return ApiResponse(data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取保内工单列表失败: {str(e)}")


@router.post("/internal/", response_model=ApiResponse)
def create_internal_order(
    order: InternalOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """创建保内工单"""
    try:
        order_data = order.model_dump(by_alias=False)
        order_data["created_by"] = current_user.id

        # 分离主工单数据和详情数据
        detail_fields = [
            "repair_person",
            "repair_date",
            "avic_responsibility",
            "fault_classification",
            "fault_location",
            "part_category",
            "part_location",
            "repair_description",
            "spare_part_location",
            "spare_parts",
            "costs",
            "labors",
            "repair_progress",
            "cost_remarks",
        ]

        detail_data = {}
        for field in detail_fields:
            if field in order_data:
                detail_data[field] = order_data.pop(field)

        # 创建工单和详情记录
        created_order = internal_order_crud.create_with_details(
            db, order_data, detail_data
        )
        order_response = InternalOrderResponse.model_validate(created_order)
        return ApiResponse(message="保内工单创建成功", data=order_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建保内工单失败: {str(e)}")


@router.get("/internal/{order_id}", response_model=ApiResponse)
def get_internal_order(order_id: str, db: Session = Depends(get_db)):
    """获取单个保内工单"""
    try:
        order = internal_order_crud.get_with_details(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="保内工单未找到")
        order_response = InternalOrderResponse.model_validate(order)
        return ApiResponse(data=order_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取保内工单失败: {str(e)}")


@router.put("/internal/{order_id}", response_model=ApiResponse)
def update_internal_order(
    order_id: str, order_update: InternalOrderUpdate, db: Session = Depends(get_db)
):
    """更新保内工单"""
    try:
        order = internal_order_crud.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="保内工单未找到")

        update_data = order_update.model_dump(exclude_unset=True, by_alias=False)

        # 分离主工单数据和详情数据
        detail_fields = [
            "repair_person",
            "repair_date",
            "avic_responsibility",
            "fault_classification",
            "fault_location",
            "part_category",
            "part_location",
            "repair_description",
            "spare_part_location",
            "spare_parts",
            "costs",
            "labors",
            "repair_progress",
            "cost_remarks",
        ]

        detail_data = {}
        for field in detail_fields:
            if field in update_data:
                detail_data[field] = update_data.pop(field)

        # 更新工单和详情记录
        updated_order = internal_order_crud.update_with_details(
            db, order_id, update_data, detail_data
        )
        order_response = InternalOrderResponse.model_validate(updated_order)
        return ApiResponse(message="保内工单更新成功", data=order_response)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除保内工单失败: {str(e)}")


@router.get("/external/", response_model=ApiResponse)
def get_external_orders(
    current: int = 1,
    size: int = 20,
    orderNo: str = None,
    customer: str = None,
    vehicleModel: str = None,
    repairShop: str = None,
    reporterName: str = None,
    sparePartLocation: str = None,
    dateRange: list = None,
    createdBy: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取保外工单列表"""
    try:
        skip = (current - 1) * size

        # 构建基础查询
        query = db.query(external_order_crud.model)

        # 根据createdBy参数过滤
        if createdBy is not None:
            query = query.filter(external_order_crud.model.created_by == createdBy)

        # 添加筛选条件
        if orderNo:
            query = query.filter(external_order_crud.model.id.contains(orderNo))

        if customer:
            query = query.filter(external_order_crud.model.customer.contains(customer))

        if vehicleModel:
            query = query.filter(
                external_order_crud.model.vehicle_model.contains(vehicleModel)
            )

        if repairShop:
            query = query.filter(
                external_order_crud.model.repair_shop.contains(repairShop)
            )

        if reporterName:
            query = query.filter(
                external_order_crud.model.reporter_name.contains(reporterName)
            )

        if sparePartLocation:
            # 通过关联的详情表筛选备件所属库位
            from app.models.order import ExternalOrderDetail
            query = query.join(ExternalOrderDetail).filter(
                ExternalOrderDetail.spare_part_location.contains(sparePartLocation)
            )

        if dateRange and len(dateRange) == 2:
            start_date, end_date = dateRange
            if start_date and end_date:
                query = query.filter(
                    external_order_crud.model.report_date >= start_date,
                    external_order_crud.model.report_date <= end_date,
                )

        # 获取总数
        total = query.count()

        # 按创建时间倒序排序并获取分页数据
        orders = (
            query.order_by(external_order_crud.model.create_time.desc())
            .offset(skip)
            .limit(size)
            .all()
        )
        order_responses = [
            ExternalOrderResponse.model_validate(order) for order in orders
        ]

        # 返回包含分页信息的响应
        response_data = {
            "records": order_responses,
            "total": total,
            "current": current,
            "size": size,
        }

        return ApiResponse(data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取保外工单列表失败: {str(e)}")


@router.post("/external/", response_model=ApiResponse)
def create_external_order(
    order: ExternalOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """创建保外工单"""
    try:
        order_data = order.model_dump(by_alias=False)
        order_data["created_by"] = current_user.id

        # 分离主工单数据和详情数据
        detail_fields = [
            "repair_person",
            "repair_date",
            "avic_responsibility",
            "fault_classification",
            "fault_location",
            "part_category",
            "part_location",
            "repair_description",
            "spare_part_location",
            "spare_parts",
            "costs",
            "labors",
            "repair_progress",
            "cost_remarks",
        ]

        detail_data = {}
        for field in detail_fields:
            if field in order_data:
                detail_data[field] = order_data.pop(field)

        # 创建工单和详情记录
        created_order = external_order_crud.create_with_details(
            db, order_data, detail_data
        )
        order_response = ExternalOrderResponse.model_validate(created_order)
        return ApiResponse(message="保外工单创建成功", data=order_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建保外工单失败: {str(e)}")


@router.get("/external/{order_id}", response_model=ApiResponse)
def get_external_order(order_id: str, db: Session = Depends(get_db)):
    """获取单个保外工单"""
    try:
        order = external_order_crud.get_with_details(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="保外工单未找到")
        order_response = ExternalOrderResponse.model_validate(order)
        return ApiResponse(data=order_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取保外工单失败: {str(e)}")


@router.put("/external/{order_id}", response_model=ApiResponse)
def update_external_order(
    order_id: str, order_update: ExternalOrderUpdate, db: Session = Depends(get_db)
):
    """更新保外工单"""
    try:
        order = external_order_crud.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="保外工单未找到")

        update_data = order_update.model_dump(exclude_unset=True, by_alias=False)

        # 分离主工单数据和详情数据
        detail_fields = [
            "repair_person",
            "repair_date",
            "avic_responsibility",
            "fault_classification",
            "fault_location",
            "part_category",
            "part_location",
            "repair_description",
            "spare_part_location",
            "spare_parts",
            "costs",
            "labors",
            "repair_progress",
            "cost_remarks",
        ]

        detail_data = {}
        for field in detail_fields:
            if field in update_data:
                detail_data[field] = update_data.pop(field)

        # 更新工单和详情记录
        updated_order = external_order_crud.update_with_details(
            db, order_id, update_data, detail_data
        )
        order_response = ExternalOrderResponse.model_validate(updated_order)
        return ApiResponse(message="保外工单更新成功", data=order_response)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除保外工单失败: {str(e)}")
