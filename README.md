# crm-backend

基于 FastAPI 的 CRM 后端系统。

## 目录结构

```
crm-backend/
├── app/                   # 应用主目录
│   ├── api/               # API路由模块
│   │   ├── auth.py        # 认证相关API
│   │   ├── dictionary.py  # 字典管理API
│   │   ├── menu.py        # 菜单管理API
│   │   ├── order.py       # 工单管理API
│   │   ├── role.py        # 角色管理API
│   │   ├── system.py      # 系统设置API
│   │   └── user.py        # 用户管理API
│   ├── core/              # 核心功能模块
│   │   ├── auth.py        # 认证逻辑
│   │   ├── config.py      # 配置管理
│   │   ├── crud.py        # CRUD基类
│   │   ├── crud_helpers.py# CRUD辅助函数
│   │   ├── database.py    # 数据库连接
│   │   ├── deps.py        # 依赖注入
│   │   ├── exceptions.py  # 自定义异常
│   │   ├── id_generator.py# ID生成器
│   │   ├── middleware.py  # 中间件
│   │   ├── response_helpers.py # 响应辅助函数
│   │   └── validators.py  # 数据验证
│   ├── crud/              # 数据访问层
│   │   ├── dictionary.py  # 字典CRUD操作
│   │   ├── menu.py        # 菜单CRUD操作
│   │   ├── order.py       # 工单CRUD操作
│   │   ├── role.py        # 角色CRUD操作
│   │   ├── system.py      # 系统设置CRUD操作
│   │   └── user.py        # 用户CRUD操作
│   ├── models/            # 数据库模型
│   │   ├── base.py        # 基础模型
│   │   ├── dictionary.py  # 字典模型
│   │   ├── menu.py        # 菜单模型
│   │   ├── order.py       # 工单模型
│   │   ├── role.py        # 角色模型
│   │   ├── role_menu.py   # 角色菜单关联表
│   │   ├── system.py      # 系统设置模型
│   │   ├── user.py        # 用户模型
│   │   └── user_role.py   # 用户角色关联表
│   ├── schemas/           # Pydantic模式
│   │   ├── base.py        # 基础模式
│   │   ├── dictionary.py  # 字典模式
│   │   ├── menu.py        # 菜单模式
│   │   ├── order.py       # 工单模式
│   │   ├── role.py        # 角色模式
│   │   ├── system.py      # 系统设置模式
│   │   └── user.py        # 用户模式
│   └── main.py            # 应用入口
├── alembic/               # 数据库迁移
│   ├── versions/          # 迁移版本文件
│   ├── env.py             # Alembic环境配置
│   └── script.py.mako     # 迁移脚本模板
├── scripts/               # 脚本文件
│   ├── init_menu.py       # 初始化菜单
│   ├── init_super.py      # 初始化超级管理员
│   └── init_system.py     # 系统码生成器
├── venv/                  # 虚拟环境
├── alembic.ini            # Alembic配置
├── pyproject.toml         # 项目配置
├── requirements.txt       # 依赖列表
└── README.md              # 项目说明
```

### 模块说明

- **api/**: 包含所有API路由，处理HTTP请求和响应
- **core/**: 核心功能模块，包含认证、配置、数据库连接等基础功能
- **crud/**: 数据访问层，封装数据库操作逻辑
- **models/**: SQLAlchemy数据库模型，定义表结构
- **schemas/**: Pydantic模式，用于数据验证和序列化
- **alembic/**: 数据库迁移管理
- **scripts/**: 各种初始化和管理脚本

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

## 常用指令
pip index versions redis # 检查最新版本

## API文档

访问 http://localhost:8000/docs 查看API文档。
