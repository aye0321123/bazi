#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib3, json, ssl

urllib3.disable_warnings()
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
http = urllib3.PoolManager(ssl_context=ctx, cert_reqs='CERT_NONE')

with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    cookie = json.load(f)['cookie']

session_id = "3cc68c66-62ae-47d8-9771-d4493ffb43b9"
url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"

response = http.request('GET', url, headers={'Cookie': cookie})
messages = json.loads(response.data.decode('utf-8'))

print(f"会话: {session_id}")
print(f"消息数: {len(messages)}\n")

for i, msg in enumerate(messages, 1):
    role = "👤 用户" if msg['role'] == 'user' else "🤖 AI"
    print(f"{i}. {role}: {msg['content'][:100]}")

print(f"\n官网链接: https://www.bazi-ai.com/zh/chat/{session_id}")
