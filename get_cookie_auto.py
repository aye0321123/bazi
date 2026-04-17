#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动获取 BaziAI Cookie 的脚本（自动化版本）
使用命令行参数直接运行
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
import sys

def get_bazi_cookie(email, password, headless=False):
    """
    自动登录 BaziAI 并获取 Cookie
    
    Args:
        email: 邮箱地址
        password: 密码
        headless: 是否使用无头模式（不显示浏览器窗口）
        
    Returns:
        dict: 包含 session_id 和 cookie 的字典
    """
    
    print("🚀 启动浏览器...")
    
    # 配置 Chrome 选项
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 启动浏览器
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"❌ 启动浏览器失败: {e}")
        print("💡 请确保已安装 Chrome 浏览器和 ChromeDriver")
        print("   下载地址: https://chromedriver.chromium.org/")
        return None
    
    try:
        # 访问登录页面
        print("📱 访问 BaziAI 网站...")
        driver.get("https://www.bazi-ai.com/zh")
        time.sleep(3)
        
        # 点击登录按钮
        print("🔍 查找登录按钮...")
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '登录') or contains(text(), 'Login')]"))
            )
            login_button.click()
            print("✅ 点击登录按钮")
            time.sleep(2)
        except:
            print("⚠️  未找到登录按钮，可能已经在登录页面")
        
        # 查找邮箱登录选项
        print("🔍 查找邮箱登录选项...")
        try:
            email_login = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '邮箱') or contains(text(), 'Email')]"))
            )
            email_login.click()
            print("✅ 选择邮箱登录")
            time.sleep(2)
        except:
            print("⚠️  未找到邮箱登录选项")
        
        # 输入邮箱
        print("📧 输入邮箱...")
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email'], input[placeholder*='邮箱'], input[placeholder*='email']"))
            )
            email_input.clear()
            email_input.send_keys(email)
            print(f"✅ 已输入邮箱: {email}")
            time.sleep(1)
        except Exception as e:
            print(f"❌ 输入邮箱失败: {e}")
            driver.save_screenshot("error_email.png")
            return None
        
        # 输入密码
        print("🔑 输入密码...")
        try:
            password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
            password_input.clear()
            password_input.send_keys(password)
            print("✅ 已输入密码")
            time.sleep(1)
        except Exception as e:
            print(f"❌ 输入密码失败: {e}")
            driver.save_screenshot("error_password.png")
            return None
        
        # 点击登录提交按钮
        print("🚪 提交登录...")
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button:contains('登录'), button:contains('Login')")
            submit_button.click()
            print("✅ 已点击登录按钮")
            time.sleep(5)
        except Exception as e:
            print(f"❌ 点击登录按钮失败: {e}")
            driver.save_screenshot("error_submit.png")
            return None
        
        # 等待登录成功，检查 URL 变化
        print("⏳ 等待登录成功...")
        time.sleep(5)
        
        current_url = driver.current_url
        print(f"📍 当前 URL: {current_url}")
        
        # 提取 Session ID（如果 URL 中包含）
        session_id = None
        if "/chat/" in current_url:
            session_id = current_url.split("/chat/")[-1].split("?")[0].split("#")[0]
            print(f"✅ 提取到 Session ID: {session_id}")
        else:
            print("⚠️  URL 中未找到 Session ID，尝试访问聊天页面...")
            # 尝试访问聊天页面
            driver.get("https://www.bazi-ai.com/zh/chat")
            time.sleep(3)
            current_url = driver.current_url
            if "/chat/" in current_url:
                session_id = current_url.split("/chat/")[-1].split("?")[0].split("#")[0]
                print(f"✅ 提取到 Session ID: {session_id}")
        
        # 获取所有 Cookies
        print("🍪 提取 Cookie...")
        cookies = driver.get_cookies()
        
        # 将 Cookies 转换为字符串格式
        cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        
        print(f"✅ 成功获取 Cookie (长度: {len(cookie_str)} 字符)")
        
        # 保存到文件
        result = {
            "session_id": session_id,
            "cookie": cookie_str,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cookies_detail": cookies
        }
        
        with open("bazi_credentials.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print("💾 凭证已保存到 bazi_credentials.json")
        
        return result
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        driver.save_screenshot("error_final.png")
        print("📸 错误截图已保存为 error_final.png")
        return None
        
    finally:
        print("🔚 关闭浏览器...")
        driver.quit()


def main():
    """主函数"""
    print("="*60)
    print("🔮 BaziAI Cookie 自动提取工具")
    print("="*60)
    print()
    
    # 使用预设的凭证
    email = "291568499@qq.com"
    password = "hzy020618"
    
    print(f"📧 邮箱: {email}")
    print(f"🔑 密码: {'*' * len(password)}")
    print()
    print("⚠️  注意: 浏览器窗口会自动打开，请不要手动操作")
    print()
    
    # 获取 Cookie
    result = get_bazi_cookie(email, password, headless=False)
    
    if result:
        print()
        print("="*60)
        print("✅ 成功获取凭证！")
        print("="*60)
        print()
        print(f"📜 Session ID:")
        print(f"   {result['session_id']}")
        print()
        print(f"🍪 Cookie (前100字符):")
        print(f"   {result['cookie'][:100]}...")
        print()
        print("💾 完整信息已保存到: bazi_credentials.json")
        print()
        print("🎯 下一步:")
        print("   1. 打开 http://127.0.0.1:5000")
        print("   2. 粘贴上面的 Session ID 和 Cookie")
        print("   3. 点击登录")
        print()
    else:
        print()
        print("="*60)
        print("❌ 获取凭证失败")
        print("="*60)
        print()
        print("💡 可能的原因:")
        print("   1. 邮箱或密码错误")
        print("   2. 网站结构发生变化")
        print("   3. 需要验证码")
        print("   4. ChromeDriver 未安装或版本不匹配")
        print()
        print("🔧 解决方法:")
        print("   1. 检查邮箱密码是否正确")
        print("   2. 查看错误截图 error_*.png")
        print("   3. 手动获取 Cookie（按 F12 → Network → 复制 Cookie）")
        print()


if __name__ == "__main__":
    main()
