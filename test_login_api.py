#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录 API
"""

import requests
import json

def test_login():
    """测试登录 API"""
    
    # 读取凭证
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        creds = json.load(f)
    
    session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"
    cookie = creds['cookie']
    
    print("="*60)
    print("🧪 测试登录 API")
    print("="*60)
    print()
    print(f"Session ID: {session_id}")
    print(f"Cookie (前50字符): {cookie[:50]}...")
    print()
    
    # 测试登录
    url = "http://127.0.0.1:5000/api/login"
    payload = {
        "session_id": session_id,
        "cookie": cookie
    }
    
    print(f"📤 发送 POST 请求到: {url}")
    print(f"📦 Payload: session_id={session_id[:20]}..., cookie={cookie[:30]}...")
    print()
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"📥 响应状态码: {response.status_code}")
        print(f"📥 响应头: {dict(response.headers)}")
        print()
        print(f"📥 响应内容 (原始):")
        print(response.text)
        print()
        
        # 尝试解析 JSON
        try:
            data = response.json()
            print(f"✅ JSON 解析成功:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败: {e}")
            print(f"响应内容类型: {response.headers.get('Content-Type')}")
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print()
    print("="*60)


if __name__ == "__main__":
    test_login()
