# crm-backend

一个基于FastAPI的CRM后端系统。

## 特性

- FastAPI + SQLAlchemy + Pydantic
- JWT认证
- 用户管理
- 客户管理
- 数据库迁移

## 字段命名转换

本项目支持数据库字段下划线和前端驼峰命名的自动转换：

### 数据库字段（下划线）
```python
# 数据库模型
class User(Base):
    user_name = Column(String)
    nick_name = Column(String)
    status = Column(Boolean)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    create_by = Column(String)
    update_by = Column(String)
```

### API响应（驼峰）
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "id": 1,
    "userName": "john_doe",
    "nickName": "John Doe",
    "status": true,
    "createTime": "2024-01-01T00:00:00",
    "updateTime": "2024-01-01T00:00:00",
    "createBy": "admin",
    "updateBy": "admin"
  }
}
```

### 实现方式

使用Pydantic的`alias_generator`自动转换：

```python
class CamelCaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel_case,
        populate_by_name=True,
        from_attributes=True
    )
```

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑.env文件
```

3. 运行数据库迁移：
```bash
alembic upgrade head
```

4. 启动服务：
```bash
uvicorn app.main:app --reload
```

## API文档

访问 http://localhost:8000/docs 查看API文档。
