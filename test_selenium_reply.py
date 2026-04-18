#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Selenium 自动获取 AI 回复
"""

import urllib3
import json
import ssl
import time
from datetime import datetime

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 禁用警告
urllib3.disable_warnings()

# 创建 SSL 上下文
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

http = urllib3.PoolManager(
    ssl_context=ctx,
    cert_reqs='CERT_NONE',
    assert_hostname=False
)

# 读取 Cookie
with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)
    cookie = creds['cookie']

base_url = "https://www.bazi-ai.com"

def create_new_session():
    """创建新的聊天会话"""
    url = f"{base_url}/api/chat-session"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Origin": base_url,
        "Referer": f"{base_url}/zh",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = http.request('POST', url, headers=headers, body=json.dumps({}).encode('utf-8'))
        if response.status == 200:
            result = json.loads(response.data.decode('utf-8'))
            if result.get('code') == 0:
                return {"success": True, "session_id": result['data']['uuid']}
        return {"success": False, "error": f"状态码: {response.status}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def send_message(session_id, content):
    """发送消息"""
    url = f"{base_url}/api/chat-session/{session_id}/messages"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Origin": base_url,
        "Referer": f"{base_url}/zh/chat/{session_id}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    payload = {
        "session_id": session_id,
        "role": "user",
        "content": content,
        "id": ""
    }
    
    try:
        response = http.request('POST', url, headers=headers, body=json.dumps(payload).encode('utf-8'))
        if response.status == 200:
            result = json.loads(response.data.decode('utf-8'))
            return {"success": True, "data": result}
        else:
            return {"success": False, "error": f"状态码: {response.status}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_messages(session_id):
    """获取消息列表"""
    url = f"{base_url}/api/chat-session/{session_id}/messages"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = http.request('GET', url, headers=headers)
        if response.status == 200:
            messages = json.loads(response.data.decode('utf-8'))
            return {"success": True, "data": messages}
        else:
            return {"success": False, "error": f"状态码: {response.status}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def trigger_ai_with_selenium(session_id):
    """使用 Selenium 触发 AI"""
    print(f"\n🌐 使用 Selenium 访问页面...")
    
    # 配置 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # 使用 webdriver-manager
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    try:
        # 访问主页
        driver.get(base_url)
        time.sleep(1)
        
        # 添加 Cookie
        for cookie_pair in cookie.split('; '):
            if '=' in cookie_pair:
                name, value = cookie_pair.split('=', 1)
                try:
                    driver.add_cookie({
                        'name': name,
                        'value': value,
                        'domain': '.bazi-ai.com'
                    })
                except:
                    pass
        
        # 访问聊天页面
        chat_url = f"{base_url}/zh/chat/{session_id}"
        print(f"   访问: {chat_url}")
        driver.get(chat_url)
        
        # 等待 AI 生成
        print(f"   等待 10 秒让 AI 生成回复...")
        time.sleep(10)
        
        print(f"   ✅ Selenium 完成")
        return {"success": True}
        
    finally:
        driver.quit()

def wait_for_reply(session_id, initial_count, max_wait=30, check_interval=2):
    """等待 AI 回复"""
    print(f"\n⏳ 检查 AI 回复（最多等待 {max_wait} 秒）...")
    
    start_time = time.time()
    attempts = 0
    
    while time.time() - start_time < max_wait:
        attempts += 1
        elapsed = int(time.time() - start_time)
        
        result = get_messages(session_id)
        
        if result['success']:
            messages = result['data']
            current_count = len(messages)
            
            print(f"   [{elapsed}s] 尝试 {attempts}: 消息数 {current_count} (初始: {initial_count})", end='\r')
            
            if current_count > initial_count + 1:
                new_messages = messages[initial_count:]
                for msg in new_messages:
                    if msg.get('role') == 'assistant':
                        print(f"\n\n✅ 收到 AI 回复！（等待时间: {elapsed}秒）")
                        return msg
        
        time.sleep(check_interval)
    
    print(f"\n\n⏰ 检查超时（{max_wait}秒）")
    return None

def main():
    print("=" * 80)
    print("🧪 测试 Selenium 自动获取 AI 回复")
    print("=" * 80)
    
    message = "请用一句话回复：今天天气怎么样？"
    
    # 步骤 1: 创建新会话
    print("\n📝 步骤 1: 创建新会话...")
    result = create_new_session()
    
    if not result['success']:
        print(f"❌ 创建失败: {result['error']}")
        return
    
    session_id = result['session_id']
    print(f"   ✅ 新会话: {session_id}")
    
    # 步骤 2: 发送消息
    print(f"\n📤 步骤 2: 发送消息...")
    print(f"   内容: {message}")
    
    result = send_message(session_id, message)
    
    if not result['success']:
        print(f"❌ 发送失败: {result['error']}")
        return
    
    print(f"   ✅ 消息已发送")
    
    # 获取初始消息数
    result = get_messages(session_id)
    initial_count = len(result['data'])
    
    # 步骤 3: 使用 Selenium 触发
    print(f"\n🤖 步骤 3: 使用 Selenium 触发 AI...")
    result = trigger_ai_with_selenium(session_id)
    
    if not result['success']:
        print(f"❌ Selenium 失败")
        return
    
    # 步骤 4: 等待回复
    print(f"\n🔄 步骤 4: 检查 AI 回复...")
    
    ai_reply = wait_for_reply(session_id, initial_count, max_wait=30, check_interval=2)
    
    if ai_reply:
        print("\n" + "=" * 80)
        print("🤖 AI 回复内容:")
        print("=" * 80)
        print(ai_reply.get('content'))
        print("=" * 80)
        
        print(f"\n🎉 测试成功！Selenium 方案可以获取 AI 回复！")
        print(f"\n💡 现在你可以在网页上使用 '🤖 自动获取回复' 按钮了！")
    else:
        print("\n⚠️  未能获取到 AI 回复")
        print(f"💡 请访问: {base_url}/zh/chat/{session_id}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
