from sqlalchemy.orm import Session

from app.core.crud import CRUDBase
from app.models.dictionary import DictionaryEnum, DictionaryType


class CRUDDictionaryType(CRUDBase[DictionaryType]):
    """字典类型 CRUD 操作"""

    def get_by_code(self, db: Session, code: str):
        """根据编码获取字典类型"""
        return db.query(self.model).filter(self.model.code == code).first()

    def get_by_name(self, db: Session, name: str):
        """根据名称获取字典类型"""
        return db.query(self.model).filter(self.model.name == name).first()


class CRUDDictionaryEnum(CRUDBase[DictionaryEnum]):
    """字典枚举 CRUD 操作"""

    def get_by_type_id(
        self, db: Session, type_id: int, skip: int = 0, limit: int = 100
    ):
        """根据类型ID获取字典枚举列表"""
        return (
            db.query(self.model)
            .filter(self.model.type_id == type_id, self.model.status)
            .order_by(self.model.sort_order)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_type_id_and_key(self, db: Session, type_id: int, key_value: str):
        """根据类型ID和键值获取字典枚举"""
        return (
            db.query(self.model)
            .filter(
                self.model.type_id == type_id,
                self.model.key_value == key_value,
                self.model.status,
            )
            .first()
        )

    def get_cascade_by_type_id(self, db: Session, type_id: int):
        """根据类型ID获取级联字典枚举列表"""
        return (
            db.query(self.model)
            .filter(self.model.type_id == type_id, self.model.status)
            .order_by(
                self.model.parent_id.nullsfirst(),
                self.model.level,
                self.model.sort_order,
            )
            .all()
        )

    def get_root_enums(self, db: Session, type_id: int):
        """获取根级枚举（无父级）"""
        return (
            db.query(self.model)
            .filter(
                self.model.type_id == type_id,
                self.model.parent_id.is_(None),
                self.model.status,
            )
            .order_by(self.model.sort_order)
            .all()
        )

    def get_children_by_parent_id(self, db: Session, parent_id: int):
        """根据父级ID获取子级枚举"""
        return (
            db.query(self.model)
            .filter(self.model.parent_id == parent_id, self.model.status)
            .order_by(self.model.sort_order)
            .all()
        )

    def build_cascade_tree(self, db: Session, type_id: int):
        """构建级联树结构"""
        all_enums = self.get_cascade_by_type_id(db, type_id)
        enum_map = {enum.id: enum for enum in all_enums}

        tree = []
        for enum in all_enums:
            enum.children = []
            enum.hasChildren = False

            if enum.parent_id is None:
                tree.append(enum)
            else:
                parent = enum_map.get(enum.parent_id)
                if parent:
                    parent.children.append(enum)
                    parent.hasChildren = True

        # 对树结构进行排序
        def sort_tree(nodes):
            # 按sort_order排序
            nodes.sort(key=lambda x: x.sort_order or 0)
            # 递归排序子节点
            for node in nodes:
                if hasattr(node, 'children') and node.children:
                    sort_tree(node.children)
        
        sort_tree(tree)
        return tree

    def delete_by_type_id(self, db: Session, type_id: int):
        """根据类型ID删除所有字典枚举"""
        db.query(self.model).filter(self.model.type_id == type_id).delete()
        db.commit()

    def delete_cascade(self, db: Session, enum_id: int):
        """级联删除字典枚举及其所有子级"""
        # 获取要删除的枚举对象
        enum_obj = self.get_or_404(db, enum_id, "字典枚举未找到")
        
        # 递归删除所有子级
        self._delete_children_recursive(db, enum_id)
        
        # 删除当前枚举
        db.delete(enum_obj)
        db.commit()

    def _delete_children_recursive(self, db: Session, parent_id: int):
        """递归删除所有子级枚举"""
        # 获取所有直接子级
        children = self.get_children_by_parent_id(db, parent_id)
        
        for child in children:
            # 递归删除子级的子级
            self._delete_children_recursive(db, child.id)
            # 删除当前子级
            db.delete(child)

    def batch_import(self, db: Session, type_id: int, import_data: list):
        """批量导入字典枚举"""
        from app.schemas.dictionary import BatchImportResult
        
        success_count = 0
        fail_count = 0
        errors = []
        
        # 创建键值到ID的映射，用于处理父子关系
        key_to_id_map = {}
        
        # 按层级排序，确保父级先创建
        sorted_data = sorted(import_data, key=lambda x: x.level or 1)
        
        for index, item in enumerate(sorted_data):
            try:
                # 检查键值是否已存在（包括当前批次中已处理的）
                existing_enum = self.get_by_type_id_and_key(db, type_id, item.key_value)
                if existing_enum:
                    # 如果已存在，将其ID添加到映射中，以便子级可以引用
                    key_to_id_map[item.key_value] = existing_enum.id
                    success_count += 1  # 已存在的项也算成功处理
                    continue
                
                # 检查是否在当前批次中已处理过
                if item.key_value in key_to_id_map:
                    success_count += 1  # 当前批次中已处理的项也算成功
                    continue
                
                # 处理父级关系
                parent_id = None
                if item.parent_key_value:
                    # 首先检查当前批次中是否已处理
                    parent_id = key_to_id_map.get(item.parent_key_value)
                    if not parent_id:
                        # 如果当前批次中没有，检查数据库中是否存在
                        parent_enum = self.get_by_type_id_and_key(db, type_id, item.parent_key_value)
                        if parent_enum:
                            parent_id = parent_enum.id
                            key_to_id_map[item.parent_key_value] = parent_id
                        else:
                            errors.append({
                                'row': index + 1,
                                'message': f"父级编码 '{item.parent_key_value}' 不存在"
                            })
                            fail_count += 1
                            continue
                
                # 计算层级和路径
                level = item.level or 1
                path = item.key_value
                
                if parent_id:
                    parent_enum = self.get(db, parent_id)
                    if parent_enum:
                        level = (parent_enum.level or 0) + 1
                        path = f"{parent_enum.path}/{item.key_value}" if parent_enum.path else f"{parent_enum.key_value}/{item.key_value}"
                
                # 创建枚举对象
                enum_dict = {
                    'type_id': type_id,
                    'parent_id': parent_id,
                    'key_value': item.key_value,
                    'dict_value': item.dict_value,
                    'sort_order': item.sort_order or 0,
                    'level': level,
                    'path': path,
                    'status': True
                }
                
                enum_obj = self.create(db, obj_in=enum_dict)
                key_to_id_map[item.key_value] = enum_obj.id
                success_count += 1
                
            except Exception as e:
                errors.append({
                    'row': index + 1,
                    'message': f"创建失败: {str(e)}"
                })
                fail_count += 1
        
        if fail_count == 0:
            message = f"导入成功，共导入 {success_count} 条数据"
        else:
            message = f"导入失败，{fail_count} 条数据导入失败"
        
        return BatchImportResult(
            success=fail_count == 0,
            message=message,
            success_count=success_count,
            fail_count=fail_count,
            errors=errors if errors else None
        )


dictionary_type_crud = CRUDDictionaryType(DictionaryType)
dictionary_enum_crud = CRUDDictionaryEnum(DictionaryEnum)
