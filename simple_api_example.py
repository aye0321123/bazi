#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 API 调用示例
直接调用 BaziAI API，无需 Flask 服务器
"""

import requests
import json

# ==================== 配置区域 ====================

# BaziAI API 基础 URL
BASE_URL = "https://www.bazi-ai.com"

# 您的 Session ID
SESSION_ID = "26a7d080-283c-43c9-a741-23d8dfcb8512"

# 从文件读取 Cookie
with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)
    COOKIE = creds['cookie']

# ==================== API 函数 ====================

def get_messages():
    """
    获取消息列表
    
    Returns:
        list: 消息列表
    """
    url = f"{BASE_URL}/api/chat-session/{SESSION_ID}/messages"
    
    headers = {
        "Cookie": COOKIE,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/zh/chat/{SESSION_ID}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ 获取消息失败: {e}")
        return []


def send_message(content):
    """
    发送消息
    
    Args:
        content: 消息内容
        
    Returns:
        dict: 响应数据
    """
    url = f"{BASE_URL}/api/chat-session/{SESSION_ID}/messages"
    
    headers = {
        "Cookie": COOKIE,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/zh/chat/{SESSION_ID}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    payload = {
        "session_id": SESSION_ID,
        "role": "user",
        "content": content,
        "id": ""
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ 发送消息失败: {e}")
        return None


# ==================== 使用示例 ====================

def main():
    """主函数"""
    
    print("="*60)
    print("🔮 BaziAI API 调用示例")
    print("="*60)
    print()
    
    # 示例 1: 获取消息列表
    print("📥 示例 1: 获取消息列表")
    print("-" * 60)
    
    messages = get_messages()
    print(f"✅ 共有 {len(messages)} 条消息")
    
    if messages:
        print()
        print("最近的 3 条消息:")
        for i, msg in enumerate(messages[-3:], 1):
            role = "👤 用户" if msg.get('role') == 'user' else "🤖 AI"
            content = msg.get('content', '')[:50]
            print(f"  {i}. {role}: {content}...")
    
    print()
    
    # 示例 2: 发送消息
    print("📤 示例 2: 发送消息")
    print("-" * 60)
    
    test_message = "请用一句话介绍一下八字命理"
    print(f"发送: {test_message}")
    
    result = send_message(test_message)
    
    if result:
        print(f"✅ 消息已发送")
        print(f"   消息 ID: {result.get('id')}")
        print(f"   发送时间: {result.get('created_at')}")
    
    print()
    print("="*60)
    print("✅ 示例完成！")
    print("="*60)
    print()
    print("💡 您可以修改上面的代码来实现自己的功能")
    print()


if __name__ == "__main__":
    main()
