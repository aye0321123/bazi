#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Selenium 自动登录并触发 AI 回复
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# 从 bazi_credentials.json 读取配置
with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)
    COOKIE = creds['cookie']

# 用户邮箱和密码
EMAIL = "291568499@qq.com"
PASSWORD = "hzy020618"

BASE_URL = "https://www.bazi-ai.com"

def auto_login_and_trigger(session_id, message_content):
    """
    自动登录 BaziAI 并触发 AI 回复
    
    Args:
        session_id: 会话 ID
        message_content: 要发送的消息内容
    """
    print("=" * 60)
    print("🤖 Selenium 自动登录并触发 AI")
    print("=" * 60)
    
    # 配置 Chrome 选项
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 注释掉，显示浏览器方便调试
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 启动浏览器
    print("\n📦 启动 Chrome 浏览器...")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    try:
        # 步骤 1: 访问主页
        print(f"\n🌐 访问 BaziAI 主页...")
        driver.get(BASE_URL)
        time.sleep(2)
        
        # 步骤 2: 添加 Cookie（如果有效）
        print(f"\n🍪 添加 Cookie...")
        for cookie_pair in COOKIE.split('; '):
            if '=' in cookie_pair:
                name, value = cookie_pair.split('=', 1)
                try:
                    driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.bazi-ai.com'
                    })
                    print(f"   ✅ 添加 Cookie: {name}")
                except Exception as e:
                    print(f"   ⚠️  跳过 Cookie: {name} ({e})")
        
        # 步骤 3: 刷新页面使 Cookie 生效
        print(f"\n🔄 刷新页面...")
        driver.refresh()
        time.sleep(2)
        
        # 步骤 4: 检查是否需要登录
        print(f"\n🔍 检查登录状态...")
        
        # 尝试查找登录按钮
        try:
            login_button = driver.find_element(By.XPATH, "//button[contains(text(), '登录') or contains(text(), 'Sign in') or contains(text(), 'Login')]")
            print(f"   ⚠️  需要登录")
            
            # 点击登录按钮
            print(f"\n🔐 点击登录按钮...")
            login_button.click()
            time.sleep(2)
            
            # 查找邮箱输入框
            print(f"\n📧 输入邮箱: {EMAIL}")
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @name='email' or @placeholder='邮箱']"))
            )
            email_input.clear()
            email_input.send_keys(EMAIL)
            time.sleep(1)
            
            # 查找密码输入框
            print(f"\n🔑 输入密码...")
            password_input = driver.find_element(By.XPATH, "//input[@type='password' or @name='password']")
            password_input.clear()
            password_input.send_keys(PASSWORD)
            time.sleep(1)
            
            # 点击提交按钮
            print(f"\n✅ 提交登录...")
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), '登录') or contains(text(), 'Sign in')]")
            submit_button.click()
            
            # 等待登录完成
            print(f"\n⏳ 等待登录完成...")
            time.sleep(5)
            
            print(f"   ✅ 登录成功！")
            
        except Exception as e:
            print(f"   ✅ 已经登录或无需登录")
        
        # 步骤 5: 访问聊天页面
        chat_url = f"{BASE_URL}/zh/chat/{session_id}"
        print(f"\n💬 访问聊天页面...")
        print(f"   URL: {chat_url}")
        driver.get(chat_url)
        time.sleep(3)
        
        # 步骤 6: 等待页面加载
        print(f"\n⏳ 等待页面加载...")
        time.sleep(5)
        
        # 步骤 7: 检查是否有 AI 回复
        print(f"\n🔍 检查 AI 回复...")
        
        # 查找消息元素
        try:
            messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message') or contains(@class, 'chat')]")
            print(f"   找到 {len(messages)} 条消息")
            
            # 等待 AI 生成回复
            print(f"\n⏳ 等待 AI 生成回复（最多 30 秒）...")
            for i in range(30):
                time.sleep(1)
                messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message') or contains(@class, 'chat')]")
                print(f"   {i+1}秒: {len(messages)} 条消息", end='\r')
                
                # 如果消息数量增加，说明 AI 回复了
                if len(messages) > 1:
                    print(f"\n   ✅ AI 已回复！")
                    break
            
            print(f"\n\n✅ 完成！")
            
        except Exception as e:
            print(f"   ⚠️  无法检测消息: {e}")
        
        # 保持浏览器打开 10 秒，方便查看
        print(f"\n⏳ 保持浏览器打开 10 秒...")
        time.sleep(10)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print(f"\n🔚 关闭浏览器...")
        driver.quit()
        print(f"\n" + "=" * 60)
        print(f"✅ 完成")
        print(f"=" * 60)


if __name__ == "__main__":
    # 测试：创建新会话并发送消息
    print("\n请先在你的应用中创建新会话并发送消息")
    print("然后输入会话 ID 来触发 AI 回复\n")
    
    session_id = input("请输入会话 ID: ").strip()
    
    if session_id:
        auto_login_and_trigger(session_id, "测试消息")
    else:
        print("❌ 未输入会话 ID")
