#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查特定会话的内容
"""

import urllib3
import json
import ssl

urllib3.disable_warnings()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

http = urllib3.PoolManager(ssl_context=ctx, cert_reqs='CERT_NONE')

with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)
    cookie = creds['cookie']

# 检查指定会话
session_id = "d8baa1e8-a0b8-493b-8c10-20aab29f4270"
url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"

print("=" * 80)
print(f"🔍 检查会话: {session_id}")
print("=" * 80)

try:
    response = http.request('GET', url, headers={'Cookie': cookie})
    messages = json.loads(response.data.decode('utf-8'))

    print(f"\n📊 消息数: {len(messages)}")
    print("\n" + "=" * 80)
    print("💬 完整对话:")
    print("=" * 80)
    
    for i, msg in enumerate(messages, 1):
        role = "👤 用户" if msg['role'] == 'user' else "🤖 AI"
        time = msg.get('created_at', 'N/A')
        content = msg['content']
        
        print(f"\n{i}. {role} ({time})")
        print("-" * 80)
        print(content)
        print("-" * 80)

    # 统计
    user_count = sum(1 for msg in messages if msg['role'] == 'user')
    ai_count = sum(1 for msg in messages if msg['role'] == 'assistant')
    
    print("\n" + "=" * 80)
    print("📈 统计信息:")
    print("=" * 80)
    print(f"总消息数: {len(messages)}")
    print(f"用户消息: {user_count}")
    print(f"AI 回复: {ai_count}")
    
    if ai_count > 0:
        print(f"\n✅ 这个会话有 AI 回复！")
        print(f"回复率: {ai_count/user_count*100:.1f}%")
    else:
        print(f"\n❌ 这个会话没有 AI 回复")
    
    print("\n" + "=" * 80)

except Exception as e:
    print(f"\n❌ 错误: {e}")
