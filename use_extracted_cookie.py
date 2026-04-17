#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用提取的 Cookie 快速开始
"""

import json
from bazi_api import BaziAI

def main():
    """使用提取的 Cookie"""
    
    print("="*60)
    print("🔮 BaziAI 快速开始")
    print("="*60)
    print()
    
    # 读取凭证
    try:
        with open('bazi_credentials.json', 'r', encoding='utf-8') as f:
            creds = json.load(f)
    except FileNotFoundError:
        print("❌ 未找到 bazi_credentials.json 文件")
        print("💡 请先运行: python get_cookie_v2.py")
        return
    
    session_id = creds.get('session_id') or "26a7d080-283c-43c9-a741-23d8dfcb8512"
    cookie = creds.get('cookie')
    
    print(f"📜 Session ID: {session_id}")
    print(f"🍪 Cookie: 已加载")
    print(f"⏰ 提取时间: {creds.get('timestamp')}")
    print()
    
    # 创建客户端
    client = BaziAI(session_id, cookie)
    
    # 主循环
    print("="*60)
    print("💬 开始对话（输入 'quit' 退出，'history' 查看历史）")
    print("="*60)
    print()
    
    while True:
        try:
            # 获取用户输入
            user_input = input("👤 您: ").strip()
            
            if not user_input:
                continue
            
            # 退出命令
            if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                print("\n👋 再见！")
                break
            
            # 查看历史命令
            if user_input.lower() in ['history', 'h', '历史']:
                print("\n📜 获取历史消息...")
                messages = client.get_messages()
                client.print_messages(messages)
                print()
                continue
            
            # 保存命令
            if user_input.lower() in ['save', 's', '保存']:
                print("\n💾 保存聊天记录...")
                messages = client.get_messages()
                client.save_messages_to_file(messages)
                print()
                continue
            
            # 发送消息
            print()
            result = client.send_message(user_input)
            
            if result:
                print(f"\n✅ 消息已发送")
                print(f"   消息ID: {result.get('id')}")
                print(f"   时间: {result.get('created_at')}")
                print()
            else:
                print("\n❌ 发送失败")
                print()
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            print()
    
    print()
    print("="*60)
    print("✅ 会话结束")
    print("="*60)
    print()
    print("💡 提示:")
    print("   - 重新运行此脚本继续对话")
    print("   - 访问 http://127.0.0.1:5000 使用 Web 界面")
    print("   - 查看 SUCCESS_SUMMARY.md 了解更多")
    print()


if __name__ == "__main__":
    main()
