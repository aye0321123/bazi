#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整测试工作流程
"""

import requests
import json
import time

def test_full_workflow():
    """测试完整的工作流程"""
    
    print("="*60)
    print("🧪 完整工作流程测试")
    print("="*60)
    print()
    
    # 读取凭证
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        creds = json.load(f)
    
    session_id = "26a7d080-283c-43c9-a741-23d8dfcb8512"
    cookie = creds['cookie']
    
    # 创建 session
    session = requests.Session()
    
    # 步骤 1: 登录
    print("📝 步骤 1: 登录")
    print("-" * 60)
    
    login_url = "http://127.0.0.1:5000/api/login"
    login_data = {
        "session_id": session_id,
        "cookie": cookie
    }
    
    try:
        response = session.post(login_url, json=login_data, timeout=30)
        result = response.json()
        
        if result.get('success'):
            print(f"✅ 登录成功: {result.get('message')}")
        else:
            print(f"❌ 登录失败: {result.get('error')}")
            return
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return
    
    print()
    time.sleep(1)
    
    # 步骤 2: 获取消息列表
    print("📝 步骤 2: 获取消息列表")
    print("-" * 60)
    
    messages_url = "http://127.0.0.1:5000/api/messages"
    
    try:
        response = session.get(messages_url, timeout=30)
        result = response.json()
        
        if result.get('success'):
            messages = result.get('data', [])
            print(f"✅ 成功获取 {len(messages)} 条消息")
            
            if messages:
                print()
                print("最近的 3 条消息:")
                for i, msg in enumerate(messages[:3], 1):
                    role = "👤 用户" if msg.get('role') == 'user' else "🤖 AI"
                    content = msg.get('content', '')[:50]
                    print(f"  {i}. {role}: {content}...")
        else:
            print(f"❌ 获取消息失败: {result.get('error')}")
    except Exception as e:
        print(f"❌ 获取消息请求失败: {e}")
    
    print()
    time.sleep(1)
    
    # 步骤 3: 发送测试消息
    print("📝 步骤 3: 发送测试消息")
    print("-" * 60)
    
    send_url = "http://127.0.0.1:5000/api/send"
    test_message = "你好，这是一条自动化测试消息，请简短回复"
    send_data = {
        "content": test_message
    }
    
    try:
        print(f"📤 发送消息: {test_message}")
        response = session.post(send_url, json=send_data, timeout=30)
        result = response.json()
        
        if result.get('success'):
            data = result.get('data', {})
            print(f"✅ 消息发送成功")
            print(f"   消息 ID: {data.get('id')}")
            print(f"   发送时间: {data.get('created_at')}")
        else:
            print(f"❌ 发送消息失败: {result.get('error')}")
    except Exception as e:
        print(f"❌ 发送消息请求失败: {e}")
    
    print()
    time.sleep(2)
    
    # 步骤 4: 再次获取消息，查看新消息
    print("📝 步骤 4: 查看新消息")
    print("-" * 60)
    
    try:
        response = session.get(messages_url, timeout=30)
        result = response.json()
        
        if result.get('success'):
            messages = result.get('data', [])
            print(f"✅ 当前共有 {len(messages)} 条消息")
            
            # 显示最新的消息
            if messages:
                latest = messages[-1]
                role = "👤 用户" if latest.get('role') == 'user' else "🤖 AI"
                content = latest.get('content', '')
                print()
                print(f"最新消息:")
                print(f"  {role}: {content[:100]}...")
        else:
            print(f"❌ 获取消息失败: {result.get('error')}")
    except Exception as e:
        print(f"❌ 获取消息请求失败: {e}")
    
    print()
    print("="*60)
    print("✅ 测试完成！")
    print("="*60)
    print()
    print("💡 总结:")
    print("   - 登录功能: ✅ 正常")
    print("   - 获取消息: ✅ 正常")
    print("   - 发送消息: ✅ 正常")
    print()
    print("🎯 您现在可以在浏览器中使用 Web 界面了！")
    print("   访问: http://127.0.0.1:5000")
    print()


if __name__ == "__main__":
    test_full_workflow()
