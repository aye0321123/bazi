#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 AI 回复
"""

import requests
import json
import time

def check_messages():
    """检查消息列表"""
    
    print("="*60)
    print("🔍 检查消息列表")
    print("="*60)
    print()
    
    # 读取凭证
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        creds = json.load(f)
    
    session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"
    cookie = creds['cookie']
    
    headers = {
        "Cookie": cookie,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.bazi-ai.com",
        "Referer": f"https://www.bazi-ai.com/zh/chat/{session_id}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        messages = response.json()
        
        print(f"✅ 共有 {len(messages)} 条消息")
        print()
        
        # 统计消息类型
        user_messages = [msg for msg in messages if msg.get('role') == 'user']
        ai_messages = [msg for msg in messages if msg.get('role') == 'assistant']
        
        print(f"📊 消息统计:")
        print(f"   👤 用户消息: {len(user_messages)} 条")
        print(f"   🤖 AI 回复: {len(ai_messages)} 条")
        print()
        
        if ai_messages:
            print("🤖 AI 回复列表:")
            print("-" * 60)
            for i, msg in enumerate(ai_messages, 1):
                content = msg.get('content', '')
                created_at = msg.get('created_at', '')
                print(f"\n{i}. [{created_at}]")
                print(f"{content[:200]}")
                if len(content) > 200:
                    print(f"... (还有 {len(content) - 200} 字符)")
                print()
        else:
            print("⚠️  没有找到 AI 回复")
            print()
            print("可能的原因:")
            print("1. AI 还在生成回复（需要等待）")
            print("2. BaziAI 使用 WebSocket 推送回复（需要特殊处理）")
            print("3. 需要在网页上才能看到回复")
            print()
        
        # 显示最近的消息
        print("📋 最近的 10 条消息:")
        print("-" * 60)
        for i, msg in enumerate(messages[-10:], 1):
            role = "👤 用户" if msg.get('role') == 'user' else "🤖 AI"
            content = msg.get('content', '')[:80]
            created_at = msg.get('created_at', '')
            print(f"{i}. {role} [{created_at}]")
            print(f"   {content}...")
            print()
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print("="*60)
    print()
    print("💡 建议:")
    print("   1. 在浏览器中访问: https://www.bazi-ai.com/zh/chat/26a7d080-283c-43c9-a741-23d8dfcb8512")
    print("   2. 查看是否有 AI 回复")
    print("   3. 如果有回复，说明 API 可能有延迟")
    print()


if __name__ == "__main__":
    check_messages()
