#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查测试会话是否有 AI 回复
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

# 检查测试会话
session_id = "21c9eb58-6c9d-49bb-a95b-7c0e1009e35d"
url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"

response = http.request('GET', url, headers={'Cookie': cookie})
messages = json.loads(response.data.decode('utf-8'))

print(f"会话 ID: {session_id}")
print(f"消息数: {len(messages)}")
print("\n消息列表:")
for i, msg in enumerate(messages, 1):
    role = "👤 用户" if msg['role'] == 'user' else "🤖 AI"
    content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
    print(f"\n{i}. {role}")
    print(f"   {content}")

if len(messages) > 1:
    print("\n✅ AI 已回复！")
else:
    print("\n❌ AI 未回复")
    print("\n请访问官网查看:")
    print(f"https://www.bazi-ai.com/zh/chat/{session_id}")
