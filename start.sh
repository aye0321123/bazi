#!/bin/bash

echo "🔮 启动 BaziAI Web 应用..."
echo "================================"

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    echo "请先安装 Python 3.7 或更高版本"
    exit 1
fi

# 检查依赖是否安装
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 安装依赖..."
    pip3 install -r requirements.txt
fi

# 设置环境变量
export FLASK_APP=app.py
export FLASK_ENV=development

# 启动应用
echo "✅ 启动成功！"
echo "================================"
echo "访问地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务"
echo "================================"

python3 app.py
