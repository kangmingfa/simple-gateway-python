# ========================================
# Dockerfile for Django Simple Gateway
# ========================================
# 构建镜像:
#   docker build -t django-gateway .
#
# 运行容器 (通过环境变量注入 SERVER_ID 和 MODEL_NAME):
#   docker run -d \
#     -p 8000:8000 \
#     -e SERVER_ID=server-001 \
#     -e MODEL_NAME=gpt-4 \
#     django-gateway
#
# 访问接口:
#   curl http://localhost:8000/v1/model
# ========================================

FROM python:3.11-slim

# 设置环境变量：防止生成 .pyc 文件，并确保日志实时输出
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 默认的 SERVER_ID 和 MODEL_NAME（可通过 docker run -e 覆盖）
ENV SERVER_ID=unknown
ENV MODEL_NAME=unknown

# 使用 gunicorn 启动 Django 服务
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app.wsgi:application"]
