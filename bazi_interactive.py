#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BaziAI 交互式命令行工具
提供友好的命令行界面来与 BaziAI 交互
"""

import sys
import time
from bazi_api import BaziAI

def print_banner():
    """打印欢迎横幅"""
    print("\n" + "="*60)
    print("🔮 BaziAI 命令行工具")
    print("="*60)

def print_menu():
    """打印菜单"""
    print("\n📋 可用命令:")
    print("  1. send    - 发送消息")
    print("  2. get     - 获取聊天记录")
    print("  3. save    - 保存聊天记录到文件")
    print("  4. clear   - 清屏")
    print("  5. help    - 显示帮助")
    print("  6. exit    - 退出程序")
    print("-"*60)

def get_user_input(prompt):
    """获取用户输入"""
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 再见！")
        sys.exit(0)

def clear_screen():
    """清屏"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """主函数"""
    print_banner()
    
    # 获取配置信息
    print("\n⚙️  配置信息")
    print("-"*60)
    
    session_id = get_user_input("请输入 Session ID: ")
    if not session_id:
        print("❌ Session ID 不能为空！")
        return
    
    print("\n请输入完整的 Cookie（可以粘贴多行，输入空行结束）:")
    cookie_lines = []
    while True:
        line = get_user_input("")
        if not line:
            break
        cookie_lines.append(line)
    
    cookie = " ".join(cookie_lines)
    if not cookie:
        print("❌ Cookie 不能为空！")
        return
    
    # 创建客户端
    print("\n✅ 正在连接到 BaziAI...")
    client = BaziAI(session_id, cookie)
    print("✅ 连接成功！")
    
    # 主循环
    while True:
        print_menu()
        command = get_user_input("\n请输入命令 (输入数字或命令名): ").lower()
        
        if command in ['1', 'send']:
            # 发送消息
            print("\n📤 发送消息")
            print("-"*60)
            content = get_user_input("请输入消息内容: ")
            
            if content:
                print("\n⏳ 正在发送...")
                result = client.send_message(content)
                
                if result:
                    print(f"\n✅ 发送成功！")
                    print(f"消息ID: {result.get('id')}")
                    print(f"时间: {result.get('created_at')}")
                    
                    # 询问是否等待回复
                    wait = get_user_input("\n是否等待 AI 回复？(y/n): ").lower()
                    if wait == 'y':
                        print("⏳ 等待 AI 回复中...")
                        time.sleep(3)  # 等待3秒
                        
                        messages = client.get_messages()
                        if messages:
                            # 只显示最后一条消息（AI的回复）
                            last_msg = messages[-1]
                            if last_msg.get('role') == 'assistant':
                                print("\n🤖 AI 回复:")
                                print("-"*60)
                                print(last_msg.get('content', ''))
                                print("-"*60)
            else:
                print("❌ 消息内容不能为空！")
        
        elif command in ['2', 'get']:
            # 获取聊天记录
            print("\n📥 获取聊天记录")
            print("-"*60)
            print("⏳ 正在获取...")
            
            messages = client.get_messages()
            if messages:
                client.print_messages(messages)
            else:
                print("❌ 没有找到聊天记录")
        
        elif command in ['3', 'save']:
            # 保存聊天记录
            print("\n💾 保存聊天记录")
            print("-"*60)
            
            filename = get_user_input("请输入文件名（留空使用默认名称）: ")
            
            print("⏳ 正在获取聊天记录...")
            messages = client.get_messages()
            
            if messages:
                if filename:
                    client.save_messages_to_file(messages, filename)
                else:
                    client.save_messages_to_file(messages)
            else:
                print("❌ 没有找到聊天记录")
        
        elif command in ['4', 'clear']:
            # 清屏
            clear_screen()
            print_banner()
        
        elif command in ['5', 'help']:
            # 帮助
            print("\n📖 帮助信息")
            print("-"*60)
            print("这是一个用于与 BaziAI 交互的命令行工具。")
            print("\n使用步骤:")
            print("1. 输入 Session ID 和 Cookie")
            print("2. 使用 'send' 命令发送消息")
            print("3. 使用 'get' 命令查看聊天记录")
            print("4. 使用 'save' 命令保存聊天记录")
            print("\n提示:")
            print("- Session ID 可以从浏览器地址栏获取")
            print("- Cookie 可以从浏览器开发者工具的 Network 标签获取")
            print("- 发送消息后可以选择等待 AI 回复")
        
        elif command in ['6', 'exit', 'quit', 'q']:
            # 退出
            print("\n👋 感谢使用，再见！")
            break
        
        else:
            print(f"\n❌ 未知命令: {command}")
            print("💡 输入 'help' 查看帮助信息")
        
        # 暂停一下
        time.sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已中断，再见！")
        sys.exit(0)
