#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BaziAI API 调用脚本
用于发送消息和获取聊天记录
"""

import requests
import json
from datetime import datetime

class BaziAI:
    def __init__(self, session_id, cookie):
        """
        初始化 BaziAI 客户端
        
        Args:
            session_id: 会话ID (从URL中获取)
            cookie: 完整的Cookie字符串
        """
        self.base_url = "https://www.bazi-ai.com"
        self.session_id = session_id
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/json",
            "Cookie": cookie,
            "Origin": "https://www.bazi-ai.com",
            "Referer": f"https://www.bazi-ai.com/zh/chat/{session_id}",
            "Sec-Ch-Ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        }
    
    def send_message(self, content):
        """
        发送消息到 BaziAI
        
        Args:
            content: 要发送的消息内容
            
        Returns:
            dict: API 响应数据
        """
        url = f"{self.base_url}/api/chat-session/{self.session_id}/messages"
        
        payload = {
            "session_id": self.session_id,
            "role": "user",
            "content": content,
            "id": ""
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            # 检查响应内容
            if not response.text:
                print(f"❌ 服务器返回空响应")
                return None
            
            try:
                result = response.json()
                print(f"✅ 消息发送成功！")
                print(f"消息ID: {result.get('id')}")
                print(f"发送时间: {result.get('created_at')}")
                return result
            except json.JSONDecodeError as e:
                print(f"❌ JSON 解析失败: {e}")
                print(f"响应内容: {response.text[:200]}")
                return None
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 发送消息失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"状态码: {e.response.status_code}")
                print(f"响应内容: {e.response.text[:200]}")
            return None
    
    def get_messages(self):
        """
        获取当前会话的所有消息
        
        Returns:
            list: 消息列表
        """
        url = f"{self.base_url}/api/chat-session/{self.session_id}/messages"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # 检查响应内容
            if not response.text:
                print(f"❌ 服务器返回空响应")
                return []
            
            try:
                messages = response.json()
                print(f"✅ 成功获取 {len(messages)} 条消息")
                return messages
            except json.JSONDecodeError as e:
                print(f"❌ JSON 解析失败: {e}")
                print(f"响应内容: {response.text[:200]}")
                return []
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取消息失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"状态码: {e.response.status_code}")
                print(f"响应内容: {e.response.text[:200]}")
            return []
    
    def print_messages(self, messages):
        """
        格式化打印消息列表
        
        Args:
            messages: 消息列表
        """
        print("\n" + "="*60)
        print("聊天记录")
        print("="*60)
        
        for msg in messages:
            role = "👤 用户" if msg.get('role') == 'user' else "🤖 AI"
            content = msg.get('content', '')
            created_at = msg.get('created_at', '')
            
            print(f"\n{role} [{created_at}]")
            print(f"{content}")
            print("-"*60)
    
    def save_messages_to_file(self, messages, filename=None):
        """
        保存消息到文件
        
        Args:
            messages: 消息列表
            filename: 文件名（可选）
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bazi_chat_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            print(f"✅ 聊天记录已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")


def main():
    """主函数 - 使用示例"""
    
    # ⚠️ 请替换为您自己的信息
    SESSION_ID = "26a7d080-283c-43c9-a741-23d8dfcb8512"
    
    COOKIE = """NEXT_LOCALE=zh; _ga=GA1.1.1899898920.1776086692; __Host-authjs.csrf-token=dc53b14177158adc3fa16ca2c3d3573a9836541975c215c45d5693ae3a8aaf4d%7Cf8648798852afc2334960251aa70c22b3f75003c155711c71a3979f47cc083df; __Secure-authjs.callback-url=https%3A%2F%2Fwww.bazi-ai.com; _ga_V7V71Z9C7T=GS2.1.s1776342169$o14$g1$t1776345108$j5b$l0$h0; __Secure-authjs.session-token=eyJhbGciOiJkaXliaXliLCJlbmNiOiJBMjU2R0NNIiwiYWx0IjoiUEJFUzItSFMyNTYrQTEyOEtXIiwiZW5jIjoiQTI1NkdDTSIsInAyYyI6MTAwMDAsInAycyI6IlVHUW5IM3lwQjZlbVZ1VjN4NkxmY3VJbmF6NmhWbS01YlV1LUxmTUFPY0s4U3E2X0p1ODlvekF6MnQzMXI4TDRWVmp1MnlKUVVlM3N4Z2dacWVEcG1kVTcxMUs3Z0JQZ0FaSG9aRWc0dUVFVk1tbXZjX3pBVnRFeXBFMFdsYWtiNU1QN2FvcktDSHFtUnRVbVZrRnZkTzBPTDBQdVNhOEVucFdyRk8tTjU0TTR3b3l0YU5oazV2b1FDeGhWU0lSUll4NTNDeHBHMzNlRGhQRkRPT04waGhWVklzcjk3eEFqLVFnVkh6ZTFrSDhTaHRaRWJKUVI5aEE4VVBlbGEtMFMtVEdiY0o4ZWhhLW1DXzE4bndjUkhubXB3bXVBYzhOaVhqN2pHZzNIZVFWOHRTaGRUa0F5aW1yYzZzUm94ZzFmbjh0eVZIck53MFpZNzRnLlFNY2EyNHVLbzlhbTUtUXhhOTREekV2WHFvbGlBbzZqX3hwZjBYZ19YVjQ"""
    
    # 创建客户端
    client = BaziAI(SESSION_ID, COOKIE)
    
    # 示例1: 发送消息
    print("\n📤 发送消息...")
    client.send_message("请帮我分析一下2026年的运势")
    
    # 示例2: 获取所有消息
    print("\n📥 获取聊天记录...")
    messages = client.get_messages()
    
    # 示例3: 打印消息
    if messages:
        client.print_messages(messages)
        
        # 示例4: 保存到文件
        client.save_messages_to_file(messages)


if __name__ == "__main__":
    main()
