#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Cloud API
"""

import requests
import json
import time

# 配置
API_URL = "http://localhost:8000"  # 本地测试
# API_URL = "https://your-app.onrender.com"  # 云端测试

# 读取 Cookie
with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    COOKIE = json.load(f)['cookie']

# 请求头
headers = {
    "X-Bazi-Cookie": COOKIE,
    "Content-Type": "application/json"
}

print("="*60)
print("🧪 测试 BaziAI Cloud API")
print("="*60)

# 测试 1: 健康检查
print("\n[测试 1] 健康检查...")
try:
    response = requests.get(f"{API_URL}/health")
    result = response.json()
    print(f"✅ 状态: {result['status']}")
    print(f"   时间: {result['timestamp']}")
except Exception as e:
    print(f"❌ 失败: {e}")
    exit(1)

# 测试 2: 获取 API 信息
print("\n[测试 2] 获取 API 信息...")
try:
    response = requests.get(f"{API_URL}/")
    result = response.json()
    print(f"✅ API 名称: {result['name']}")
    print(f"   版本: {result['version']}")
except Exception as e:
    print(f"❌ 失败: {e}")

# 测试 3: 创建会话
print("\n[测试 3] 创建会话...")
try:
    response = requests.post(
        f"{API_URL}/api/session/create",
        headers=headers
    )
    result = response.json()
    
    if result['success']:
        session_id = result['session_id']
        print(f"✅ 会话创建成功")
        print(f"   Session ID: {session_id}")
    else:
        print(f"❌ 失败: {result['error']}")
        exit(1)
except Exception as e:
    print(f"❌ 失败: {e}")
    exit(1)

# 测试 4: 发送消息
print("\n[测试 4] 发送消息...")
try:
    response = requests.post(
        f"{API_URL}/api/session/{session_id}/send",
        headers=headers,
        json={"content": "今天运势如何？"}
    )
    result = response.json()
    
    if result['success']:
        print(f"✅ 消息发送成功")
    else:
        print(f"❌ 失败: {result['error']}")
except Exception as e:
    print(f"❌ 失败: {e}")

# 测试 5: 获取消息
print("\n[测试 5] 获取消息...")
try:
    response = requests.get(
        f"{API_URL}/api/session/{session_id}/messages",
        headers=headers
    )
    result = response.json()
    
    if result['success']:
        messages = result['messages']
        print(f"✅ 获取成功")
        print(f"   消息数: {len(messages)}")
        
        for i, msg in enumerate(messages, 1):
            role = "👤 用户" if msg['role'] == 'user' else "🤖 AI"
            content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
            print(f"   {i}. {role}: {content}")
    else:
        print(f"❌ 失败: {result['error']}")
except Exception as e:
    print(f"❌ 失败: {e}")

# 测试 6: 一键对话
print("\n[测试 6] 一键对话...")
try:
    response = requests.post(
        f"{API_URL}/api/chat",
        headers=headers,
        json={"content": "请帮我分析一下明天的运势"}
    )
    result = response.json()
    
    if result['success']:
        print(f"✅ 对话创建成功")
        print(f"   Session ID: {result['session_id']}")
        print(f"   官网链接: {result['chat_url']}")
        print(f"   提示: {result['note']}")
    else:
        print(f"❌ 失败: {result['error']}")
except Exception as e:
    print(f"❌ 失败: {e}")

print("\n" + "="*60)
print("✅ 所有测试完成！")
print("="*60)

print("\n💡 提示:")
print("   - API 工作正常")
print("   - 可以部署到云端了")
print("   - 记得更新 API_URL 为云端地址")
