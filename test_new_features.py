#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试天机阁的新功能
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_create_session():
    """测试创建新会话"""
    print("="*60)
    print("测试 1: 创建新会话")
    print("="*60)
    
    # 读取 Cookie
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        cookie = json.load(f)['cookie']
    
    # 先登录（只需要 Cookie）
    print("\n步骤 1: 登录...")
    login_response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "session_id": "temp",  # 临时 ID
            "cookie": cookie
        }
    )
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {login_response.status_code}")
        return
    
    # 使用 session 保持登录状态
    session = requests.Session()
    session.cookies.update(login_response.cookies)
    
    print("✅ 登录成功")
    
    # 创建新会话
    print("\n步骤 2: 创建新会话...")
    create_response = session.post(f"{BASE_URL}/api/create-session")
    
    if create_response.status_code == 200:
        result = create_response.json()
        if result.get('success'):
            print(f"✅ 新会话创建成功！")
            print(f"   会话 ID: {result['session_id']}")
            print(f"   创建时间: {result['data']['created_at']}")
            return result['session_id']
        else:
            print(f"❌ 创建失败: {result.get('error')}")
    else:
        print(f"❌ 请求失败: {create_response.status_code}")
    
    return None


def test_create_and_send():
    """测试创建新会话并发送消息"""
    print("\n" + "="*60)
    print("测试 2: 创建新会话并发送消息")
    print("="*60)
    
    # 读取 Cookie
    with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
        cookie = json.load(f)['cookie']
    
    # 先登录
    print("\n步骤 1: 登录...")
    login_response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "session_id": "temp",
            "cookie": cookie
        }
    )
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {login_response.status_code}")
        return
    
    session = requests.Session()
    session.cookies.update(login_response.cookies)
    print("✅ 登录成功")
    
    # 创建新会话并发送消息
    print("\n步骤 2: 创建新会话并发送消息...")
    message = "你好，请用一句话介绍你自己"
    
    create_send_response = session.post(
        f"{BASE_URL}/api/create-and-send",
        json={"content": message}
    )
    
    if create_send_response.status_code == 200:
        result = create_send_response.json()
        if result.get('success'):
            print(f"✅ 创建并发送成功！")
            print(f"   会话 ID: {result['session_id']}")
            print(f"   消息 ID: {result['message_data']['id']}")
            print(f"   对话链接: {result['chat_url']}")
            print(f"\n💡 提示: 在浏览器中打开上面的链接查看 AI 回复")
            return result
        else:
            print(f"❌ 失败: {result.get('error')}")
    else:
        print(f"❌ 请求失败: {create_send_response.status_code}")
    
    return None


def main():
    """主函数"""
    print("\n🔮 天机阁新功能测试\n")
    
    try:
        # 测试 1: 创建新会话
        session_id = test_create_session()
        
        # 测试 2: 创建新会话并发送消息
        result = test_create_and_send()
        
        print("\n" + "="*60)
        print("✅ 测试完成")
        print("="*60)
        
        if result:
            print(f"\n🌐 在浏览器中打开:")
            print(f"   {result['chat_url']}")
            print(f"\n💡 等待 5-10 秒查看 AI 回复")
        
    except FileNotFoundError:
        print("❌ 找不到 bazi_credentials.json 文件")
        print("   请先运行: python get_cookie_v2.py")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
