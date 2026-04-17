#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天机阁 - 现代国学风算命网站
融合传统文化与现代科技
"""

from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# 配置
BASE_URL = "https://www.bazi-ai.com"

class BaziAIClient:
    """BaziAI 客户端类"""
    
    def __init__(self, session_id, cookie):
        self.session_id = session_id
        self.cookie = cookie
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/json",
            "Cookie": cookie,
            "Origin": BASE_URL,
            "Referer": f"{BASE_URL}/zh/chat/{session_id}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
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
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_messages(self):
        """获取消息列表"""
        url = f"{BASE_URL}/api/chat-session/{self.session_id}/messages"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}


@app.route('/')
def index():
    """首页"""
    return render_template('fortune_index.html')


@app.route('/api/login', methods=['POST'])
def login():
    """登录接口"""
    data = request.json
    session_id = data.get('session_id', '').strip()
    cookie = data.get('cookie', '').strip()
    
    if not session_id or not cookie:
        return jsonify({"success": False, "error": "Session ID 和 Cookie 不能为空"})
    
    # 验证连接
    client = BaziAIClient(session_id, cookie)
    result = client.get_messages()
    
    if result['success']:
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"天机阁_命理记录_{timestamp}.json"
        
        return jsonify({
            "success": True,
            "filename": filename,
            "data": result['data']
        })
    else:
        return jsonify(result)


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
