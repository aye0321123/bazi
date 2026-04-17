#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BaziAI Cookie 自动提取工具 V2
改进版：更好的错误处理和多种登录方式尝试
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import json
import sys

def setup_driver(headless=False):
    """设置并返回 WebDriver"""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # 隐藏 webdriver 特征
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
        return driver
    except Exception as e:
        print(f"❌ 启动浏览器失败: {e}")
        return None

def wait_and_click(driver, selectors, timeout=10, description="元素"):
    """尝试多个选择器，找到第一个可点击的元素并点击"""
    for selector_type, selector in selectors:
        try:
            if selector_type == "xpath":
                element = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
            elif selector_type == "css":
                element = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
            element.click()
            print(f"✅ 点击{description}成功")
            return True
        except:
            continue
    print(f"⚠️  未找到{description}")
    return False

def wait_and_input(driver, selectors, text, timeout=10, description="输入框"):
    """尝试多个选择器，找到第一个输入框并输入文本"""
    for selector_type, selector in selectors:
        try:
            if selector_type == "xpath":
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
            elif selector_type == "css":
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
            element.clear()
            element.send_keys(text)
            print(f"✅ 输入{description}成功")
            return True
        except:
            continue
    print(f"⚠️  未找到{description}")
    return False

def get_bazi_cookie(email, password, headless=False):
    """
    自动登录 BaziAI 并获取 Cookie
    """
    
    print("🚀 启动浏览器...")
    driver = setup_driver(headless)
    
    if not driver:
        return None
    
    try:
        # 访问登录页面
        print("📱 访问 BaziAI 网站...")
        driver.get("https://www.bazi-ai.com/zh")
        time.sleep(3)
        
        # 保存初始截图
        driver.save_screenshot("step1_homepage.png")
        print("📸 截图: step1_homepage.png")
        
        # 尝试点击登录按钮
        print("🔍 查找登录按钮...")
        login_selectors = [
            ("xpath", "//button[contains(text(), '登录')]"),
            ("xpath", "//button[contains(text(), 'Login')]"),
            ("xpath", "//a[contains(text(), '登录')]"),
            ("xpath", "//a[contains(text(), 'Login')]"),
            ("css", "button.login"),
            ("css", "a.login"),
        ]
        wait_and_click(driver, login_selectors, description="登录按钮")
        time.sleep(2)
        driver.save_screenshot("step2_after_login_click.png")
        print("📸 截图: step2_after_login_click.png")
        
        # 尝试选择邮箱登录
        print("🔍 查找邮箱登录选项...")
        email_login_selectors = [
            ("xpath", "//button[contains(text(), '邮箱')]"),
            ("xpath", "//button[contains(text(), 'Email')]"),
            ("xpath", "//a[contains(text(), '邮箱')]"),
            ("xpath", "//div[contains(text(), '邮箱')]"),
        ]
        wait_and_click(driver, email_login_selectors, description="邮箱登录选项")
        time.sleep(2)
        driver.save_screenshot("step3_email_option.png")
        print("📸 截图: step3_email_option.png")
        
        # 输入邮箱
        print("📧 输入邮箱...")
        email_selectors = [
            ("css", "input[type='email']"),
            ("css", "input[name='email']"),
            ("css", "input[placeholder*='邮箱']"),
            ("css", "input[placeholder*='email']"),
            ("css", "input[placeholder*='Email']"),
            ("xpath", "//input[@type='email']"),
            ("xpath", "//input[contains(@placeholder, '邮箱')]"),
        ]
        if not wait_and_input(driver, email_selectors, email, description="邮箱"):
            driver.save_screenshot("error_email_not_found.png")
            return None
        time.sleep(1)
        driver.save_screenshot("step4_email_entered.png")
        print("📸 截图: step4_email_entered.png")
        
        # 输入密码
        print("🔑 输入密码...")
        password_selectors = [
            ("css", "input[type='password']"),
            ("css", "input[name='password']"),
            ("css", "input[placeholder*='密码']"),
            ("css", "input[placeholder*='password']"),
            ("css", "input[placeholder*='Password']"),
            ("xpath", "//input[@type='password']"),
        ]
        if not wait_and_input(driver, password_selectors, password, description="密码"):
            driver.save_screenshot("error_password_not_found.png")
            return None
        time.sleep(1)
        driver.save_screenshot("step5_password_entered.png")
        print("📸 截图: step5_password_entered.png")
        
        # 点击提交按钮
        print("🚪 提交登录...")
        submit_selectors = [
            ("css", "button[type='submit']"),
            ("xpath", "//button[@type='submit']"),
            ("xpath", "//button[contains(text(), '登录')]"),
            ("xpath", "//button[contains(text(), 'Login')]"),
            ("xpath", "//button[contains(text(), '提交')]"),
            ("xpath", "//button[contains(text(), 'Submit')]"),
            ("css", "button.submit"),
            ("css", "button.login-button"),
        ]
        
        # 如果找不到提交按钮，尝试按 Enter 键
        if not wait_and_click(driver, submit_selectors, description="提交按钮"):
            print("⚠️  未找到提交按钮，尝试按 Enter 键...")
            try:
                password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                password_input.send_keys(Keys.RETURN)
                print("✅ 已按 Enter 键提交")
            except:
                driver.save_screenshot("error_submit_failed.png")
                print("❌ 提交失败")
                return None
        
        time.sleep(5)
        driver.save_screenshot("step6_after_submit.png")
        print("📸 截图: step6_after_submit.png")
        
        # 等待登录成功
        print("⏳ 等待登录成功...")
        time.sleep(5)
        
        current_url = driver.current_url
        print(f"📍 当前 URL: {current_url}")
        
        # 提取 Session ID
        session_id = None
        if "/chat/" in current_url:
            session_id = current_url.split("/chat/")[-1].split("?")[0].split("#")[0]
            print(f"✅ 提取到 Session ID: {session_id}")
        else:
            print("⚠️  URL 中未找到 Session ID，尝试访问聊天页面...")
            driver.get("https://www.bazi-ai.com/zh/chat")
            time.sleep(3)
            current_url = driver.current_url
            if "/chat/" in current_url:
                session_id = current_url.split("/chat/")[-1].split("?")[0].split("#")[0]
                print(f"✅ 提取到 Session ID: {session_id}")
        
        driver.save_screenshot("step7_final_page.png")
        print("📸 截图: step7_final_page.png")
        
        # 获取所有 Cookies
        print("🍪 提取 Cookie...")
        cookies = driver.get_cookies()
        
        if not cookies:
            print("❌ 未获取到任何 Cookie")
            return None
        
        # 将 Cookies 转换为字符串格式
        cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        
        print(f"✅ 成功获取 Cookie (长度: {len(cookie_str)} 字符)")
        print(f"   Cookie 数量: {len(cookies)} 个")
        
        # 保存到文件
        result = {
            "session_id": session_id,
            "cookie": cookie_str,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cookies_detail": cookies,
            "current_url": current_url
        }
        
        with open("bazi_credentials.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print("💾 凭证已保存到 bazi_credentials.json")
        
        return result
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot("error_final.png")
        print("📸 错误截图已保存为 error_final.png")
        return None
        
    finally:
        print("🔚 关闭浏览器...")
        driver.quit()


def main():
    """主函数"""
    print("="*60)
    print("🔮 BaziAI Cookie 自动提取工具 V2")
    print("="*60)
    print()
    
    # 使用预设的凭证
    email = "291568499@qq.com"
    password = "hzy020618"
    
    print(f"📧 邮箱: {email}")
    print(f"🔑 密码: {'*' * len(password)}")
    print()
    print("⚠️  注意: 浏览器窗口会自动打开，请不要手动操作")
    print("📸 过程中会保存多个截图，方便调试")
    print()
    
    # 获取 Cookie
    result = get_bazi_cookie(email, password, headless=False)
    
    if result:
        print()
        print("="*60)
        print("✅ 成功获取凭证！")
        print("="*60)
        print()
        if result['session_id']:
            print(f"📜 Session ID:")
            print(f"   {result['session_id']}")
            print()
        print(f"🍪 Cookie (前100字符):")
        print(f"   {result['cookie'][:100]}...")
        print()
        print(f"📍 当前 URL:")
        print(f"   {result['current_url']}")
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
        print("   1. 查看截图文件 step*.png 和 error*.png")
        print("   2. 使用手动方法获取 Cookie")
        print("   3. 阅读 QUICK_COOKIE_GUIDE.md")
        print()
        print("📸 已保存的截图:")
        import os
        for f in os.listdir('.'):
            if f.endswith('.png'):
                print(f"   - {f}")
        print()


if __name__ == "__main__":
    main()
