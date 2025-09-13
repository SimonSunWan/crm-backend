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
    created_by = Column(String)
    updated_by = Column(String)
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

### Docker 部署（推荐）

1. 快速启动：
```bash
# 运行启动脚本
./docker/docker-start.sh
```

或手动启动：
```bash
cd docker
docker-compose up --build -d
sleep 10
docker-compose exec crm-backend alembic upgrade head
```

2. 服务架构：

| 服务 | 端口 | 描述 |
|------|------|------|
| crm-backend | 8000 | FastAPI应用 |
| postgres | 5432 | PostgreSQL数据库 |
| redis | 6379 | Redis缓存 |

3. 访问地址：
- **API文档**: http://localhost:8000/docs
- **ReDoc文档**: http://localhost:8000/redoc

4. 常用命令：
```bash
# 进入docker目录
cd docker

# 启动服务
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 数据库迁移
docker-compose exec crm-backend alembic upgrade head

# 进入容器
docker-compose exec crm-backend bash
```

5. 配置说明：
- 默认配置文件：`docker/docker.env`
- 生产环境：复制到`.env`并修改`SECRET_KEY`等配置
- 数据库：postgres/123456@localhost:5432/postgres

### 本地开发

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
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 宝塔面板部署（生产环境）

### 前置准备

1. **服务器要求**：
   - 操作系统：Alibaba Cloud Linux
   - 内存：至少 2GB RAM
   - 硬盘：至少 20GB 可用空间
   - Python 3.8+ 环境

2. **进入workbench连接服务器并下载宝塔** wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh ed8484bec

2. 阿里云服务器 -> 应用概详情 -> 端口放通

### 第一步：安装必要软件

1. **登录宝塔面板**：
   - 访问：`http://你的服务器IP:8888`
   - 使用安装时显示的账号密码登录

2. **安装软件环境**：
   - 进入 **软件商店**
   - 安装以下软件：
     - **Nginx** (1.20+)
     - **PostgreSQL** (12+)
     - **Redis** (6.0+)
     - **python环境管理器** (用于管理Python环境)

### 第二步：创建数据库（也可以不创建，用默认的postgres数据库）

1. **进入数据库管理**：
   - 点击 **数据库** → **添加数据库**
   ```
   数据库名：crm_backend
   用户名：crm_user
   密码：crm123456
   主机：localhost
   端口：5432
   ```

### 第三步：上传项目代码

1. **上传代码**：
   - **方式一**：压缩上传（推荐）
     - 压缩项目文件（**不要包含venv目录**）
     - 上传到 `/www/wwwroot/` 并解压
   - **方式二**：Git克隆
     - 进入 **文件** `/www/wwwroot/` **终端**
     ```bash
     git clone https://github.com/SimonSunWan/crm-backend.git
     cd crm-backend
     ```
   - 改.env宝塔数据库配置打开

### 第四步：配置Python环境

1. **创建Python项目**：
   - 进入 **网站** → **Python项目**
   - 点击 **添加项目**
   - 项目名称：`crm-backend`
   - 项目端口：`8000`
   - Python版本：`3.8+`（推荐3.13.7）
   - 启动方式：`命令行启动`
   - 项目路径：`/www/wwwroot/crm-backend`
   - 启动命令：`uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
   - 环境变量：选择 `从文件加载`，文件路径：`/www/wwwroot/crm-backend/.env`
   - 启动用户：`www`

2. **安装依赖**：
   - 在Python项目管理页面点击 **终端**
   - 执行以下命令：
     ```bash
     # 删除旧的venv目录（如果存在）
     rm -rf venv
     
     # 创建新的虚拟环境
     python3 -m venv venv
     
     # 激活虚拟环境
     source venv/bin/activate
     
     # 升级pip
     pip install --upgrade pip
     
     # 安装依赖
     pip install -r requirements.txt
     
     # 如果pip速度慢，使用国内源
     pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
     ```

### 第五步：数据库迁移

1. **执行数据库迁移**：
   ```bash
   # 在项目终端中执行
   cd /www/wwwroot/crm-backend
   source venv/bin/activate

   # python环境变量
   export PYTHONPATH=/www/wwwroot/crm-backend:$PYTHONPATH
   
   # 初始化数据库
   alembic upgrade head
   
   # 初始化系统数据
   python scripts/init_super.py
   python scripts/init_menu.py
   python scripts/init_system.py
   ```

### 第六步：启动服务

   - 安全 -> 系统防火墙 -> 添加端口规则
   - 软件商店 -> PostgreSQL管理器 -> 数据库列表 -> 修改Postgres密码
   - 软件商店 -> PostgreSQL管理器 -> 配置修改 -> listen_addresses = '*'
   - HTML项目管理 -> 配置文件 -> 
   ```
    #禁止访问的文件或目录
    location ~ ^/(\.user.ini|\.htaccess|\.git|\.env|\.svn|\.project|LICENSE|README.md) {
        return 404;
    }
    # API反向代理配置
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
   ```

### 注意事项
   
   **如果不知道密码：单用户模式重置密码**：
   # 切换到postgres用户
   su - postgres
   # 以postgres用户身份启动单用户模式
   /www/server/pgsql/bin/postgres --single -D /www/server/pgsql/data postgres
   ALTER USER postgres PASSWORD '123456';
   \q


### 常用指令

pip index versions redis # 检查最新版本

psql
\l
\c postgres
\dt
\d 表名
SELECT * FROM 表名;
SELECT * FROM 表名 LIMIT 10;
\q

### 域名解析

1. 购买域名的网站添加记录值：外网ip
2. 宝塔点击网站 -> 设置 -> 域名管理（前后端项目设置成不一样的）
3. 宝塔后端项目外网映射打开
4. 宝塔后端项目SSL点击"Let's Encrypt"
5. 完成ICP备案

## API文档

访问 http://localhost:8000/docs 查看API文档。
