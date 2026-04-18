FROM python:3.11-slim

WORKDIR /app

# 安装 Chrome 和依赖（用于 Selenium）
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用文件
COPY . .

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
ENV CHROME_BIN=/usr/bin/google-chrome
ENV DISPLAY=:99

# 启动应用（使用 $PORT 环境变量，默认 5000）
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 app:app
