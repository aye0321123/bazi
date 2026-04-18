#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Selenium 是否正确安装
"""

print("=" * 80)
print("🧪 测试 Selenium 安装")
print("=" * 80)

# 测试 1: 检查 Selenium 是否安装
print("\n📦 测试 1: 检查 Selenium 是否安装...")
try:
    import selenium
    print(f"   ✅ Selenium 已安装 (版本: {selenium.__version__})")
except ImportError:
    print(f"   ❌ Selenium 未安装")
    print(f"   💡 请运行: pip install selenium")
    exit(1)

# 测试 2: 检查 ChromeDriver
print("\n🚗 测试 2: 检查 ChromeDriver...")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    print("   尝试启动 Chrome...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com")
    print(f"   ✅ ChromeDriver 工作正常")
    print(f"   页面标题: {driver.title}")
    driver.quit()
    
except Exception as e:
    print(f"   ❌ ChromeDriver 错误: {e}")
    print(f"\n   💡 解决方法:")
    print(f"   方法 1: pip install webdriver-manager")
    print(f"   方法 2: 手动下载 ChromeDriver")
    print(f"           https://chromedriver.chromium.org/downloads")
    exit(1)

# 测试 3: 测试访问 BaziAI
print("\n🌐 测试 3: 测试访问 BaziAI...")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.bazi-ai.com")
    time.sleep(2)
    
    print(f"   ✅ 成功访问 BaziAI")
    print(f"   页面标题: {driver.title}")
    
    driver.quit()
    
except Exception as e:
    print(f"   ❌ 访问失败: {e}")
    exit(1)

print("\n" + "=" * 80)
print("🎉 所有测试通过！Selenium 已正确安装并可以使用！")
print("=" * 80)
print("\n💡 下一步:")
print("   1. 启动 Flask: python app.py")
print("   2. 访问: http://127.0.0.1:5000")
print("   3. 点击 '🤖 自动获取回复' 按钮")
print("   4. AI 回复将自动显示在你的网页上！")
print("\n" + "=" * 80)
