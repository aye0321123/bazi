#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 Railway 部署详情"""

import requests
import time

BASE_URL = "https://web-production-c59ea.up.railway.app"

print("🔍 检查 Railway 部署状态\n")

endpoints = [
    "/",
    "/health", 
    "/test",
    "/debug"
]

for endpoint in endpoints:
    url = f"{BASE_URL}{endpoint}"
    print(f"📡 测试: {url}")
    
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=15)
            print(f"   ✅ 状态码: {response.status_code}")
            
            if response.status_code == 200:
                content_preview = response.text[:200].replace('\n', ' ')
                print(f"   📄 内容预览: {content_preview}...")
            else:
                print(f"   ⚠️  响应: {response.text[:300]}")
            break
            
        except requests.exceptions.ConnectionError as e:
            print(f"   ⚠️  尝试 {attempt + 1}/3: 连接错误")
            if attempt < 2:
                time.sleep(2)
            else:
                print(f"   ❌ 最终失败: {str(e)[:100]}")
        except Exception as e:
            print(f"   ❌ 错误: {str(e)[:100]}")
            break
    
    print()

print("=" * 60)
print("💡 如果部分端点失败，可能是 Railway 正在重新部署")
print("   请等待 1-2 分钟后重试")
print("=" * 60)
