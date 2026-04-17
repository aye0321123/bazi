@echo off
chcp 65001 >nul
echo 🔮 启动 BaziAI Web 应用...
echo ================================

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo 请先安装 Python 3.7 或更高版本
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 📦 安装依赖...
    pip install -r requirements.txt
)

REM 启动应用
echo ✅ 启动成功！
echo ================================
echo 访问地址: http://localhost:5000
echo 按 Ctrl+C 停止服务
echo ================================

python app.py
