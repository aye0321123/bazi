#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连接测试脚本
用于验证 Session ID 和 Cookie 是否有效
"""

import requests
import sys

def test_connection(session_id, cookie):
    """
    测试连接是否有效
    
    Args:
        session_id: 会话ID
        cookie: Cookie字符串
        
    Returns:
        bool: 连接是否成功
    """
    print("🔍 开始测试连接...")
    print("-" * 60)
    
    # 测试配置
    base_url = "https://www.bazi-ai.com"
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 测试1: 检查 Session ID 格式
    print("\n✓ 测试1: 检查 Session ID 格式")
    if not session_id or len(session_id) < 30:
        print("  ❌ Session ID 格式不正确")
        print(f"  当前值: {session_id}")
        return False
    print(f"  ✅ Session ID 格式正确: {session_id[:20]}...")
    
    # 测试2: 检查 Cookie 格式
    print("\n✓ 测试2: 检查 Cookie 格式")
    if not cookie or len(cookie) < 100:
        print("  ❌ Cookie 格式不正确或太短")
        return False
    
    # 检查必要的 Cookie 字段
    required_cookies = ["__Secure-authjs.session-token"]
    missing_cookies = [c for c in required_cookies if c not in cookie]
    
    if missing_cookies:
        print(f"  ❌ 缺少必要的 Cookie 字段: {', '.join(missing_cookies)}")
        return False
    print(f"  ✅ Cookie 格式正确 (长度: {len(cookie)} 字符)")
    
    # 测试3: 尝试获取消息
    print("\n✓ 测试3: 尝试连接 API")
    url = f"{base_url}/api/chat-session/{session_id}/messages"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            messages = response.json()
            print(f"  ✅ 连接成功！找到 {len(messages)} 条消息")
            
            # 显示最近的消息
            if messages:
                print("\n📝 最近的消息:")
                for msg in messages[-3:]:  # 显示最后3条
                    role = "👤 用户" if msg.get('role') == 'user' else "🤖 AI"
                    content = msg.get('content', '')[:50]
                    print(f"  {role}: {content}...")
            
            return True
            
        elif response.status_code == 401:
            print("  ❌ 认证失败 (401)")
            print("  原因: Cookie 可能已过期或无效")
            print("  解决: 重新登录网站并获取新的 Cookie")
            return False
            
        elif response.status_code == 404:
            print("  ❌ 未找到会话 (404)")
            print("  原因: Session ID 可能不正确")
            print("  解决: 检查 Session ID 是否正确")
            return False
            
        else:
            print(f"  ❌ 未知错误 (状态码: {response.status_code})")
            print(f"  响应: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("  ❌ 连接超时")
        print("  原因: 网络连接问题或服务器响应慢")
        return False
        
    except requests.exceptions.ConnectionError:
        print("  ❌ 连接错误")
        print("  原因: 无法连接到服务器")
        print("  解决: 检查网络连接")
        return False
        
    except Exception as e:
        print(f"  ❌ 发生错误: {str(e)}")
        return False


def main():
    """主函数"""
    print("\n" + "="*60)
    print("🔮 BaziAI 连接测试工具")
    print("="*60)
    
    # 获取配置
    print("\n请输入配置信息:")
    print("-" * 60)
    
    try:
        session_id = input("Session ID: ").strip()
        print("\n请输入 Cookie (可以粘贴多行，输入空行结束):")
        
        cookie_lines = []
        while True:
            line = input()
            if not line:
                break
            cookie_lines.append(line)
        
        cookie = " ".join(cookie_lines).strip()
        
        # 运行测试
        success = test_connection(session_id, cookie)
        
        # 显示结果
        print("\n" + "="*60)
        if success:
            print("✅ 测试通过！您可以开始使用 API 了")
            print("\n下一步:")
            print("  1. 运行 python bazi_simple.py 快速测试")
            print("  2. 或运行 python bazi_interactive.py 使用交互式工具")
        else:
            print("❌ 测试失败！请检查配置")
            print("\n建议:")
            print("  1. 确保已登录 BaziAI 网站")
            print("  2. 重新获取 Cookie（可能已过期）")
            print("  3. 检查 Session ID 是否正确")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n👋 测试已取消")
        sys.exit(0)


if __name__ == "__main__":
    main()
