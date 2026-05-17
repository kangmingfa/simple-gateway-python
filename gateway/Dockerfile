# ========================================
# Dockerfile for Gateway Service
# ========================================
# 构建镜像:
#   docker build -t gateway .
#
# 运行容器:
#   docker run -d \
#     -p 9000:9000 \
#     -e LLM_BACKEND_URL=http://backend:8000 \
#     gateway
#
# 访问接口 (通过 gateway 转发到后端):
#   curl http://localhost:9000/v1/model
# ========================================

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9000

# 后端 LLM 服务地址（可通过 docker run -e 覆盖）
ENV LLM_BACKEND_URL=http://localhost:8000

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "2", "app:app"]
