#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细测试 API 响应
"""

import json
import requests

def test_api():
    """详细测试 API"""
    
    print("="*60)
    print("🔍 详细 API 测试")
    print("="*60)
    print()
    
    # 读取凭证
    try:
        with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
            creds = json.load(f)
    except FileNotFoundError:
        print("❌ 未找到 bazi_credentials.json 文件")
        return
    
    session_id = creds.get('session_id') or "26a7d080-283c-43c9-a741-23d8dfcb8512"
    cookie = creds.get('cookie')
    
    print(f"📜 Session ID: {session_id}")
    print(f"🍪 Cookie: {cookie[:80]}...")
    print()
    
    # 设置请求头
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Origin": "https://www.bazi-ai.com",
        "Referer": f"https://www.bazi-ai.com/zh/chat/{session_id}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 测试获取消息
    print("📥 测试 GET /api/chat-session/{session_id}/messages")
    url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   状态码: {response.status_code}")
        print(f"   响应头: {dict(response.headers)}")
        print(f"   响应内容 (前200字符):")
        print(f"   {response.text[:200]}")
        print()
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON 解析成功")
                print(f"   数据类型: {type(data)}")
                if isinstance(data, list):
                    print(f"   消息数量: {len(data)}")
                print()
            except:
                print(f"   ❌ JSON 解析失败")
                print()
        else:
            print(f"   ❌ 请求失败")
            print()
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
        print()
    
    # 测试发送消息
    print("📤 测试 POST /api/chat-session/{session_id}/messages")
    
    payload = {
        "session_id": session_id,
        "role": "user",
        "content": "你好",
        "id": ""
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"   状态码: {response.status_code}")
        print(f"   响应内容 (前200字符):")
        print(f"   {response.text[:200]}")
        print()
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON 解析成功")
                print(f"   数据: {data}")
                print()
            except:
                print(f"   ❌ JSON 解析失败")
                print()
        else:
            print(f"   ❌ 请求失败")
            print()
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
        print()
    
    print("="*60)
    print("✅ 测试完成")
    print("="*60)


if __name__ == "__main__":
    test_api()
