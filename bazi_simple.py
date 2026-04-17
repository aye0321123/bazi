#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BaziAI 简化版脚本
快速使用示例
"""

import requests
import json

# ⚠️ 请替换为您自己的信息
SESSION_ID = "26a7d080-283c-43c9-a741-23d8dfcb8512"

COOKIE = """NEXT_LOCALE=zh; _ga=GA1.1.1899898920.1776086692; __Host-authjs.csrf-token=dc53b14177158adc3fa16ca2c3d3573a9836541975c215c45d5693ae3a8aaf4d%7Cf8648798852afc2334960251aa70c22b3f75003c155711c71a3979f47cc083df; __Secure-authjs.callback-url=https%3A%2F%2Fwww.bazi-ai.com; _ga_V7V71Z9C7T=GS2.1.s1776342169$o14$g1$t1776345108$j5b$l0$h0; __Secure-authjs.session-token=eyJhbGciOiJkaXliaXliLCJlbmNiOiJBMjU2R0NNIiwiYWx0IjoiUEJFUzItSFMyNTYrQTEyOEtXIiwiZW5jIjoiQTI1NkdDTSIsInAyYyI6MTAwMDAsInAycyI6IlVHUW5IM3lwQjZlbVZ1VjN4NkxmY3VJbmF6NmhWbS01YlV1LUxmTUFPY0s4U3E2X0p1ODlvekF6MnQzMXI4TDRWVmp1MnlKUVVlM3N4Z2dacWVEcG1kVTcxMUs3Z0JQZ0FaSG9aRWc0dUVFVk1tbXZjX3pBVnRFeXBFMFdsYWtiNU1QN2FvcktDSHFtUnRVbVZrRnZkTzBPTDBQdVNhOEVucFdyRk8tTjU0TTR3b3l0YU5oazV2b1FDeGhWU0lSUll4NTNDeHBHMzNlRGhQRkRPT04waGhWVklzcjk3eEFqLVFnVkh6ZTFrSDhTaHRaRWJKUVI5aEE4VVBlbGEtMFMtVEdiY0o4ZWhhLW1DXzE4bndjUkhubXB3bXVBYzhOaVhqN2pHZzNIZVFWOHRTaGRUa0F5aW1yYzZzUm94ZzFmbjh0eVZIck53MFpZNzRnLlFNY2EyNHVLbzlhbTUtUXhhOTREekV2WHFvbGlBbzZqX3hwZjBYZ19YVjQ"""

# API 基础配置
BASE_URL = "https://www.bazi-ai.com"
HEADERS = {
    "Content-Type": "application/json",
    "Cookie": COOKIE,
}

def send_message(content):
    """发送消息"""
    url = f"{BASE_URL}/api/chat-session/{SESSION_ID}/messages"
    payload = {
        "session_id": SESSION_ID,
        "role": "user",
        "content": content,
        "id": ""
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

def get_messages():
    """获取所有消息"""
    url = f"{BASE_URL}/api/chat-session/{SESSION_ID}/messages"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 1. 发送消息
    print("📤 发送消息...")
    result = send_message("请帮我分析一下2026年的运势")
    print(f"✅ 消息已发送: {result.get('id')}")
    
    # 2. 获取聊天记录
    print("\n📥 获取聊天记录...")
    messages = get_messages()
    
    # 3. 打印聊天记录
    print(f"\n共有 {len(messages)} 条消息:\n")
    for msg in messages:
        role = "👤 用户" if msg['role'] == 'user' else "🤖 AI"
        print(f"{role}: {msg['content'][:100]}...")
        print("-" * 60)
    
    # 4. 保存到文件
    with open('chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    print("\n✅ 聊天记录已保存到 chat_history.json")
