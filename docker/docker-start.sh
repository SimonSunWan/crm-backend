#!/bin/bash

# CRM后端系统Docker启动脚本
set -e

echo "🚀 启动CRM后端系统..."

# 进入docker目录
cd "$(dirname "$0")"

# 停止并删除现有容器
docker-compose down

# 构建并启动服务
docker-compose up --build -d

# 等待服务启动
sleep 10

# 运行数据库迁移
docker-compose exec crm-backend alembic upgrade head

echo "✅ CRM系统启动完成！"
echo "📖 API文档: http://localhost:8000/docs"
