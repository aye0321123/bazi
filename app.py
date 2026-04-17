#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BaziAI Web 应用
基于 Flask 的 Web 界面，支持多用户使用
"""

from flask import Flask, render_template, request, jsonify, session
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os
from datetime import datetime
import secrets
import urllib3

# 禁用 SSL 警告（仅用于调试）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# 配置
BASE_URL = "https://www.bazi-ai.com"

# 创建一个带重试机制的 session
def create_session():
    """创建带重试机制的 requests session"""
    session = requests.Session()
    
    # 配置重试策略
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

class BaziAIClient:
    """BaziAI 客户端类"""
    
    def __init__(self, session_id, cookie):
        self.session_id = session_id
        self.cookie = cookie
        self.session = create_session()
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
            # 使用 session 发送请求，带重试机制
            response = self.session.post(
                url, 
                headers=self.headers, 
                json=payload, 
                timeout=30,
                verify=True
            )
            response.raise_for_status()
            
            # 直接使用 response.json()，requests 会自动处理压缩
            data = response.json()
            return {"success": True, "data": data}
                
        except requests.exceptions.SSLError as e:
            print(f"[DEBUG] SSL 错误: {e}")
            return {"success": False, "error": f"SSL 连接错误，请检查网络设置"}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "请求超时，请检查网络连接"}
        except requests.exceptions.JSONDecodeError as e:
            return {"success": False, "error": f"JSON 解析失败: {str(e)}"}
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" (状态码: {e.response.status_code})"
            return {"success": False, "error": error_msg}
        except Exception as e:
            print(f"[DEBUG] 未知错误: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": f"未知错误: {str(e)}"}
    
    def get_messages(self):
        """获取消息列表"""
        url = f"{BASE_URL}/api/chat-session/{self.session_id}/messages"
        
        print(f"[DEBUG] 请求 URL: {url}")
        
        try:
            # 使用 session 发送请求，带重试机制
            response = self.session.get(
                url, 
                headers=self.headers, 
                timeout=30,
                verify=True  # 验证 SSL 证书
            )
            
            print(f"[DEBUG] 响应状态码: {response.status_code}")
            print(f"[DEBUG] 响应内容长度: {len(response.content)}")
            
            response.raise_for_status()
            
            # 直接使用 response.json()，requests 会自动处理压缩
            data = response.json()
            print(f"[DEBUG] JSON 解析成功，消息数量: {len(data) if isinstance(data, list) else 'N/A'}")
            return {"success": True, "data": data}
                
        except requests.exceptions.SSLError as e:
            print(f"[DEBUG] SSL 错误: {e}")
            return {"success": False, "error": f"SSL 连接错误，请检查网络设置"}
        except requests.exceptions.Timeout:
            print(f"[DEBUG] 请求超时")
            return {"success": False, "error": "请求超时，请检查网络连接"}
        except requests.exceptions.JSONDecodeError as e:
            print(f"[DEBUG] JSON 解析失败: {e}")
            return {"success": False, "error": f"JSON 解析失败: {str(e)}"}
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" (状态码: {e.response.status_code})"
            print(f"[DEBUG] 请求异常: {error_msg}")
            return {"success": False, "error": error_msg}
        except Exception as e:
            print(f"[DEBUG] 未知错误: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": f"未知错误: {str(e)}"}
    
    def create_new_session(self):
        """创建新的聊天会话"""
        url = f"{BASE_URL}/api/chat-session"
        
        # 更新 headers 中的 Referer
        headers = self.headers.copy()
        headers["Referer"] = f"{BASE_URL}/zh"
        
        print(f"[DEBUG] 创建新会话 URL: {url}")
        
        try:
            response = self.session.post(
                url,
                headers=headers,
                json={},
                timeout=30,
                verify=True
            )
            
            print(f"[DEBUG] 响应状态码: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
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
                
        except Exception as e:
            print(f"[DEBUG] 创建会话失败: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": f"创建会话失败: {str(e)}"}


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


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


if __name__ == '__main__':
    # 从环境变量获取端口，默认 5000
    port = int(os.environ.get('PORT', 5000))
    # 生产环境不使用 debug 模式
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
