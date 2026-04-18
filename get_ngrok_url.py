#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""获取 ngrok 公网 URL"""

import requests

try:
    # ngrok 提供了一个本地 API 来查询隧道信息
    response = requests.get("http://127.0.0.1:4040/api/tunnels")
    data = response.json()
    
    if data.get('tunnels'):
        for tunnel in data['tunnels']:
            if tunnel.get('proto') == 'https':
                public_url = tunnel.get('public_url')
                print(f"\n✅ 找到 ngrok 公网地址：")
                print(f"🌐 {public_url}")
                print(f"\n📋 可用页面：")
                print(f"   主页：{public_url}")
                print(f"   测试页面：{public_url}/test")
                print(f"   调试页面：{public_url}/debug")
                print(f"   健康检查：{public_url}/health")
                break
    else:
        print("❌ 未找到 ngrok 隧道")
        
except Exception as e:
    print(f"❌ 获取失败: {e}")
    print("\n💡 请确保 ngrok 正在运行")
