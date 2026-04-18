#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动本地 Flask 服务器
"""

import subprocess
import sys
import webbrowser
import time

print("=" * 60)
print("🚀 启动 BaziAI API 本地服务")
print("=" * 60)

print("\n📍 服务地址: http://127.0.0.1:5000")
print("💡 提示: 按 Ctrl+C 停止服务\n")
print("=" * 60)

# 等待 2 秒后自动打开浏览器
time.sleep(2)
try:
    webbrowser.open("http://127.0.0.1:5000")
    print("✅ 已在浏览器中打开")
except:
    print("⚠️  请手动访问: http://127.0.0.1:5000")

print("=" * 60)
print()

# 启动 Flask
subprocess.run([sys.executable, "app.py"])
