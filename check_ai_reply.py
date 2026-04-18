#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 AI 回复功能
快速测试脚本
"""

import urllib3
import json
import ssl

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

def get_messages():
    """获取消息列表"""
    url = f"{base_url}/api/chat-session/{session_id}/messages"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = http.request('GET', url, headers=headers)
        if response.status == 200:
            messages = json.loads(response.data.decode('utf-8'))
            return {"success": True, "data": messages}
        else:
            return {"success": False, "error": f"状态码: {response.status}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    print("=" * 80)
    print("🔍 检查 BaziAI 消息状态")
    print("=" * 80)
    
    result = get_messages()
    
    if not result['success']:
        print(f"\n❌ 获取失败: {result['error']}")
        return
    
    messages = result['data']
    print(f"\n📊 总消息数: {len(messages)}")
    
    # 显示最近5条消息
    print("\n📝 最近的消息:")
    print("-" * 80)
    
    recent_messages = messages[-5:] if len(messages) > 5 else messages
    
    for i, msg in enumerate(recent_messages, 1):
        role = "👤 用户" if msg['role'] == 'user' else "🤖 AI"
        content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
        time = msg.get('created_at', 'N/A')
        
        print(f"\n{i}. {role}")
        print(f"   时间: {time}")
        print(f"   内容: {content}")
    
    print("\n" + "=" * 80)
    
    # 统计
    user_count = sum(1 for msg in messages if msg['role'] == 'user')
    ai_count = sum(1 for msg in messages if msg['role'] == 'assistant')
    
    print(f"\n📈 统计信息:")
    print(f"   用户消息: {user_count}")
    print(f"   AI 回复: {ai_count}")
    print(f"   回复率: {ai_count/user_count*100:.1f}%" if user_count > 0 else "   回复率: N/A")
    
    # 检查最后一条消息
    if messages:
        last_msg = messages[-1]
        if last_msg['role'] == 'user':
            print(f"\n⚠️  最后一条消息是用户消息，AI 可能还未回复")
        else:
            print(f"\n✅ 最后一条消息是 AI 回复")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
