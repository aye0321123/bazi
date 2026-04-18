#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 ngrok URL"""

import requests

base_url = "https://map-debtor-crease.ngrok-free.dev"

endpoints = [
    "/",
    "/test",
    "/health",
    "/debug"
]

print("🧪 测试 ngrok URL...\n")

for endpoint in endpoints:
    url = f"{base_url}{endpoint}"
    print(f"测试: {url}")
    
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ 成功")
        else:
            print(f"  ⚠️  响应: {response.text[:200]}")
            
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    print()
