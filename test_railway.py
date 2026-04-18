#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 Railway 部署"""

import requests

BASE_URL = "https://web-production-c59ea.up.railway.app"

print("=" * 60)
print("🧪 测试 Railway 部署")
print("=" * 60)

# 测试 1: 健康检查
print("\n1️⃣ 测试健康检查端点...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.text}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试 2: 首页
print("\n2️⃣ 测试首页...")
try:
    response = requests.get(BASE_URL, timeout=10)
    print(f"   状态码: {response.status_code}")
    print(f"   响应长度: {len(response.text)} 字符")
    if response.status_code == 200:
        print("   ✅ 首页加载成功")
    else:
        print(f"   ❌ 首页加载失败")
        print(f"   响应内容: {response.text[:500]}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试 3: 测试页面
print("\n3️⃣ 测试测试页面...")
try:
    response = requests.get(f"{BASE_URL}/test", timeout=10)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ 测试页面加载成功")
    else:
        print(f"   ❌ 测试页面加载失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n" + "=" * 60)
print("✅ 测试完成")
print("=" * 60)
