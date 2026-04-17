#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 API 响应
"""

import requests
import json
import time

def test_api():
    """详细测试 API 响应"""
    
    print("="*60)
    print("🔍 详细测试 API 响应")
    print("="*60)
    print()
    
    # 读取凭证
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        creds = json.load(f)
    
    session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"
    cookie = creds['cookie']
    
    print(f"📜 Session ID: {session_id}")
    print(f"🍪 Cookie 长度: {len(cookie)} 字符")
    print()
    
    # 设置请求头
    headers = {
        "Cookie": cookie,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.bazi-ai.com",
        "Referer": f"https://www.bazi-ai.com/zh/chat/{session_id}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 测试 1: 发送消息
    print("📤 测试 1: 发送消息")
    print("-" * 60)
    
    url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"
    payload = {
        "session_id": session_id,
        "role": "user",
        "content": "你好，请简短回复",
        "id": ""
    }
    
    print(f"请求 URL: {url}")
    print(f"请求内容: {payload['content']}")
    print()
    
    try:
        print("⏳ 发送请求...")
        start_time = time.time()
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        elapsed = time.time() - start_time
        
        print(f"✅ 响应状态码: {response.status_code}")
        print(f"⏱️  响应时间: {elapsed:.2f} 秒")
        print(f"📦 响应大小: {len(response.content)} 字节")
        print()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 消息已发送")
            print(f"   消息 ID: {result.get('id')}")
            print(f"   角色: {result.get('role')}")
            print(f"   内容: {result.get('content')}")
            print(f"   时间: {result.get('created_at')}")
            print()
            
            message_id = result.get('id')
            
            # 等待 AI 回复
            print("⏳ 等待 AI 回复（最多等待 30 秒）...")
            print()
            
            for i in range(30):
                time.sleep(1)
                
                # 获取消息列表
                response = requests.get(url, headers=headers, timeout=30)
                messages = response.json()
                
                # 查找 AI 的回复
                ai_replies = [msg for msg in messages if msg.get('role') == 'assistant' and msg.get('created_at') > result.get('created_at')]
                
                if ai_replies:
                    print(f"✅ 收到 AI 回复！（等待了 {i+1} 秒）")
                    print()
                    print("🤖 AI 回复:")
                    print("-" * 60)
                    latest_reply = ai_replies[-1]
                    content = latest_reply.get('content', '')
                    print(content[:500])  # 显示前 500 字符
                    if len(content) > 500:
                        print(f"\n... (还有 {len(content) - 500} 字符)")
                    print()
                    break
                
                if (i + 1) % 5 == 0:
                    print(f"   已等待 {i+1} 秒...")
            else:
                print("⚠️  等待超时，未收到 AI 回复")
                print("   可能原因:")
                print("   1. AI 正在生成回复（需要更长时间）")
                print("   2. 网络延迟")
                print("   3. API 限流")
                print()
        else:
            print(f"❌ 请求失败")
            print(f"响应内容: {response.text[:200]}")
            print()
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()
        print()
    
    # 测试 2: 获取所有消息
    print("📥 测试 2: 获取所有消息")
    print("-" * 60)
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            messages = response.json()
            print(f"✅ 成功获取 {len(messages)} 条消息")
            print()
            
            if messages:
                print("最近的 5 条消息:")
                for i, msg in enumerate(messages[-5:], 1):
                    role = "👤 用户" if msg.get('role') == 'user' else "🤖 AI"
                    content = msg.get('content', '')[:60]
                    created_at = msg.get('created_at', '')
                    print(f"  {i}. {role} [{created_at}]")
                    print(f"     {content}...")
                    print()
        else:
            print(f"❌ 获取失败: {response.status_code}")
            print()
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        print()
    
    print("="*60)
    print("✅ 测试完成")
    print("="*60)
    print()
    print("💡 说明:")
    print("   - 如果消息发送成功但没有收到回复，说明 AI 正在生成")
    print("   - 您可以稍后再次运行此脚本查看回复")
    print("   - 或者在 Web 界面查看: http://127.0.0.1:5000")
    print()


if __name__ == "__main__":
    test_api()
