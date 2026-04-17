#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动准备部署文件
"""

import os
import subprocess

def run_command(command):
    """运行命令"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("="*60)
    print("  🔮 天机阁部署准备工具")
    print("="*60)
    print()
    
    # 1. 检查 Git
    print("[1/5] 检查 Git...")
    success, stdout, stderr = run_command("git --version")
    if success:
        print(f"✅ Git 已安装: {stdout.strip()}")
    else:
        print("❌ Git 未安装")
        print("请访问 https://git-scm.com/downloads 安装 Git")
        return
    
    # 2. 初始化 Git 仓库
    print("\n[2/5] 初始化 Git 仓库...")
    if os.path.exists('.git'):
        print("✅ Git 仓库已存在")
    else:
        success, stdout, stderr = run_command("git init")
        if success:
            print("✅ Git 仓库初始化成功")
        else:
            print(f"❌ 初始化失败: {stderr}")
            return
    
    # 3. 创建 .gitignore
    print("\n[3/5] 创建 .gitignore...")
    gitignore_content = """# Python
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
    print("✅ .gitignore 已创建")
    
    # 4. 添加文件到 Git
    print("\n[4/5] 添加文件到 Git...")
    run_command("git add .")
    success, stdout, stderr = run_command('git commit -m "准备部署到云端"')
    if success or "nothing to commit" in stderr:
        print("✅ 文件已提交")
    else:
        print(f"⚠️  提交信息: {stderr}")
    
    # 5. 显示部署选项
    print("\n[5/5] 部署选项")
    print("="*60)
    print()
    
    print("📦 你的项目已准备好部署！")
    print()
    print("选择部署方式：")
    print()
    
    print("🚀 方式 1: Railway（最推荐）")
    print("   - 完全免费（$5 免费额度/月）")
    print("   - 部署超级简单（3 分钟完成）")
    print("   - 自动 HTTPS")
    print()
    print("   步骤：")
    print("   1. 创建 GitHub 仓库")
    print("   2. 推送代码：")
    print("      git remote add origin https://github.com/你的用户名/bazi-ai.git")
    print("      git branch -M main")
    print("      git push -u origin main")
    print("   3. 访问 https://railway.app")
    print("   4. 选择 'Deploy from GitHub repo'")
    print("   5. 选择你的仓库")
    print()
    
    print("🎨 方式 2: Render")
    print("   - 完全免费")
    print("   - 有休眠限制（15分钟无活动后休眠）")
    print()
    print("   步骤：")
    print("   1. 推送代码到 GitHub（同上）")
    print("   2. 访问 https://render.com")
    print("   3. 创建 Web Service")
    print("   4. 连接 GitHub 仓库")
    print()
    
    print("🐳 方式 3: Docker（本地或服务器）")
    print("   - 适合有服务器的用户")
    print("   - 完全控制")
    print()
    print("   步骤：")
    print("   docker-compose up -d")
    print()
    
    print("🇨🇳 方式 4: 阿里云/腾讯云")
    print("   - 国内访问快")
    print("   - 学生价约 ¥10/月")
    print()
    print("   详见：云端部署指南.md")
    print()
    
    print("="*60)
    print()
    print("📚 更多信息：")
    print("   - 云端部署指南.md - 详细部署教程")
    print("   - README.md - 项目说明")
    print("   - 快速开始.md - 快速上手")
    print()
    print("✅ 准备完成！选择一个方式开始部署吧！")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
