#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版 Cookie 提取工具
使用 requests 库直接登录（如果网站支持）
"""

import requests
import json
from datetime import datetime

def get_cookie_simple(email, password):
    """
    尝试通过 API 登录获取 Cookie
    
    Args:
        email: 邮箱
        password: 密码
        
    Returns:
        dict: 包含 cookie 的字典
    """
    
    print("🚀 尝试登录 BaziAI...")
    
    session = requests.Session()
    
    # 尝试不同的登录端点
    login_urls = [
        "https://www.bazi-ai.com/api/auth/signin",
        "https://www.bazi-ai.com/api/login",
        "https://www.bazi-ai.com/auth/signin",
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    payload = {
        "email": email,
        "password": password
    }
    
    for url in login_urls:
        try:
            print(f"📡 尝试: {url}")
            response = session.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ 登录成功！")
                
                # 获取 Cookies
                cookies = session.cookies.get_dict()
                cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
                
                result = {
                    "cookie": cookie_str,
                    "cookies_dict": cookies,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # 保存到文件
                with open("bazi_credentials_simple.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                print(f"💾 Cookie 已保存到 bazi_credentials_simple.json")
                return result
                
        except Exception as e:
            print(f"⚠️  失败: {e}")
            continue
    
    print("❌ 所有登录尝试都失败了")
    print("💡 建议使用 Selenium 版本: python get_cookie.py")
    return None


def main():
    print("="*60)
    print("🔮 BaziAI Cookie 简易提取工具")
    print("="*60)
    print()
    
    email = input("📧 请输入邮箱: ").strip()
    password = input("🔑 请输入密码: ").strip()
    
    if not email or not password:
        print("❌ 邮箱和密码不能为空！")
        return
    
    result = get_cookie_simple(email, password)
    
    if result:
        print()
        print("="*60)
        print("✅ 成功！")
        print("="*60)
        print()
        print(f"🍪 Cookie:")
        print(f"   {result['cookie'][:100]}...")
        print()
    else:
        print()
        print("="*60)
        print("❌ 简易方法失败")
        print("="*60)
        print()
        print("💡 请使用完整版本:")
        print("   python get_cookie.py")
        print()


if __name__ == "__main__":
    main()
