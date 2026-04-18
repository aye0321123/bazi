#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BaziAI Cloud API
逆向工程的 BaziAI API 封装，部署到云端
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib3
import json
import ssl
import os
from datetime import datetime

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# BaziAI 官方 API 地址
BASE_URL = "https://www.bazi-ai.com"

# 创建 SSL 上下文
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 创建 HTTP 客户端
http_client = urllib3.PoolManager(
    ssl_context=ctx,
    cert_reqs='CERT_NONE',
    assert_hostname=False,
    timeout=urllib3.Timeout(connect=30.0, read=60.0),
    retries=urllib3.Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
)


class BaziAPIClient:
    """BaziAI API 客户端"""
    
    def __init__(self, cookie):
        self.cookie = cookie
    
    def _get_headers(self, session_id=None):
        """获取请求头"""
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/json",
            "Cookie": self.cookie,
            "Origin": BASE_URL,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        if session_id:
            headers["Referer"] = f"{BASE_URL}/zh/chat/{session_id}"
        else:
            headers["Referer"] = f"{BASE_URL}/zh"
        
        return headers
    
    def create_session(self):
        """创建新的聊天会话"""
        url = f"{BASE_URL}/api/chat-session"
        headers = self._get_headers()
        
        try:
            response = http_client.request(
                'POST',
                url,
                headers=headers,
                body=json.dumps({}).encode('utf-8')
            )
            
            if response.status == 200:
                data = json.loads(response.data.decode('utf-8'))
                
                if data.get('code') == 0:
                    return {
                        "success": True,
                        "session_id": data['data']['uuid'],
                        "data": data['data']
                    }
                else:
                    return {"success": False, "error": data.get('message', '创建失败')}
            else:
                return {"success": False, "error": f"状态码: {response.status}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_message(self, session_id, content):
        """发送消息"""
        url = f"{BASE_URL}/api/chat-session/{session_id}/messages"
        headers = self._get_headers(session_id)
        
        payload = {
            "session_id": session_id,
            "role": "user",
            "content": content,
            "id": ""
        }
        
        try:
            response = http_client.request(
                'POST',
                url,
                headers=headers,
                body=json.dumps(payload).encode('utf-8')
            )
            
            if response.status == 200:
                data = json.loads(response.data.decode('utf-8'))
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": f"状态码: {response.status}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_messages(self, session_id):
        """获取消息列表"""
        url = f"{BASE_URL}/api/chat-session/{session_id}/messages"
        headers = self._get_headers(session_id)
        
        try:
            response = http_client.request(
                'GET',
                url,
                headers=headers
            )
            
            if response.status == 200:
                messages = json.loads(response.data.decode('utf-8'))
                return {"success": True, "messages": messages}
            else:
                return {"success": False, "error": f"状态码: {response.status}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}


# ============================================================
# API 路由
# ============================================================

@app.route('/')
def index():
    """API 首页"""
    return jsonify({
        "name": "BaziAI Cloud API",
        "version": "1.0.0",
        "description": "逆向工程的 BaziAI API 封装",
        "endpoints": {
            "POST /api/session/create": "创建新会话",
            "POST /api/session/<session_id>/send": "发送消息",
            "GET /api/session/<session_id>/messages": "获取消息列表",
            "POST /api/chat": "一键对话（创建会话+发送消息）"
        },
        "docs": "/docs",
        "health": "/health"
    })


@app.route('/docs')
def docs():
    """API 文档"""
    return jsonify({
        "title": "BaziAI Cloud API 文档",
        "base_url": request.host_url,
        "authentication": {
            "type": "Cookie",
            "description": "需要在请求头中提供 BaziAI 的 Cookie",
            "header": "X-Bazi-Cookie"
        },
        "endpoints": [
            {
                "method": "POST",
                "path": "/api/session/create",
                "description": "创建新的聊天会话",
                "headers": {
                    "X-Bazi-Cookie": "你的 BaziAI Cookie"
                },
                "response": {
                    "success": True,
                    "session_id": "xxx-xxx-xxx",
                    "data": {}
                }
            },
            {
                "method": "POST",
                "path": "/api/session/<session_id>/send",
                "description": "在指定会话中发送消息",
                "headers": {
                    "X-Bazi-Cookie": "你的 BaziAI Cookie"
                },
                "body": {
                    "content": "你的问题"
                },
                "response": {
                    "success": True,
                    "data": {}
                }
            },
            {
                "method": "GET",
                "path": "/api/session/<session_id>/messages",
                "description": "获取指定会话的所有消息",
                "headers": {
                    "X-Bazi-Cookie": "你的 BaziAI Cookie"
                },
                "response": {
                    "success": True,
                    "messages": []
                }
            },
            {
                "method": "POST",
                "path": "/api/chat",
                "description": "一键对话（创建会话+发送消息）",
                "headers": {
                    "X-Bazi-Cookie": "你的 BaziAI Cookie"
                },
                "body": {
                    "content": "你的问题"
                },
                "response": {
                    "success": True,
                    "session_id": "xxx-xxx-xxx",
                    "user_message": {},
                    "chat_url": "https://www.bazi-ai.com/zh/chat/xxx"
                }
            }
        ]
    })


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "BaziAI Cloud API"
    })


@app.route('/api/session/create', methods=['POST'])
def create_session():
    """创建新会话"""
    cookie = request.headers.get('X-Bazi-Cookie')
    
    if not cookie:
        return jsonify({"success": False, "error": "缺少 X-Bazi-Cookie 请求头"}), 400
    
    client = BaziAPIClient(cookie)
    result = client.create_session()
    
    return jsonify(result)


@app.route('/api/session/<session_id>/send', methods=['POST'])
def send_message(session_id):
    """发送消息"""
    cookie = request.headers.get('X-Bazi-Cookie')
    
    if not cookie:
        return jsonify({"success": False, "error": "缺少 X-Bazi-Cookie 请求头"}), 400
    
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({"success": False, "error": "缺少 content 参数"}), 400
    
    client = BaziAPIClient(cookie)
    result = client.send_message(session_id, content)
    
    return jsonify(result)


@app.route('/api/session/<session_id>/messages', methods=['GET'])
def get_messages(session_id):
    """获取消息列表"""
    cookie = request.headers.get('X-Bazi-Cookie')
    
    if not cookie:
        return jsonify({"success": False, "error": "缺少 X-Bazi-Cookie 请求头"}), 400
    
    client = BaziAPIClient(cookie)
    result = client.get_messages(session_id)
    
    return jsonify(result)


@app.route('/api/chat', methods=['POST'])
def chat():
    """一键对话（创建会话+发送消息）"""
    cookie = request.headers.get('X-Bazi-Cookie')
    
    if not cookie:
        return jsonify({"success": False, "error": "缺少 X-Bazi-Cookie 请求头"}), 400
    
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({"success": False, "error": "缺少 content 参数"}), 400
    
    client = BaziAPIClient(cookie)
    
    # 1. 创建会话
    create_result = client.create_session()
    if not create_result['success']:
        return jsonify(create_result)
    
    session_id = create_result['session_id']
    
    # 2. 发送消息
    send_result = client.send_message(session_id, content)
    if not send_result['success']:
        return jsonify(send_result)
    
    # 3. 返回结果
    return jsonify({
        "success": True,
        "session_id": session_id,
        "user_message": send_result['data'],
        "chat_url": f"{BASE_URL}/zh/chat/{session_id}",
        "note": "AI 回复需要在官网查看，或稍后调用 /api/session/<session_id>/messages 获取"
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
