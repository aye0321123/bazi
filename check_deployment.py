#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 Render 部署状态
"""

import requests
import sys

def check_deployment(api_url):
    """检查部署是否成功"""
    
    print("="*60)
    print("🔍 检查 Render 部署状态")
    print("="*60)
    
    # 测试 1: 健康检查
    print("\n[测试 1] 健康检查...")
    try:
        response = requests.get(f"{api_url}/health", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 部署成功！")
            print(f"   状态: {result['status']}")
            print(f"   时间: {result['timestamp']}")
            print(f"   服务: {result['service']}")
        else:
            print(f"❌ 部署失败或未完成")
            print(f"   状态码: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到 API")
        print(f"   可能原因:")
        print(f"   1. 部署还未完成（等待 2-3 分钟）")
        print(f"   2. API 地址错误")
        print(f"   3. Render 服务未启动")
        return False
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False
    
    # 测试 2: API 信息
    print("\n[测试 2] 获取 API 信息...")
    try:
        response = requests.get(f"{api_url}/", timeout=10)
        result = response.json()
        print(f"✅ API 信息:")
        print(f"   名称: {result['name']}")
        print(f"   版本: {result['version']}")
        print(f"   描述: {result['description']}")
    except Exception as e:
        print(f"⚠️  无法获取 API 信息: {e}")
    
    # 测试 3: API 文档
    print("\n[测试 3] 检查 API 文档...")
    try:
        response = requests.get(f"{api_url}/docs", timeout=10)
        if response.status_code == 200:
            print(f"✅ API 文档可访问")
            print(f"   地址: {api_url}/docs")
        else:
            print(f"⚠️  API 文档不可访问")
    except Exception as e:
        print(f"⚠️  无法访问 API 文档: {e}")
    
    print("\n" + "="*60)
    print("✅ 部署检查完成！")
    print("="*60)
    
    print("\n📡 你的 API 地址:")
    print(f"   {api_url}")
    
    print("\n📚 可用端点:")
    print(f"   GET  {api_url}/")
    print(f"   GET  {api_url}/docs")
    print(f"   GET  {api_url}/health")
    print(f"   POST {api_url}/api/chat")
    
    print("\n💡 下一步:")
    print("   1. 在你的代码中使用这个 API 地址")
    print("   2. 运行 test_cloud_api.py 进行完整测试")
    print("   3. 集成到你的网页中")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        print("请输入你的 Render API 地址:")
        print("例如: https://bazi-cloud-api.onrender.com")
        api_url = input("\nAPI 地址: ").strip()
    
    if not api_url:
        print("❌ 错误: 未提供 API 地址")
        sys.exit(1)
    
    # 移除末尾的斜杠
    api_url = api_url.rstrip('/')
    
    # 检查部署
    success = check_deployment(api_url)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
