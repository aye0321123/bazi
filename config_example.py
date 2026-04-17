#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件示例
复制此文件为 config.py 并填入您的实际信息
"""

# 会话ID - 从浏览器地址栏获取
# 示例: https://www.bazi-ai.com/zh/chat/26a7d080-283c-43c9-a741-23d8dfcb8512
SESSION_ID = "你的会话ID"

# Cookie - 从浏览器开发者工具获取
# 步骤:
# 1. 打开开发者工具 (F12)
# 2. 切换到 Network 标签
# 3. 在网站上发送一条消息
# 4. 点击 messages 请求
# 5. 在 Headers 中找到 Cookie 字段
# 6. 复制完整的 Cookie 值
COOKIE = """你的完整Cookie"""

# 可选配置
CONFIG = {
    # 请求超时时间（秒）
    "timeout": 30,
    
    # 请求间隔时间（秒）- 避免请求过快
    "request_interval": 2,
    
    # 保存文件的默认目录
    "save_directory": "./chat_logs",
    
    # 是否自动保存聊天记录
    "auto_save": True,
}
