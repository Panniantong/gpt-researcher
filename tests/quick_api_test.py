#!/usr/bin/env python3
"""
快速API测试脚本
用于快速验证逆向API和官方API的连接状态
"""

import os
import sys
import asyncio
import requests
import json
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 加载环境变量
load_dotenv()

def test_reverse_openai_api():
    """测试逆向OpenAI API连接"""
    print("🔍 测试逆向OpenAI API连接...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL', 'https://gptgod.cloud/v1')
    
    if not api_key:
        print("  ❌ OPENAI_API_KEY 未设置")
        return False
    
    try:
        # 测试模型列表接口
        url = f"{base_url}/models"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        print(f"  📡 请求URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('data', [])
            print(f"  ✅ 连接成功！发现 {len(models)} 个可用模型")
            
            # 显示前几个模型
            if models:
                print("  📋 可用模型示例:")
                for i, model in enumerate(models[:5]):
                    model_id = model.get('id', 'unknown')
                    print(f"    {i+1}. {model_id}")
                if len(models) > 5:
                    print(f"    ... 还有 {len(models) - 5} 个模型")
            
            return True
        else:
            print(f"  ❌ 请求失败: HTTP {response.status_code}")
            print(f"  📝 响应: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("  ❌ 请求超时")
        return False
    except requests.exceptions.ConnectionError:
        print("  ❌ 连接错误，请检查网络或URL")
        return False
    except Exception as e:
        print(f"  ❌ 未知错误: {e}")
        return False

def test_reverse_openai_chat():
    """测试逆向OpenAI API的聊天功能"""
    print("\n🤖 测试逆向OpenAI API聊天功能...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL', 'https://gptgod.cloud/v1')
    
    if not api_key:
        print("  ❌ OPENAI_API_KEY 未设置")
        return False
    
    try:
        url = f"{base_url}/chat/completions"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 测试数据
        data = {
            "model": "gpt-4o-mini",  # 使用常见的模型名
            "messages": [
                {"role": "user", "content": "请回答：1+1等于几？只需要回答数字。"}
            ],
            "max_tokens": 10,
            "temperature": 0.1
        }
        
        print(f"  📡 请求URL: {url}")
        print(f"  🎯 测试模型: {data['model']}")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"  ✅ 聊天测试成功！")
                print(f"  💬 AI回复: {content.strip()}")
                return True
            else:
                print(f"  ❌ 响应格式异常: {result}")
                return False
        else:
            print(f"  ❌ 请求失败: HTTP {response.status_code}")
            print(f"  📝 响应: {response.text[:300]}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_official_openai_embedding():
    """测试官方OpenAI API的embedding功能"""
    print("\n🔍 测试官方OpenAI API embedding功能...")
    
    api_key = os.getenv('OPENAI_EMBEDDING_API_KEY')
    base_url = os.getenv('OPENAI_EMBEDDING_BASE_URL', 'https://api.openai.com/v1')
    
    if not api_key:
        print("  ❌ OPENAI_EMBEDDING_API_KEY 未设置")
        return False
    
    try:
        url = f"{base_url}/embeddings"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 测试数据
        data = {
            "model": "text-embedding-3-small",
            "input": "这是一个测试文本"
        }
        
        print(f"  📡 请求URL: {url}")
        print(f"  🎯 测试模型: {data['model']}")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'data' in result and len(result['data']) > 0:
                embedding = result['data'][0]['embedding']
                print(f"  ✅ Embedding测试成功！")
                print(f"  📊 向量维度: {len(embedding)}")
                print(f"  🔢 前5个值: {embedding[:5]}")
                return True
            else:
                print(f"  ❌ 响应格式异常: {result}")
                return False
        else:
            print(f"  ❌ 请求失败: HTTP {response.status_code}")
            print(f"  📝 响应: {response.text[:300]}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_tavily_api():
    """测试Tavily API连接"""
    print("\n🔍 测试Tavily API连接...")
    
    api_key = os.getenv('TAVILY_API_KEY')
    
    if not api_key:
        print("  ❌ TAVILY_API_KEY 未设置")
        return False
    
    try:
        url = "https://api.tavily.com/search"
        headers = {
            'Content-Type': 'application/json'
        }
        
        # 测试数据
        data = {
            "api_key": api_key,
            "query": "Python programming",
            "max_results": 2
        }
        
        print(f"  📡 请求URL: {url}")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'results' in result:
                results_count = len(result['results'])
                print(f"  ✅ Tavily API测试成功！")
                print(f"  📊 搜索结果数量: {results_count}")
                return True
            else:
                print(f"  ❌ 响应格式异常: {result}")
                return False
        else:
            print(f"  ❌ 请求失败: HTTP {response.status_code}")
            print(f"  📝 响应: {response.text[:300]}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 GPT-Researcher 快速API测试工具")
    print("=" * 50)
    
    # 显示环境变量状态
    print("\n📋 环境变量检查:")
    env_vars = [
        'OPENAI_API_KEY',
        'OPENAI_BASE_URL', 
        'OPENAI_EMBEDDING_API_KEY',
        'OPENAI_EMBEDDING_BASE_URL',
        'TAVILY_API_KEY'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # 隐藏API密钥的大部分内容
            if 'API_KEY' in var:
                display_value = f"{value[:8]}...{value[-8:]}" if len(value) > 16 else "已设置"
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: 未设置")
    
    print("\n" + "=" * 50)
    
    # 运行测试
    results = []
    
    # 测试逆向OpenAI API
    results.append(("逆向OpenAI API连接", test_reverse_openai_api()))
    results.append(("逆向OpenAI API聊天", test_reverse_openai_chat()))
    
    # 测试官方OpenAI API
    results.append(("官方OpenAI Embedding", test_official_openai_embedding()))
    
    # 测试Tavily API
    results.append(("Tavily搜索API", test_tavily_api()))
    
    # 显示总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print("=" * 50)
    
    success_count = 0
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {test_name:20} | {status}")
        if success:
            success_count += 1
    
    print("-" * 50)
    print(f"总计: {success_count}/{len(results)} 项测试通过")
    
    if success_count == len(results):
        print("🎉 所有API都可以正常使用！")
    elif success_count > 0:
        print("⚠️  部分API可用，请检查失败的API配置")
    else:
        print("🚨 所有API都无法使用，请检查配置和网络连接")

if __name__ == "__main__":
    main()
