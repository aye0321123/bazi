#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建新对话并发送消息
"""

import requests
import json
import time

def create_new_chat_and_send():
    """创建新对话并发送消息"""
    
    print("="*60)
    print("🆕 创建新对话并发送消息")
    print("="*60)
    print()
    
    # 读取凭证
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        creds = json.load(f)
    
    cookie = creds['cookie']
    
    headers = {
        "Cookie": cookie,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.bazi-ai.com",
        "Referer": "https://www.bazi-ai.com/zh",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 步骤 1: 尝试创建新对话
    print("📝 步骤 1: 创建新对话")
    print("-" * 60)
    
    # 尝试不同的端点
    endpoints = [
        "/api/chat-session",
        "/api/chat",
        "/api/sessions",
        "/api/new-chat",
        "/api/chat-session/new"
    ]
    
    for endpoint in endpoints:
        url = f"https://www.bazi-ai.com{endpoint}"
        print(f"尝试: {url}")
        
        try:
            # 尝试 POST 创建新会话
            response = requests.post(url, headers=headers, json={}, timeout=10)
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ 成功！")
                print(f"  响应: {response.text[:200]}")
                try:
                    data = response.json()
                    if 'id' in data or 'session_id' in data:
                        session_id = data.get('id') or data.get('session_id')
                        print(f"  🎉 新会话 ID: {session_id}")
                        return session_id
                except:
                    pass
            else:
                print(f"  ❌ 失败")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        
        print()
    
    print("⚠️  未找到创建新对话的 API 端点")
    print()
    
    # 步骤 2: 分析网页请求
    print("📝 步骤 2: 建议")
    print("-" * 60)
    print()
    print("要创建新对话，需要：")
    print()
    print("1. 在浏览器中打开 BaziAI 网站")
    print("   https://www.bazi-ai.com/zh")
    print()
    print("2. 按 F12 打开开发者工具")
    print()
    print("3. 切换到 Network 标签")
    print()
    print("4. 点击 '新对话' 按钮")
    print()
    print("5. 查看 Network 中的请求，找到创建新对话的 API")
    print()
    print("6. 记录以下信息：")
    print("   - 请求 URL")
    print("   - 请求方法 (GET/POST)")
    print("   - 请求体 (如果有)")
    print("   - 响应数据格式")
    print()
    
    return None


def send_message_to_session(session_id, message):
    """向指定会话发送消息"""
    
    print("="*60)
    print(f"📤 向会话发送消息")
    print("="*60)
    print()
    
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        cookie = json.load(f)['cookie']
    
    headers = {
        "Cookie": cookie,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.bazi-ai.com",
        "Referer": f"https://www.bazi-ai.com/zh/chat/{session_id}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    url = f"https://www.bazi-ai.com/api/chat-session/{session_id}/messages"
    
    payload = {
        "session_id": session_id,
        "role": "user",
        "content": message,
        "id": ""
    }
    
    print(f"会话 ID: {session_id}")
    print(f"消息内容: {message}")
    print()
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 消息已发送")
            print(f"   消息 ID: {result.get('id')}")
            print(f"   时间: {result.get('created_at')}")
            print()
            print(f"🌐 在浏览器中查看:")
            print(f"   https://www.bazi-ai.com/zh/chat/{session_id}")
            print()
            return result
        else:
            print(f"❌ 发送失败: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None


def main():
    """主函数"""
    
    # 尝试创建新对话
    new_session_id = create_new_chat_and_send()
    
    if new_session_id:
        # 如果成功创建，发送消息
        print()
        send_message_to_session(new_session_id, "你好，这是一个新对话")
    else:
        # 如果无法创建，使用现有会话
        print()
        print("="*60)
        print("💡 使用现有会话")
        print("="*60)
        print()
        print("由于无法通过 API 创建新对话，")
        print("我们将使用您现有的会话 ID:")
        print()
        print("26a7d080-283c-43c9-a741-23d8dfcb8512")
        print()
        
        choice = input("是否向现有会话发送消息？(y/n): ").strip().lower()
        
        if choice == 'y':
            message = input("请输入消息内容: ").strip()
            if message:
                send_message_to_session("26a7d080-283c-43c9-a741-23d8dfcb8512", message)
    
    print()
    print("="*60)
    print("✅ 完成")
    print("="*60)


if __name__ == "__main__":
    main()
