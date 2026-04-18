#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取 BaziAI 聊天记录
"""

import urllib3
import json
import ssl
from datetime import datetime

# 禁用警告
urllib3.disable_warnings()

# 创建 SSL 上下文
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 创建 HTTP 客户端
http = urllib3.PoolManager(
    ssl_context=ctx,
    cert_reqs='CERT_NONE',
    assert_hostname=False
)

# 读取 Cookie
with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)
    cookie = creds['cookie']

# Session ID
session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"

print("=" * 80)
print("📜 获取 BaziAI 聊天记录")
print("=" * 80)

# 请求 URL
url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print(f"\n🔗 Session ID: {session_id}")
print(f"📡 正在获取聊天记录...\n")

try:
    response = http.request('GET', url, headers=headers, timeout=10.0)
    
    if response.status == 200:
        messages = json.loads(response.data.decode('utf-8'))
        
        print(f"✅ 成功获取 {len(messages)} 条消息\n")
        print("=" * 80)
        
        # 显示所有消息
        for i, msg in enumerate(messages, 1):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            created_at = msg.get('created_at', '')
            
            # 格式化角色
            if role == 'user':
                role_icon = "👤 用户"
            elif role == 'assistant':
                role_icon = "🤖 AI"
            else:
                role_icon = f"❓ {role}"
            
            print(f"\n[{i}] {role_icon}")
            if created_at:
                print(f"⏰ 时间: {created_at}")
            print(f"💬 内容:\n{content}")
            print("-" * 80)
        
        # 保存到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 聊天记录已保存到: {filename}")
        
    else:
        print(f"❌ 请求失败，状态码: {response.status}")
        
except Exception as e:
    print(f"❌ 错误: {e}")

print("\n" + "=" * 80)
