FROM python:3.11-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用文件
COPY . .

# 暴露端口（Railway 会使用动态端口）
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# 启动应用（使用 $PORT 环境变量）
CMD gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
