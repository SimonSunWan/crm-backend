from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_superuser
from app.crud.department import department_crud
from app.models.user import User
from app.schemas.base import ApiResponse
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate

router = APIRouter()


def department_to_response(dept) -> DepartmentResponse:
    """将Department对象转换为DepartmentResponse对象"""
    return DepartmentResponse.model_validate(dept)


def build_department_tree(departments, parent_id=None):
    """构建部门树形结构"""
    tree = []
    for dept in departments:
        if dept.parent_id == parent_id:
            children = build_department_tree(departments, dept.id)
            dept_response = department_to_response(dept)
            dept_response.children = children
            tree.append(dept_response)
    tree.sort(key=lambda x: x.sort_order)
    return tree


def filter_department_tree(tree, name_filter=None, status_filter=None):
    """过滤部门树"""
    filtered = []
    for dept in tree:
        matches = True
        if name_filter and name_filter.lower() not in dept.dept_name.lower():
            matches = False
        if status_filter is not None and dept.status != status_filter:
            matches = False

        filtered_children = filter_department_tree(dept.children, name_filter, status_filter)

        if matches or filtered_children:
            dept.children = filtered_children
            filtered.append(dept)
    return filtered


def count_department_tree_nodes(tree):
    """计算部门树形结构的总节点数"""
    count = len(tree)
    for node in tree:
        if node.children:
            count += count_department_tree_nodes(node.children)
    return count


@router.get("/", response_model=ApiResponse)
def get_departments(
    dept_name: Optional[str] = None,
    status: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """获取部门列表"""
    try:
        all_departments = db.query(department_crud.model).options(
            joinedload(department_crud.model.users),
            joinedload(department_crud.model.leaders)
        ).all()

        dept_tree = build_department_tree(all_departments)

        if dept_name or status is not None:
            dept_tree = filter_department_tree(dept_tree, dept_name, status)

        total_nodes = count_department_tree_nodes(dept_tree)
        response_data = {
            "records": dept_tree,
            "total": total_nodes,
            "current": 1,
            "size": total_nodes,
        }

        return ApiResponse(code=200, message="操作成功", data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部门列表失败: {str(e)}")


@router.get("/tree", response_model=ApiResponse)
def get_department_tree(db: Session = Depends(get_db)):
    """获取部门树形结构"""
    try:
        # 获取所有部门，预加载关联的用户和负责人数据
        departments = db.query(department_crud.model).options(
            joinedload(department_crud.model.users),
            joinedload(department_crud.model.leaders)
        ).all()
        
        # 转换为响应模型，处理children字段
        dept_responses = []
        for dept in departments:
            dept_response = department_to_response(dept)
            dept_responses.append(dept_response)
        return ApiResponse(code=200, message="操作成功", data=dept_responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部门树失败: {str(e)}")


@router.post("/", response_model=ApiResponse)
def create_department(
    department: DepartmentCreate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """创建部门"""
    try:
        # 检查部门名称是否已存在（同层级查重）
        if department_crud.get_by_name_and_parent(db, department.dept_name, department.parent_id):
            raise HTTPException(status_code=400, detail="部门名称已存在")


        # 创建部门数据
        dept_data = department.model_dump(by_alias=False)
        dept_data["created_by"] = current_user.user_name

        # 如果有parent_id，验证父部门是否存在
        if department.parent_id:
            parent_dept = department_crud.get_or_404(db, department.parent_id, "父部门不存在")
            dept_data["level"] = parent_dept.level + 1
            dept_data["path"] = f"{parent_dept.path or ''}/{department.parent_id}" if parent_dept.path else str(department.parent_id)

        created_dept = department_crud.create(db, dept_data)

        # 重新加载部门数据，包含关联的用户和负责人信息
        reloaded_dept = db.query(department_crud.model).options(
            joinedload(department_crud.model.users),
            joinedload(department_crud.model.leaders)
        ).filter(department_crud.model.id == created_dept.id).first()

        # 转换为响应模型
        dept_response = department_to_response(reloaded_dept)

        return ApiResponse(code=200, message="部门创建成功", data=dept_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建部门失败: {str(e)}")


@router.get("/{dept_id}", response_model=ApiResponse)
def get_department(dept_id: int, db: Session = Depends(get_db)):
    """获取单个部门"""
    try:
        # 获取部门，预加载关联的用户和负责人数据
        dept = db.query(department_crud.model).options(
            joinedload(department_crud.model.users),
            joinedload(department_crud.model.leaders)
        ).filter(department_crud.model.id == dept_id).first()
        
        if not dept:
            raise HTTPException(status_code=404, detail="部门未找到")
            
        # 转换为响应模型
        dept_response = department_to_response(dept)
        return ApiResponse(code=200, message="操作成功", data=dept_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部门失败: {str(e)}")


@router.put("/{dept_id}", response_model=ApiResponse)
def update_department(
    dept_id: int,
    department: DepartmentUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db),
):
    """更新部门"""
    try:
        # 检查部门是否存在
        existing_dept = department_crud.get_or_404(db, dept_id, "部门未找到")

        # 检查名称是否重复（如果更新了名称，同层级查重）
        if department.dept_name and department.dept_name != existing_dept.dept_name:
            if department_crud.get_by_name_and_parent(db, department.dept_name, existing_dept.parent_id):
                raise HTTPException(status_code=400, detail="部门名称已存在")


        # 更新部门数据
        update_data = department.model_dump(exclude_unset=True, by_alias=False)
        update_data["updated_by"] = current_user.user_name

        updated_dept = department_crud.update(db, existing_dept, update_data)

        # 重新加载部门数据，包含关联的用户和负责人信息
        reloaded_dept = db.query(department_crud.model).options(
            joinedload(department_crud.model.users),
            joinedload(department_crud.model.leaders)
        ).filter(department_crud.model.id == dept_id).first()

        # 转换为响应模型
        dept_response = department_to_response(reloaded_dept)
        return ApiResponse(code=200, message="部门更新成功", data=dept_response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新部门失败: {str(e)}")


@router.delete("/{dept_id}", response_model=ApiResponse)
def delete_department(dept_id: int, db: Session = Depends(get_db)):
    """删除部门"""
    try:
        # 检查部门是否存在
        dept = department_crud.get_or_404(db, dept_id, "部门未找到")

        # 检查是否有子部门
        children_count = (
            db.query(department_crud.model)
            .filter(department_crud.model.parent_id == dept_id)
            .count()
        )
        if children_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"该部门下有 {children_count} 个子部门，无法删除",
            )

        # 检查是否有用户（负责人和部门成员的并集）
        from app.models.department import UserDepartment, DepartmentLeader
        
        member_user_ids = [uid[0] for uid in db.query(UserDepartment.user_id).filter(
            UserDepartment.dept_id == dept_id
        ).all()]
        
        leader_user_ids = [uid[0] for uid in db.query(DepartmentLeader.user_id).filter(
            DepartmentLeader.dept_id == dept_id
        ).all()]
        
        users_count = len(set(member_user_ids + leader_user_ids))
        
        if users_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"该部门下有 {users_count} 个用户，无法删除",
            )

        # 保存父部门ID用于后续更新
        parent_id = dept.parent_id

        # 删除部门
        department_crud.delete(db, dept)

        # 提交事务
        db.commit()

        # 更新父部门的status状态
        if parent_id:
            department_crud.update_parent_status(db, parent_id)

        return ApiResponse(code=200, message="部门删除成功")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除部门失败: {str(e)}")


@router.get("/{dept_id}/users", response_model=ApiResponse)
def get_department_users(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    """获取部门下的用户"""
    try:
        users = department_crud.get_users_by_dept(db, dept_id)
        return ApiResponse(code=200, message="操作成功", data=users)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取部门用户失败: {str(e)}")
