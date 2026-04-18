#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单测试 BaziAI API"""

import requests
import json

# 读取 Cookie
with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)
    cookie = creds['cookie']

# 测试 Session ID
session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"

print("=" * 60)
print("🧪 测试 BaziAI API")
print("=" * 60)

# 测试获取消息
url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print(f"\n📡 请求 URL: {url}")
print(f"🔑 Cookie 长度: {len(cookie)} 字符")

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"\n✅ 状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 成功获取 {len(data)} 条消息")
        print("\n📋 最近的消息：")
        for msg in data[-3:]:  # 显示最后3条
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')[:50]
            print(f"   {role}: {content}...")
    else:
        print(f"❌ 请求失败: {response.text[:200]}")
        
except Exception as e:
    print(f"\n❌ 错误: {e}")

print("\n" + "=" * 60)
