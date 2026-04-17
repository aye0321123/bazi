#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试 BaziAI API
"""

import requests
import json

def test_direct():
    """直接测试 API"""
    
    # 读取凭证
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        creds = json.load(f)
    
    session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"
    cookie = creds['cookie']
    
    print("="*60)
    print("🧪 直接测试 BaziAI API")
    print("="*60)
    print()
    
    # 测试 GET 请求
    url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"
    
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Origin": "https://www.bazi-ai.com",
        "Referer": f"https://www.bazi-ai.com/zh/chat/{session_id}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print(f"📤 GET {url}")
    print()
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📥 状态码: {response.status_code}")
        print(f"📥 Content-Type: {response.headers.get('Content-Type')}")
        print(f"📥 Content-Encoding: {response.headers.get('Content-Encoding', 'none')}")
        print(f"📥 响应长度: {len(response.content)} 字节")
        print()
        
        # 检查原始内容
        print(f"📥 原始内容 (前100字节):")
        print(response.content[:100])
        print()
        
        # 检查文本内容
        print(f"📥 文本内容 (前200字符):")
        print(response.text[:200])
        print()
        
        # 尝试解析 JSON
        try:
            data = response.json()
            print(f"✅ JSON 解析成功")
            print(f"消息数量: {len(data)}")
            if data:
                print(f"第一条消息: {data[0].get('content', '')[:50]}...")
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败: {e}")
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print()
    print("="*60)


if __name__ == "__main__":
    test_direct()
