#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建新对话并自动获取 AI 回复
"""

import requests
import json
import time

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
        
        if response.status_code == 200:
            result = response.json()
            
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
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None


def send_message(session_id, message):
    """发送消息"""
    
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
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"❌ 发送失败: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None


def get_messages(session_id):
    """获取消息列表"""
    
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
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            return []
            
    except Exception as e:
        print(f"❌ 获取消息失败: {e}")
        return []


def main():
    """主函数"""
    
    # 步骤 1: 创建新对话
    session_id = create_new_session()
    
    if not session_id:
        print("❌ 无法创建新对话")
        return
    
    # 步骤 2: 发送消息
    print("="*60)
    print("📤 发送消息")
    print("="*60)
    print()
    
    message = input("请输入您的问题: ").strip()
    
    if not message:
        message = "你好，请简单介绍一下你自己"
    
    print(f"发送: {message}")
    print()
    
    result = send_message(session_id, message)
    
    if result:
        print(f"✅ 消息已发送")
        print(f"   消息 ID: {result.get('id')}")
        print(f"   时间: {result.get('created_at')}")
        print()
    else:
        print("❌ 消息发送失败")
        return
    
    # 步骤 3: 在浏览器中打开对话
    print("="*60)
    print("🌐 在浏览器中查看")
    print("="*60)
    print()
    print(f"对话链接: https://www.bazi-ai.com/zh/chat/{session_id}")
    print()
    print("⚠️  重要提示:")
    print("   1. 请在浏览器中打开上面的链接")
    print("   2. 在网页上您会看到 AI 的回复")
    print("   3. AI 回复需要在网页上才能触发")
    print()
    
    # 打开浏览器
    import subprocess
    try:
        subprocess.run(['cmd', '/c', 'start', f'https://www.bazi-ai.com/zh/chat/{session_id}'], check=True)
        print("✅ 已在浏览器中打开对话")
    except:
        print("⚠️  请手动打开上面的链接")
    
    print()
    
    # 步骤 4: 等待并检查回复
    print("="*60)
    print("⏳ 等待 AI 回复")
    print("="*60)
    print()
    print("提示: 请在浏览器中查看 AI 回复")
    print("      然后按 Enter 键检查消息...")
    print()
    
    input("按 Enter 键检查消息...")
    
    messages = get_messages(session_id)
    
    print()
    print(f"📊 当前共有 {len(messages)} 条消息")
    print()
    
    ai_messages = [msg for msg in messages if msg.get('role') == 'assistant']
    
    if ai_messages:
        print("🤖 AI 回复:")
        print("-" * 60)
        for msg in ai_messages:
            content = msg.get('content', '')
            print(content)
            print()
    else:
        print("⚠️  暂时没有 AI 回复")
        print("   请在浏览器中查看")
    
    print("="*60)
    print("✅ 完成")
    print("="*60)
    print()
    print(f"💾 会话 ID 已保存: {session_id}")
    print(f"   您可以使用此 ID 继续对话")
    print()


if __name__ == "__main__":
    main()
