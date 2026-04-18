#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只启动 ngrok（Flask 需要单独运行）"""

from pyngrok import ngrok
import time

print("=" * 60)
print("🚀 启动 ngrok 隧道")
print("=" * 60)

# 设置 authtoken
ngrok.set_auth_token("3CTotAFNuw3LDtolUYnyQGRSsgE_7vYG8Y3V4yqJ2ytijHghE")

print("\n⚠️  请确保 Flask 已经在运行（python app.py）")
print("   等待 3 秒...")
time.sleep(3)

try:
    # 创建隧道
    public_url = ngrok.connect(5000, bind_tls=True)
    
    print("\n" + "=" * 60)
    print("🎉 ngrok 隧道已建立！")
    print("=" * 60)
    print(f"\n🌐 公网地址: {public_url}")
    print(f"\n📋 可用页面：")
    print(f"   主页：{public_url}")
    print(f"   测试页面：{public_url}/test")
    print(f"   调试页面：{public_url}/debug")
    print(f"   健康检查：{public_url}/health")
    print("\n💡 提示: 按 Ctrl+C 停止 ngrok")
    print("=" * 60)
    
    # 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  正在停止 ngrok...")
        
except Exception as e:
    print(f"\n❌ ngrok 启动失败: {e}")
    
finally:
    ngrok.kill()
    print("✅ ngrok 已停止")
