#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天机阁一键部署脚本
支持多个云平台的自动化部署
"""

import os
import sys
import subprocess
import json

def print_header(text):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(step, text):
    """打印步骤"""
    print(f"\n[步骤 {step}] {text}")
    print("-" * 60)

def run_command(command, cwd=None):
    """运行命令"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def check_git():
    """检查 Git 是否安装"""
    success, output = run_command("git --version")
    return success

def check_docker():
    """检查 Docker 是否安装"""
    success, output = run_command("docker --version")
    return success

def init_git():
    """初始化 Git 仓库"""
    print_step(1, "初始化 Git 仓库")
    
    # 检查是否已经是 Git 仓库
    if os.path.exists('.git'):
        print("✅ Git 仓库已存在")
        return True
    
    # 初始化
    success, output = run_command("git init")
    if not success:
        print(f"❌ Git 初始化失败: {output}")
        return False
    
    print("✅ Git 仓库初始化成功")
    
    # 添加 .gitignore
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Flask
instance/
.webassets-cache

# 敏感信息
bazi_credentials.json
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content.strip())
    
    print("✅ .gitignore 文件已创建")
    
    # 添加所有文件
    run_command("git add .")
    run_command('git commit -m "Initial commit for deployment"')
    
    print("✅ 文件已提交到 Git")
    return True

def deploy_to_railway():
    """部署到 Railway"""
    print_header("🚂 部署到 Railway")
    
    print("""
Railway 是最简单的部署方式！

步骤：
1. 访问 https://railway.app
2. 使用 GitHub 登录
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择你的仓库
6. Railway 会自动检测并部署

完成后，Railway 会提供一个 URL，例如：
https://bazi-ai-production.up.railway.app

按任意键继续...
""")
    input()
    
    # 打开 Railway 网站
    import webbrowser
    webbrowser.open('https://railway.app')
    
    print("✅ 已在浏览器中打开 Railway")

def deploy_to_render():
    """部署到 Render"""
    print_header("🎨 部署到 Render")
    
    print("""
Render 提供免费的 Web 服务！

步骤：
1. 访问 https://render.com
2. 注册账号
3. 点击 "New +" → "Web Service"
4. 连接你的 GitHub 仓库
5. 配置：
   - Name: bazi-ai
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
6. 点击 "Create Web Service"

完成后，Render 会提供一个 URL，例如：
https://bazi-ai.onrender.com

按任意键继续...
""")
    input()
    
    # 打开 Render 网站
    import webbrowser
    webbrowser.open('https://render.com')
    
    print("✅ 已在浏览器中打开 Render")

def deploy_to_docker():
    """使用 Docker 部署"""
    print_header("🐳 使用 Docker 部署")
    
    if not check_docker():
        print("❌ Docker 未安装")
        print("\n请先安装 Docker:")
        print("  Windows/Mac: https://www.docker.com/products/docker-desktop")
        print("  Linux: curl -fsSL https://get.docker.com | sh")
        return False
    
    print("✅ Docker 已安装")
    
    print_step(1, "构建 Docker 镜像")
    success, output = run_command("docker build -t bazi-ai .")
    if not success:
        print(f"❌ 构建失败: {output}")
        return False
    print("✅ 镜像构建成功")
    
    print_step(2, "启动容器")
    success, output = run_command("docker-compose up -d")
    if not success:
        print(f"❌ 启动失败: {output}")
        return False
    print("✅ 容器启动成功")
    
    print("\n" + "="*60)
    print("🎉 部署成功！")
    print("="*60)
    print("\n访问: http://localhost:5000")
    print("\n查看日志: docker-compose logs -f")
    print("停止服务: docker-compose down")
    
    return True

def deploy_to_github():
    """推送到 GitHub"""
    print_header("📦 推送到 GitHub")
    
    print("请输入你的 GitHub 仓库地址")
    print("格式: https://github.com/用户名/仓库名.git")
    repo_url = input("\nGitHub 仓库地址: ").strip()
    
    if not repo_url:
        print("❌ 仓库地址不能为空")
        return False
    
    print_step(1, "添加远程仓库")
    run_command("git remote remove origin")  # 删除旧的
    success, output = run_command(f"git remote add origin {repo_url}")
    if not success:
        print(f"❌ 添加失败: {output}")
        return False
    print("✅ 远程仓库已添加")
    
    print_step(2, "推送到 GitHub")
    success, output = run_command("git push -u origin main")
    if not success:
        # 尝试 master 分支
        success, output = run_command("git branch -M main")
        success, output = run_command("git push -u origin main")
        if not success:
            print(f"❌ 推送失败: {output}")
            print("\n可能的原因:")
            print("1. 仓库地址错误")
            print("2. 没有权限")
            print("3. 需要先在 GitHub 上创建仓库")
            return False
    
    print("✅ 代码已推送到 GitHub")
    print(f"\n仓库地址: {repo_url}")
    
    return True

def create_readme():
    """创建 README.md"""
    readme_content = """# 🔮 天机阁 - BaziAI Web 应用

基于 Flask 的 BaziAI API Web 界面，提供友好的用户体验。

## ✨ 功能特性

- 🆕 创建新对话
- 💬 发送和接收消息
- 🔄 实时刷新对话
- 📥 导出聊天记录
- 🎨 精美的中国风界面

## 🚀 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# 访问
http://localhost:5000
```

### Docker 运行

```bash
# 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

## 📚 文档

- [快速开始](快速开始.md)
- [使用说明](天机阁使用说明.md)
- [API 文档](API_DOCUMENTATION.md)
- [部署指南](云端部署指南.md)

## 🌐 部署到云端

支持多种部署方式：

- **Railway** - 推荐，免费且简单
- **Render** - 免费，有休眠限制
- **Docker** - 适合有服务器的用户
- **阿里云/腾讯云** - 国内访问快

详见 [云端部署指南](云端部署指南.md)

## 📝 使用方法

1. 访问应用 URL
2. 粘贴你的 Cookie（从 BaziAI 官网获取）
3. 点击"✨ 新对话"创建对话
4. 开始使用

## 🔒 安全提示

- 不要分享你的 Cookie
- 不要将 `bazi_credentials.json` 上传到公共仓库
- 定期更新 Cookie

## 📄 许可证

MIT License

## 🙏 致谢

感谢 BaziAI 提供的 API 服务。
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README.md 已创建")

def main():
    """主函数"""
    print_header("🔮 天机阁一键部署工具")
    
    print("""
欢迎使用天机阁一键部署工具！

本工具将帮助你快速部署到云端。

支持的平台：
1. Railway（推荐）- 免费且简单
2. Render - 免费，有休眠限制
3. Docker - 本地或服务器部署
4. GitHub - 推送代码到 GitHub

请选择部署方式：
""")
    
    print("1. 部署到 Railway（推荐）")
    print("2. 部署到 Render")
    print("3. 使用 Docker 本地部署")
    print("4. 推送到 GitHub")
    print("5. 全部准备（Git + GitHub + 部署指南）")
    print("0. 退出")
    
    choice = input("\n请输入选项 (0-5): ").strip()
    
    if choice == "0":
        print("\n👋 再见！")
        return
    
    # 检查 Git
    if not check_git():
        print("\n❌ Git 未安装")
        print("请先安装 Git: https://git-scm.com/downloads")
        return
    
    print("\n✅ Git 已安装")
    
    # 创建 README
    create_readme()
    
    # 初始化 Git
    if not init_git():
        print("\n❌ Git 初始化失败")
        return
    
    # 根据选择执行
    if choice == "1":
        deploy_to_railway()
    elif choice == "2":
        deploy_to_render()
    elif choice == "3":
        deploy_to_docker()
    elif choice == "4":
        deploy_to_github()
    elif choice == "5":
        print_header("📦 完整准备流程")
        
        # 推送到 GitHub
        if deploy_to_github():
            print("\n✅ 代码已推送到 GitHub")
            
            # 选择部署平台
            print("\n现在选择部署平台：")
            print("1. Railway")
            print("2. Render")
            
            platform = input("\n请选择 (1-2): ").strip()
            
            if platform == "1":
                deploy_to_railway()
            elif platform == "2":
                deploy_to_render()
    else:
        print("\n❌ 无效的选项")
    
    print("\n" + "="*60)
    print("📚 更多信息请查看:")
    print("  - 云端部署指南.md")
    print("  - DEPLOYMENT.md")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 部署已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
