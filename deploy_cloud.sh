#!/bin/bash

echo "=========================================="
echo "🚀 BaziAI Cloud API 部署脚本"
echo "=========================================="

# 检查 git
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 未安装 git"
    exit 1
fi

echo ""
echo "请选择部署方式:"
echo "1. 部署到 Render"
echo "2. 部署到 Heroku"
echo "3. 本地测试"
echo ""
read -p "请输入选项 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📦 准备部署到 Render..."
        echo ""
        echo "步骤:"
        echo "1. 创建 GitHub 仓库"
        echo "2. 推送代码"
        echo "3. 在 Render 上连接仓库"
        echo ""
        
        # 初始化 git
        if [ ! -d ".git" ]; then
            git init
            echo "✅ Git 仓库已初始化"
        fi
        
        # 添加文件
        git add cloud_api.py requirements_cloud.txt Procfile_cloud runtime.txt render_cloud.yaml CLOUD_API_README.md
        
        # 提交
        git commit -m "Add BaziAI Cloud API for Render deployment"
        
        echo ""
        echo "✅ 代码已准备好"
        echo ""
        echo "下一步:"
        echo "1. 在 GitHub 上创建新仓库"
        echo "2. 运行以下命令推送代码:"
        echo ""
        echo "   git remote add origin <your-repo-url>"
        echo "   git push -u origin main"
        echo ""
        echo "3. 访问 https://render.com"
        echo "4. 点击 'New +' → 'Web Service'"
        echo "5. 连接你的 GitHub 仓库"
        echo "6. 选择 render_cloud.yaml 配置"
        echo "7. 点击 'Create Web Service'"
        echo ""
        ;;
        
    2)
        echo ""
        echo "📦 准备部署到 Heroku..."
        echo ""
        
        # 检查 Heroku CLI
        if ! command -v heroku &> /dev/null; then
            echo "❌ 错误: 未安装 Heroku CLI"
            echo "请访问 https://devcenter.heroku.com/articles/heroku-cli 下载安装"
            exit 1
        fi
        
        # 重命名 Procfile
        if [ -f "Procfile_cloud" ]; then
            cp Procfile_cloud Procfile
            echo "✅ Procfile 已准备好"
        fi
        
        # 初始化 git
        if [ ! -d ".git" ]; then
            git init
            echo "✅ Git 仓库已初始化"
        fi
        
        # 添加文件
        git add cloud_api.py requirements_cloud.txt Procfile runtime.txt CLOUD_API_README.md
        
        # 提交
        git commit -m "Add BaziAI Cloud API for Heroku deployment"
        
        # 登录 Heroku
        echo ""
        echo "正在登录 Heroku..."
        heroku login
        
        # 创建应用
        echo ""
        read -p "请输入应用名称 (例如: bazi-cloud-api): " app_name
        heroku create $app_name
        
        # 部署
        echo ""
        echo "正在部署..."
        git push heroku main
        
        echo ""
        echo "✅ 部署完成！"
        echo ""
        echo "查看应用: heroku open"
        echo "查看日志: heroku logs --tail"
        echo ""
        ;;
        
    3)
        echo ""
        echo "🧪 本地测试..."
        echo ""
        
        # 检查 Python
        if ! command -v python &> /dev/null; then
            echo "❌ 错误: 未安装 Python"
            exit 1
        fi
        
        # 安装依赖
        echo "安装依赖..."
        pip install -r requirements_cloud.txt
        
        echo ""
        echo "✅ 依赖已安装"
        echo ""
        echo "启动服务..."
        echo ""
        python cloud_api.py
        ;;
        
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac
