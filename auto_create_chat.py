#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动创建新对话并发送消息
"""

import requests
import json
import time
import sys

def create_new_session():
    """创建新的聊天会话"""
    
    print("="*60)
    print("🆕 创建新对话")
    print("="*60)
    print()
    
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        cookie = json.load(f)['cookie']
    
    headers = {
        "Cookie": cookie,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.bazi-ai.com",
        "Referer": "https://www.bazi-ai.com/zh",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    url = "https://www.bazi-ai.com/api/chat-session"
    
    try:
        print("📡 发送请求...")
        response = requests.post(url, headers=headers, json={}, timeout=30)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            print()
            
            if result.get('code') == 0:
                data = result.get('data', {})
                session_id = data.get('uuid')
                
                print(f"✅ 新对话创建成功！")
                print(f"   会话 ID: {session_id}")
                print(f"   创建时间: {data.get('created_at')}")
                print()
                
                return session_id
            else:
                print(f"❌ 创建失败: {result.get('message')}")
                return None
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()
        return None


def send_message(session_id, message):
    """发送消息"""
    
    print("="*60)
    print("📤 发送消息")
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
        print("📡 发送请求...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 消息已发送")
            print(f"   消息 ID: {result.get('id')}")
            print(f"   时间: {result.get('created_at')}")
            print()
            return result
        else:
            print(f"❌ 发送失败: {response.status_code}")
            print(f"响应: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    
    # 步骤 1: 创建新对话
    session_id = create_new_session()
    
    if not session_id:
        print("❌ 无法创建新对话")
        sys.exit(1)
    
    # 步骤 2: 发送测试消息
    test_message = "你好，请用一句话介绍你自己"
    
    result = send_message(session_id, test_message)
    
    if not result:
        print("❌ 消息发送失败")
        sys.exit(1)
    
    # 步骤 3: 打开浏览器
    print("="*60)
    print("🌐 在浏览器中查看")
    print("="*60)
    print()
    
    chat_url = f"https://www.bazi-ai.com/zh/chat/{session_id}"
    print(f"对话链接: {chat_url}")
    print()
    
    # 打开浏览器
    import subprocess
    try:
        subprocess.run(['cmd', '/c', 'start', chat_url], check=True)
        print("✅ 已在浏览器中打开对话")
    except Exception as e:
        print(f"⚠️  无法自动打开浏览器: {e}")
        print("   请手动复制上面的链接到浏览器")
    
    print()
    print("="*60)
    print("✅ 完成")
    print("="*60)
    print()
    print("📝 重要提示:")
    print("   1. 消息已发送到新对话")
    print("   2. 请在浏览器中查看 AI 回复")
    print("   3. AI 回复需要在网页上才能触发")
    print()
    print(f"💾 新会话 ID: {session_id}")
    print("   您可以保存此 ID 用于后续 API 调用")
    print()


if __name__ == "__main__":
    main()
