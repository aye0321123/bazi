#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试提取的 Cookie 是否可用
"""

import json
from bazi_api import BaziAI

def test_cookie():
    """测试 Cookie"""
    
    print("="*60)
    print("🧪 测试提取的 Cookie")
    print("="*60)
    print()
    
    # 读取凭证
    try:
        with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
            creds = json.load(f)
    except FileNotFoundError:
        print("❌ 未找到 bazi_credentials.json 文件")
        print("💡 请先运行: python get_cookie_v2.py")
        return
    
    session_id = creds.get('session_id') or "26a7d080-283c-43c9-a741-23d8dfcb8512"
    cookie = creds.get('cookie')
    
    if not cookie:
        print("❌ Cookie 为空")
        return
    
    print(f"📜 Session ID: {session_id}")
    print(f"🍪 Cookie (前50字符): {cookie[:50]}...")
    print()
    
    # 创建客户端
    print("🔌 连接到 BaziAI...")
    client = BaziAI(session_id, cookie)
    
    # 测试获取消息
    print("📥 测试获取消息...")
    try:
        messages = client.get_messages()
        print(f"✅ 成功获取 {len(messages)} 条消息")
        
        if messages:
            print()
            print("📋 最近的消息:")
            for i, msg in enumerate(messages[:3], 1):
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                print(f"   {i}. [{role}] {content[:50]}...")
        print()
    except Exception as e:
        print(f"❌ 获取消息失败: {e}")
        print()
    
    # 测试发送消息
    print("📤 测试发送消息...")
    test_message = "你好，这是一条测试消息"
    try:
        response = client.send_message(test_message)
        print(f"✅ 成功发送消息")
        print(f"📨 回复: {response[:100]}...")
        print()
    except Exception as e:
        print(f"❌ 发送消息失败: {e}")
        print()
    
    print("="*60)
    print("✅ 测试完成！")
    print("="*60)
    print()
    print("🎯 下一步:")
    print("   1. 打开 http://127.0.0.1:5000")
    print("   2. 使用提取的 Cookie 登录")
    print("   3. 开始使用 Web 界面")
    print()


if __name__ == "__main__":
    test_cookie()
