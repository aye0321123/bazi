#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用 urllib3 测试"""

import urllib3
import json
import ssl

# 禁用警告
urllib3.disable_warnings()

# 读取 Cookie
with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)
    cookie = creds['cookie']

session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"
url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"

print("=" * 60)
print("🧪 使用 urllib3 测试")
print("=" * 60)

# 创建自定义的 SSL 上下文
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 创建 PoolManager
http = urllib3.PoolManager(
    ssl_context=ctx,
    cert_reqs='CERT_NONE',
    assert_hostname=False
)

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print(f"\n📡 请求 URL: {url}")

try:
    response = http.request('GET', url, headers=headers, timeout=10.0)
    print(f"\n✅ 状态码: {response.status}")
    
    if response.status == 200:
        data = json.loads(response.data.decode('utf-8'))
        print(f"✅ 成功获取 {len(data)} 条消息")
    else:
        print(f"❌ 请求失败")
        print(response.data.decode('utf-8')[:200])
        
except Exception as e:
    print(f"\n❌ 错误: {e}")
    print(f"错误类型: {type(e).__name__}")

print("\n" + "=" * 60)
