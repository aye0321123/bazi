#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Cookie 是否有效
"""

import requests
import json

def test_cookie():
    """测试 Cookie"""
    
    print("="*60)
    print("测试 Cookie 有效性")
    print("="*60)
    
    # 读取 Cookie
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        cookie = json.load(f)['cookie']
    
    print(f"\nCookie 长度: {len(cookie)} 字符")
    print(f"Cookie 前50字符: {cookie[:50]}...")
    
    # 测试请求
    session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"
    url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"
    
    headers = {
        "Cookie": cookie,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print(f"\n请求 URL: {url}")
    print("发送请求...")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容长度: {len(response.content)}")
        print(f"响应内容前200字符:\n{response.text[:200]}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"\n✅ Cookie 有效！")
                print(f"消息数量: {len(data) if isinstance(data, list) else 'N/A'}")
                return True
            except json.JSONDecodeError as e:
                print(f"\n❌ JSON 解析失败: {e}")
                print(f"这可能意味着 Cookie 已过期或无效")
                return False
        else:
            print(f"\n❌ 请求失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_cookie()
