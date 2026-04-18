#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 BaziAI 的回复机制
"""

import urllib3
import json
import ssl
import time

# 禁用警告
urllib3.disable_warnings()

# 创建 SSL 上下文
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

http = urllib3.PoolManager(
    ssl_context=ctx,
    cert_reqs='CERT_NONE',
    assert_hostname=False
)

# 读取 Cookie
with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)
    cookie = creds['cookie']

session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"
base_url = "https://www.bazi-ai.com"

print("=" * 80)
print("🔍 分析 BaziAI 回复机制")
print("=" * 80)

# 步骤 1: 发送一条消息
print("\n📤 步骤 1: 发送测试消息...")

url = f"{base_url}/api/chat-session/{session_id}/messages"
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Cookie": cookie,
    "Origin": base_url,
    "Referer": f"{base_url}/zh/chat/{session_id}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

payload = {
    "session_id": session_id,
    "role": "user",
    "content": "请用一句话回复：今天天气怎么样",
    "id": ""
}

try:
    # 发送消息前，记录当前消息数量
    response = http.request('GET', url, headers=headers)
    messages_before = json.loads(response.data.decode('utf-8'))
    count_before = len(messages_before)
    print(f"   发送前消息数: {count_before}")
    
    # 发送消息
    response = http.request(
        'POST',
        url,
        headers=headers,
        body=json.dumps(payload).encode('utf-8')
    )
    
    if response.status == 200:
        result = json.loads(response.data.decode('utf-8'))
        print(f"   ✅ 消息发送成功")
        print(f"   返回数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
    else:
        print(f"   ❌ 发送失败: {response.status}")
        exit()
    
    # 步骤 2: 轮询检查 AI 回复
    print("\n🔄 步骤 2: 轮询检查 AI 回复...")
    
    max_attempts = 20
    for i in range(max_attempts):
        time.sleep(2)  # 等待 2 秒
        
        response = http.request('GET', url, headers=headers)
        messages_after = json.loads(response.data.decode('utf-8'))
        count_after = len(messages_after)
        
        print(f"   尝试 {i+1}/{max_attempts}: 当前消息数 = {count_after}")
        
        if count_after > count_before + 1:
            # 有新消息了
            print(f"\n   ✅ 检测到 AI 回复！")
            
            # 获取最新的消息
            new_messages = messages_after[count_before:]
            
            print(f"\n📊 新增消息分析:")
            print(f"   新增消息数: {len(new_messages)}")
            
            for idx, msg in enumerate(new_messages, 1):
                print(f"\n   消息 {idx}:")
                print(f"   - 角色: {msg.get('role')}")
                print(f"   - 内容长度: {len(msg.get('content', ''))} 字符")
                print(f"   - 创建时间: {msg.get('created_at')}")
                print(f"   - 消息 ID: {msg.get('id')}")
                
                if msg.get('role') == 'assistant':
                    print(f"\n   🤖 AI 回复内容:")
                    print(f"   {msg.get('content')[:200]}...")
            
            break
    else:
        print(f"\n   ⚠️  等待超时，未检测到 AI 回复")
    
    # 步骤 3: 分析回复机制
    print("\n" + "=" * 80)
    print("📋 回复机制分析:")
    print("=" * 80)
    
    print("""
    1. 发送消息方式:
       - 方法: POST
       - 端点: /api/chat-session/{session_id}/messages
       - 立即返回: 是（不等待 AI 回复）
    
    2. AI 回复方式:
       - 异步处理: AI 在后台生成回复
       - 获取方式: 需要轮询 GET 请求
       - 回复时间: 通常 2-10 秒
    
    3. 消息结构:
       - role: "user" 或 "assistant"
       - content: 消息内容
       - created_at: 时间戳
       - id: 消息唯一标识
    
    4. 前端实现建议:
       - 发送消息后，启动轮询
       - 每 2-3 秒检查一次新消息
       - 检测到 assistant 消息时停止轮询
       - 显示加载动画提升用户体验
    """)
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
