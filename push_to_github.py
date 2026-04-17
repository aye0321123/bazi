#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送更新到 GitHub
"""

import subprocess
import sys

def run_command(command):
    """运行命令"""
    print(f"执行: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0

def main():
    print("="*60)
    print("推送更新到 GitHub")
    print("="*60)
    print()
    
    # 1. 添加文件
    print("[1/3] 添加文件...")
    if not run_command("git add ."):
        print("❌ 添加文件失败")
        return
    print("✅ 文件已添加")
    
    # 2. 提交
    print("\n[2/3] 提交更改...")
    if not run_command('git commit -m "Add brotli dependency for cloud deployment"'):
        print("⚠️  可能没有更改需要提交")
    else:
        print("✅ 更改已提交")
    
    # 3. 推送
    print("\n[3/3] 推送到 GitHub...")
    if not run_command("git push"):
        print("❌ 推送失败")
        return
    print("✅ 推送成功")
    
    print("\n" + "="*60)
    print("✅ 完成！")
    print("="*60)
    print("\nRailway 会自动检测更新并重新部署")
    print("等待 2-3 分钟后，再次访问你的应用")
    print("\n应用地址: https://web-production-c59ea.up.railway.app")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
