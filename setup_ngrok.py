#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ngrok 设置助手
帮助安装和配置 ngrok
"""

import os
import sys
import subprocess
import platform

print("=" * 60)
print("🚀 ngrok 设置助手")
print("=" * 60)

# 检查是否已安装 ngrok
def check_ngrok():
    try:
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✅ ngrok 已安装: {result.stdout.strip()}")
            return True
    except:
        pass
    
    print("❌ ngrok 未安装")
    return False

# 安装说明
def show_install_instructions():
    print("\n📦 ngrok 安装方法：")
    print("\n方法 1: 使用 Chocolatey (推荐)")
    print("   choco install ngrok")
    
    print("\n方法 2: 使用 Scoop")
    print("   scoop install ngrok")
    
    print("\n方法 3: 手动下载")
    print("   1. 访问: https://ngrok.com/download")
    print("   2. 下载 Windows 版本")
    print("   3. 解压到任意目录")
    print("   4. 将 ngrok.exe 所在目录添加到 PATH")
    
    print("\n方法 4: 使用 pip (pyngrok)")
    print("   pip install pyngrok")

# 配置 ngrok
def configure_ngrok():
    print("\n🔑 配置 ngrok authtoken:")
    print("1. 访问 https://dashboard.ngrok.com/get-started/your-authtoken")
    print("2. 注册/登录账号")
    print("3. 复制你的 authtoken")
    print("4. 运行: ngrok config add-authtoken <你的token>")

# 启动说明
def show_start_instructions():
    print("\n" + "=" * 60)
    print("🎯 启动步骤：")
    print("=" * 60)
    print("\n1️⃣ 确保本地 Flask 应用正在运行:")
    print("   python app.py")
    print("   (应该在 http://127.0.0.1:5000 运行)")
    
    print("\n2️⃣ 在新的终端窗口运行 ngrok:")
    print("   ngrok http 5000")
    
    print("\n3️⃣ ngrok 会显示一个公网 URL，例如:")
    print("   https://xxxx-xx-xx-xx-xx.ngrok-free.app")
    
    print("\n4️⃣ 使用这个 URL 访问你的应用！")
    print("=" * 60)

# 主程序
if __name__ == "__main__":
    if check_ngrok():
        print("\n✅ ngrok 已准备就绪！")
        show_start_instructions()
    else:
        show_install_instructions()
        print("\n" + "=" * 60)
        print("⚠️  请先安装 ngrok，然后重新运行此脚本")
        print("=" * 60)
