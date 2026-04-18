#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 ngrok 启动 Flask 应用
自动创建公网访问地址
"""

from pyngrok import ngrok
import subprocess
import time
import sys
import os

print("=" * 60)
print("🚀 启动 BaziAI API 服务（带 ngrok 内网穿透）")
print("=" * 60)

# 设置 ngrok authtoken
ngrok.set_auth_token("3CTotAFNuw3LDtolUYnyQGRSsgE_7vYG8Y3V4yqJ2ytijHghE")

# 启动 Flask 应用（后台运行）
print("\n1️⃣ 启动 Flask 应用...")
flask_process = subprocess.Popen(
    [sys.executable, "app.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# 等待 Flask 启动
print("   等待 Flask 启动...")
time.sleep(3)

# 检查 Flask 是否成功启动
if flask_process.poll() is not None:
    print("   ❌ Flask 启动失败")
    sys.exit(1)

print("   ✅ Flask 已启动在 http://127.0.0.1:5000")

# 启动 ngrok
print("\n2️⃣ 启动 ngrok 隧道...")
try:
    # 创建 HTTP 隧道到端口 5000
    public_url = ngrok.connect(5000, bind_tls=True)
    print(f"   ✅ ngrok 隧道已建立")
    
    print("\n" + "=" * 60)
    print("🎉 服务已启动！")
    print("=" * 60)
    print(f"\n📍 本地地址: http://127.0.0.1:5000")
    print(f"🌐 公网地址: {public_url}")
    print("\n💡 提示:")
    print("   - 使用公网地址可以从任何地方访问你的 API")
    print("   - 按 Ctrl+C 停止服务")
    print("=" * 60)
    
    # 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  正在停止服务...")
        
except Exception as e:
    print(f"   ❌ ngrok 启动失败: {e}")
    print("\n💡 可能需要设置 authtoken:")
    print("   1. 访问: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("   2. 注册/登录获取 authtoken")
    print("   3. 在脚本中设置: ngrok.set_auth_token('你的token')")
    
finally:
    # 清理
    print("   关闭 ngrok...")
    ngrok.kill()
    print("   关闭 Flask...")
    flask_process.terminate()
    flask_process.wait()
    print("✅ 服务已停止")
