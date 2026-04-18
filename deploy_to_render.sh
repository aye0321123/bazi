#!/bin/bash

# 部署到 Render 的快速脚本

echo "🚀 开始部署到 Render..."
echo ""

# 检查 Git 状态
if [ -d .git ]; then
    echo "✅ Git 仓库已存在"
else
    echo "❌ 未找到 Git 仓库，正在初始化..."
    git init
    git add .
    git commit -m "Initial commit for Render deployment"
fi

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 发现未提交的更改，正在提交..."
    git add .
    git commit -m "Update for cloud deployment"
else
    echo "✅ 没有未提交的更改"
fi

# 检查远程仓库
if git remote | grep -q origin; then
    echo "✅ 远程仓库已配置"
    echo "📤 推送到 GitHub..."
    git push origin main || git push origin master
else
    echo "⚠️  未配置远程仓库"
    echo ""
    echo "请先配置 GitHub 仓库："
    echo "1. 在 GitHub 创建新仓库"
    echo "2. 运行以下命令："
    echo "   git remote add origin https://github.com/your-username/your-repo.git"
    echo "   git push -u origin main"
    echo ""
    exit 1
fi

echo ""
echo "✅ 代码已推送到 GitHub！"
echo ""
echo "📋 下一步："
echo "1. 访问 https://render.com"
echo "2. 使用 GitHub 账号登录"
echo "3. 点击 'New +' → 'Web Service'"
echo "4. 选择你的仓库"
echo "5. 配置如下："
echo "   - Name: bazi-ai-api"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn app:app --bind 0.0.0.0:\$PORT"
echo "6. 点击 'Create Web Service'"
echo ""
echo "⏱️  等待 5-10 分钟完成部署"
echo ""
echo "🎉 部署完成后，你会得到一个 URL，例如："
echo "   https://bazi-ai-api.onrender.com"
echo ""
