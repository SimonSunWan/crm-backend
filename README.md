# CRM Backend

一个基于FastAPI的CRM系统后端API。

## 功能特性

- 用户管理
- 客户管理
- RESTful API
- 数据库迁移
- 自动生成API文档

## 技术栈

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic

## 安装和运行

1. 克隆项目
```bash
git clone <repository-url>
cd crm-backend
```

2. 创建虚拟环境
```bash
python -m venv venv
```

3. 激活虚拟环境
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. 安装依赖
```bash
pip install -r requirements.txt
```

5. 配置环境变量
```bash
cp env.example .env
# 编辑.env文件，配置数据库连接等信息
```

6. 运行数据库迁移
```bash
alembic upgrade head
```

7. 启动服务器
```bash
uvicorn app.main:app --reload
```

## API文档

启动服务器后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
crm-backend/
├── app/
│   ├── api/
│   │   ├── users.py
│   │   ├── customers.py
│   │   └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── user.py
│   │   └── customer.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── customer.py
│   └── main.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── requirements.txt
├── alembic.ini
└── README.md
```

## 开发

### 创建新的数据库迁移

```bash
alembic revision --autogenerate -m "描述"
alembic upgrade head
```

### 运行测试

```bash
pytest
```
