#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BaziAI Web 应用
基于 Flask 的 Web 界面，支持多用户使用
"""

from flask import Flask, render_template, request, jsonify, session
import urllib3
import json
import os
from datetime import datetime
import secrets
import ssl

# Selenium 相关导入
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# 配置
BASE_URL = "https://www.bazi-ai.com"

# 创建自定义的 SSL 上下文
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 创建全局 HTTP 客户端
http_client = urllib3.PoolManager(
    ssl_context=ctx,
    cert_reqs='CERT_NONE',
    assert_hostname=False,
    timeout=urllib3.Timeout(connect=10.0, read=30.0)
)

class BaziAIClient:
    """BaziAI 客户端类"""
    
    def __init__(self, session_id, cookie):
        self.session_id = session_id
        self.cookie = cookie
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/json",
            "Cookie": cookie,
            "Origin": BASE_URL,
            "Referer": f"{BASE_URL}/zh/chat/{session_id}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def send_message(self, content):
        """发送消息"""
        url = f"{BASE_URL}/api/chat-session/{self.session_id}/messages"
        payload = {
            "session_id": self.session_id,
            "role": "user",
            "content": content,
            "id": ""
        }
        
        try:
            response = http_client.request(
                'POST',
                url,
                headers=self.headers,
                body=json.dumps(payload).encode('utf-8')
            )
            
            if response.status == 200:
                data = json.loads(response.data.decode('utf-8'))
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": f"状态码: {response.status}"}
                
        except Exception as e:
            print(f"[DEBUG] 发送消息错误: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": f"请求失败: {str(e)}"}
    
    def get_messages(self):
        """获取消息列表"""
        url = f"{BASE_URL}/api/chat-session/{self.session_id}/messages"
        
        print(f"[DEBUG] 请求 URL: {url}")
        print(f"[DEBUG] Cookie 长度: {len(self.cookie)}")
        print(f"[DEBUG] Session ID: {self.session_id}")
        
        try:
            response = http_client.request(
                'GET',
                url,
                headers=self.headers
            )
            
            print(f"[DEBUG] 响应状态码: {response.status}")
            print(f"[DEBUG] 响应内容长度: {len(response.data)}")
            
            if response.status == 200:
                data = json.loads(response.data.decode('utf-8'))
                print(f"[DEBUG] JSON 解析成功，消息数量: {len(data) if isinstance(data, list) else 'N/A'}")
                return {"success": True, "data": data}
            else:
                error_msg = f"状态码: {response.status}"
                print(f"[DEBUG] 请求失败: {error_msg}")
                return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"请求失败: {str(e)}"
            print(f"[DEBUG] {error_msg}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": error_msg}
    
    def create_new_session(self):
        """创建新的聊天会话"""
        url = f"{BASE_URL}/api/chat-session"
        
        # 更新 headers 中的 Referer
        headers = self.headers.copy()
        headers["Referer"] = f"{BASE_URL}/zh"
        
        print(f"[DEBUG] 创建新会话 URL: {url}")
        
        try:
            response = http_client.request(
                'POST',
                url,
                headers=headers,
                body=json.dumps({}).encode('utf-8')
            )
            
            print(f"[DEBUG] 响应状态码: {response.status}")
            
            if response.status == 200:
                data = json.loads(response.data.decode('utf-8'))
                print(f"[DEBUG] 新会话创建成功: {data}")
                
                if data.get('code') == 0:
                    new_session_id = data['data']['uuid']
                    return {
                        "success": True, 
                        "session_id": new_session_id,
                        "data": data['data']
                    }
                else:
                    return {"success": False, "error": data.get('message', '创建失败')}
            else:
                return {"success": False, "error": f"状态码: {response.status}"}
                
        except Exception as e:
            print(f"[DEBUG] 创建会话失败: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": f"创建会话失败: {str(e)}"}


@app.route('/')
def index():
    """首页"""
    try:
        return render_template('index.html')
    except Exception as e:
        # 如果模板加载失败，返回简单的 HTML
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>BaziAI API</title></head>
        <body>
            <h1>BaziAI API 服务正在运行</h1>
            <p>错误: {str(e)}</p>
            <p><a href="/health">健康检查</a></p>
            <p><a href="/test">测试页面</a></p>
            <p><a href="/chat">聊天记录</a></p>
        </body>
        </html>
        """, 200


@app.route('/chat')
def chat():
    """聊天记录页面"""
    return render_template('chat.html')


@app.route('/test')
def test_page():
    """测试页面"""
    return render_template('test.html')


@app.route('/debug')
def debug_page():
    """API 调试页面"""
    try:
        return render_template('debug.html')
    except Exception as e:
        return f"Error loading debug page: {str(e)}", 500


@app.route('/api/login', methods=['POST'])
def login():
    """登录接口 - 保存用户的 Session ID 和 Cookie"""
    data = request.json
    session_id = data.get('session_id', '').strip()
    cookie = data.get('cookie', '').strip()
    
    if not session_id or not cookie:
        return jsonify({"success": False, "error": "Session ID 和 Cookie 不能为空"})
    
    # 验证连接
    client = BaziAIClient(session_id, cookie)
    result = client.get_messages()
    
    # 添加详细日志
    print(f"[DEBUG] 登录验证结果: {result}")
    
    if result['success']:
        # 保存到 session
        session['session_id'] = session_id
        session['cookie'] = cookie
        return jsonify({"success": True, "message": "登录成功"})
    else:
        return jsonify({"success": False, "error": f"连接失败: {result['error']}"})


@app.route('/api/logout', methods=['POST'])
def logout():
    """登出"""
    session.clear()
    return jsonify({"success": True, "message": "已登出"})


@app.route('/api/send', methods=['POST'])
def send_message():
    """发送消息"""
    if 'session_id' not in session:
        return jsonify({"success": False, "error": "未登录"})
    
    data = request.json
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({"success": False, "error": "消息内容不能为空"})
    
    client = BaziAIClient(session['session_id'], session['cookie'])
    result = client.send_message(content)
    
    return jsonify(result)


def trigger_ai_with_selenium(session_id, cookie_str):
    """使用 Selenium 后台触发 AI（无头模式）"""
    if not SELENIUM_AVAILABLE:
        print(f"[DEBUG] ❌ Selenium 未安装")
        return {"success": False, "error": "Selenium 未安装"}
    
    try:
        import time
        
        print(f"[DEBUG] 使用 Selenium 触发 AI...")
        
        # 配置 Chrome 选项（无头模式）
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式，不显示浏览器
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # 使用 webdriver-manager 自动管理 ChromeDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        try:
            # 访问主页设置 Cookie
            driver.get(BASE_URL)
            time.sleep(1)
            
            # 解析并添加 Cookie
            for cookie_pair in cookie_str.split('; '):
                if '=' in cookie_pair:
                    name, value = cookie_pair.split('=', 1)
                    try:
                        driver.add_cookie({
                            'name': name,
                            'value': value,
                            'domain': '.bazi-ai.com'
                        })
                    except:
                        pass  # 忽略无效的 Cookie
            
            # 访问聊天页面
            chat_url = f"{BASE_URL}/zh/chat/{session_id}"
            print(f"[DEBUG] 访问页面: {chat_url}")
            driver.get(chat_url)
            
            # 等待页面加载和 AI 生成
            print(f"[DEBUG] 等待 AI 生成回复...")
            time.sleep(10)  # 等待 10 秒让 AI 生成
            
            print(f"[DEBUG] ✅ Selenium 触发完成")
            return {"success": True}
            
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"[DEBUG] ❌ Selenium 错误: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


@app.route('/api/send-and-wait', methods=['POST'])
def send_and_wait():
    """发送消息并等待 AI 回复（使用 Selenium 触发）"""
    if 'cookie' not in session:
        return jsonify({"success": False, "error": "未登录"})
    
    data = request.json
    content = data.get('content', '').strip()
    use_selenium = data.get('use_selenium', True)  # 默认使用 Selenium
    max_wait = data.get('max_wait', 30)  # 默认等待30秒
    check_interval = data.get('check_interval', 2)  # 默认2秒检查一次
    
    if not content:
        return jsonify({"success": False, "error": "消息内容不能为空"})
    
    # 步骤1: 创建新会话
    print("[DEBUG] 创建新会话...")
    temp_client = BaziAIClient("temp", session['cookie'])
    create_result = temp_client.create_new_session()
    
    if not create_result['success']:
        return jsonify({
            "success": False, 
            "error": f"创建新会话失败: {create_result.get('error')}"
        })
    
    new_session_id = create_result['session_id']
    print(f"[DEBUG] 新会话创建成功: {new_session_id}")
    
    # 使用新会话
    client = BaziAIClient(new_session_id, session['cookie'])
    session['session_id'] = new_session_id
    
    # 步骤2: 获取当前消息数
    messages_result = client.get_messages()
    if not messages_result['success']:
        return jsonify({"success": False, "error": "无法获取消息列表"})
    
    initial_count = len(messages_result['data'])
    
    # 步骤3: 发送消息
    send_result = client.send_message(content)
    if not send_result['success']:
        return jsonify(send_result)
    
    print(f"[DEBUG] 消息已发送")
    
    # 步骤4: 使用 Selenium 触发 AI（如果启用）
    if use_selenium:
        selenium_result = trigger_ai_with_selenium(new_session_id, session['cookie'])
        if not selenium_result['success']:
            print(f"[DEBUG] Selenium 失败，将使用纯轮询模式")
    
    # 步骤5: 轮询等待 AI 回复
    print(f"[DEBUG] 开始轮询检查 AI 回复...")
    import time
    start_time = time.time()
    attempts = 0
    
    while time.time() - start_time < max_wait:
        attempts += 1
        time.sleep(check_interval)
        
        # 获取最新消息
        messages_result = client.get_messages()
        if messages_result['success']:
            messages = messages_result['data']
            current_count = len(messages)
            
            print(f"[DEBUG] 尝试 {attempts}: 消息数 {current_count} (初始: {initial_count})")
            
            # 检查是否有新的 assistant 消息
            if current_count > initial_count + 1:
                new_messages = messages[initial_count:]
                
                for msg in new_messages:
                    if msg.get('role') == 'assistant':
                        elapsed = int(time.time() - start_time)
                        print(f"[DEBUG] ✅ 收到 AI 回复！等待时间: {elapsed}秒")
                        return jsonify({
                            "success": True,
                            "user_message": send_result['data'],
                            "ai_reply": msg,
                            "wait_time": elapsed,
                            "attempts": attempts,
                            "new_session_id": new_session_id,
                            "method": "selenium" if use_selenium else "polling"
                        })
    
    # 超时未收到回复
    elapsed = int(time.time() - start_time)
    print(f"[DEBUG] ⏰ 等待超时: {elapsed}秒")
    return jsonify({
        "success": False,
        "error": "等待超时，AI 未回复",
        "user_message": send_result['data'],
        "wait_time": elapsed,
        "attempts": attempts,
        "new_session_id": new_session_id,
        "suggestion": "AI 可能需要更长时间生成回复，请稍后刷新查看"
    })


@app.route('/api/messages', methods=['GET'])
def get_messages():
    """获取消息列表"""
    if 'session_id' not in session:
        return jsonify({"success": False, "error": "未登录"})
    
    client = BaziAIClient(session['session_id'], session['cookie'])
    result = client.get_messages()
    
    return jsonify(result)


@app.route('/api/export', methods=['GET'])
def export_messages():
    """导出聊天记录"""
    if 'session_id' not in session:
        return jsonify({"success": False, "error": "未登录"})
    
    client = BaziAIClient(session['session_id'], session['cookie'])
    result = client.get_messages()
    
    if result['success']:
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bazi_chat_{timestamp}.json"
        
        return jsonify({
            "success": True,
            "filename": filename,
            "data": result['data']
        })
    else:
        return jsonify(result)


@app.route('/api/create-session', methods=['POST'])
def create_session_route():
    """创建新的聊天会话"""
    if 'cookie' not in session:
        return jsonify({"success": False, "error": "未登录，请先设置 Cookie"})
    
    # 使用临时 session_id 创建客户端（仅用于创建新会话）
    client = BaziAIClient("temp", session['cookie'])
    result = client.create_new_session()
    
    if result['success']:
        # 更新 session 中的 session_id
        session['session_id'] = result['session_id']
        return jsonify(result)
    else:
        return jsonify(result)


@app.route('/api/create-and-send', methods=['POST'])
def create_and_send():
    """创建新对话并发送消息"""
    if 'cookie' not in session:
        return jsonify({"success": False, "error": "未登录，请先设置 Cookie"})
    
    data = request.json
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({"success": False, "error": "消息内容不能为空"})
    
    # 步骤1: 创建新会话
    client = BaziAIClient("temp", session['cookie'])
    create_result = client.create_new_session()
    
    if not create_result['success']:
        return jsonify(create_result)
    
    new_session_id = create_result['session_id']
    
    # 步骤2: 发送消息
    client = BaziAIClient(new_session_id, session['cookie'])
    send_result = client.send_message(content)
    
    if send_result['success']:
        # 更新 session 中的 session_id
        session['session_id'] = new_session_id
        
        return jsonify({
            "success": True,
            "session_id": new_session_id,
            "message_data": send_result['data'],
            "chat_url": f"{BASE_URL}/zh/chat/{new_session_id}"
        })
    else:
        return jsonify(send_result)


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    """测试与 BaziAI 的连接"""
    import socket
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
    
    # 测试 1: DNS 解析
    try:
        ip = socket.gethostbyname("www.bazi-ai.com")
        results["tests"].append({
            "name": "DNS 解析",
            "success": True,
            "message": f"成功解析到 IP: {ip}"
        })
    except Exception as e:
        results["tests"].append({
            "name": "DNS 解析",
            "success": False,
            "message": f"DNS 解析失败: {str(e)}"
        })
    
    # 测试 2: HTTP 连接
    try:
        response = http_client.request('GET', "https://www.bazi-ai.com", timeout=10.0)
        results["tests"].append({
            "name": "HTTP 连接",
            "success": True,
            "message": f"成功连接，状态码: {response.status}"
        })
    except Exception as e:
        results["tests"].append({
            "name": "HTTP 连接",
            "success": False,
            "message": f"连接失败: {str(e)}"
        })
    
    # 测试 3: API 端点
    try:
        test_url = f"{BASE_URL}/api/chat-session/test/messages"
        response = http_client.request('GET', test_url, timeout=10.0)
        results["tests"].append({
            "name": "API 端点",
            "success": True,
            "message": f"API 可访问，状态码: {response.status}"
        })
    except Exception as e:
        results["tests"].append({
            "name": "API 端点",
            "success": False,
            "message": f"API 访问失败: {str(e)}"
        })
    
    return jsonify(results)


if __name__ == '__main__':
    # 从环境变量获取端口，默认 5000
    port = int(os.environ.get('PORT', 5000))
    # 生产环境不使用 debug 模式
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
