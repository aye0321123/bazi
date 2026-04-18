#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送消息并等待 BaziAI 回复
"""

import urllib3
import json
import ssl
import time
from datetime import datetime

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

def send_message(content):
    """发送消息"""
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
        "content": content,
        "id": ""
    }
    
    try:
        response = http.request(
            'POST',
            url,
            headers=headers,
            body=json.dumps(payload).encode('utf-8')
        )
        
        if response.status == 200:
            result = json.loads(response.data.decode('utf-8'))
            return {"success": True, "data": result}
        else:
            return {"success": False, "error": f"状态码: {response.status}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

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

def wait_for_reply(initial_count, max_wait=120, check_interval=3):
    """
    等待 AI 回复
    
    Args:
        initial_count: 发送消息前的消息数量
        max_wait: 最大等待时间（秒）
        check_interval: 检查间隔（秒）
    
    Returns:
        AI 回复内容或 None
    """
    print(f"\n⏳ 等待 AI 回复（最多等待 {max_wait} 秒）...")
    
    start_time = time.time()
    attempts = 0
    
    while time.time() - start_time < max_wait:
        attempts += 1
        elapsed = int(time.time() - start_time)
        
        # 获取最新消息
        result = get_messages()
        
        if result['success']:
            messages = result['data']
            current_count = len(messages)
            
            print(f"   [{elapsed}s] 尝试 {attempts}: 消息数 {current_count} (初始: {initial_count})", end='\r')
            
            # 检查是否有新的 assistant 消息
            if current_count > initial_count + 1:
                # 获取新消息
                new_messages = messages[initial_count:]
                
                for msg in new_messages:
                    if msg.get('role') == 'assistant':
                        print(f"\n\n✅ 收到 AI 回复！（等待时间: {elapsed}秒）")
                        return msg
        
        time.sleep(check_interval)
    
    print(f"\n\n⏰ 等待超时（{max_wait}秒）")
    return None

def main():
    print("=" * 80)
    print("🤖 BaziAI 消息发送与回复获取")
    print("=" * 80)
    
    # 获取用户输入
    message = input("\n💬 请输入要发送的消息: ").strip()
    
    if not message:
        print("❌ 消息不能为空")
        return
    
    # 步骤 1: 获取当前消息数
    print("\n📊 步骤 1: 获取当前消息数...")
    result = get_messages()
    
    if not result['success']:
        print(f"❌ 获取失败: {result['error']}")
        return
    
    initial_count = len(result['data'])
    print(f"   当前消息数: {initial_count}")
    
    # 步骤 2: 发送消息
    print(f"\n📤 步骤 2: 发送消息...")
    print(f"   内容: {message}")
    
    result = send_message(message)
    
    if not result['success']:
        print(f"❌ 发送失败: {result['error']}")
        return
    
    print(f"   ✅ 消息已发送")
    print(f"   消息 ID: {result['data'].get('id')}")
    
    # 步骤 3: 等待回复
    print(f"\n🔄 步骤 3: 等待 AI 回复...")
    
    ai_reply = wait_for_reply(initial_count, max_wait=180, check_interval=3)
    
    if ai_reply:
        print("\n" + "=" * 80)
        print("🤖 AI 回复内容:")
        print("=" * 80)
        print(ai_reply.get('content'))
        print("=" * 80)
        
        # 保存到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_reply_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"用户消息: {message}\n\n")
            f.write(f"AI 回复:\n{ai_reply.get('content')}\n\n")
            f.write(f"时间: {ai_reply.get('created_at')}\n")
        
        print(f"\n💾 回复已保存到: {filename}")
    else:
        print("\n⚠️  未能获取到 AI 回复")
        print("💡 建议:")
        print("   1. 到 BaziAI 官网查看: https://www.bazi-ai.com/zh/chat/" + session_id)
        print("   2. 稍后运行 python get_chat_history.py 获取完整聊天记录")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
