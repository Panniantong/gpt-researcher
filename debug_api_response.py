#!/usr/bin/env python3
"""
深度调试API响应，查找embedding数据
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def deep_debug_api():
    """深度调试API响应"""
    print("🔍 深度调试embedding API响应...")
    
    # 加载环境变量
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    url = f"{base_url}/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 测试不同的请求格式
    test_cases = [
        {
            "name": "标准格式 - 单个文本",
            "data": {
                "input": "test text",
                "model": "text-embedding-3-small"
            }
        },
        {
            "name": "标准格式 - 文本数组",
            "data": {
                "input": ["test text 1", "test text 2"],
                "model": "text-embedding-3-small"
            }
        },
        {
            "name": "不同编码格式",
            "data": {
                "input": "test text",
                "model": "text-embedding-3-small",
                "encoding_format": "float"
            }
        },
        {
            "name": "指定维度",
            "data": {
                "input": "test text",
                "model": "text-embedding-3-small",
                "dimensions": 3072
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"🧪 测试: {test_case['name']}")
        print(f"📤 请求数据: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(url, headers=headers, json=test_case['data'], timeout=30)
            
            print(f"📥 状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    print(f"📊 响应结构: {list(response_json.keys())}")
                    
                    # 详细分析每个字段
                    for key, value in response_json.items():
                        print(f"   {key}: {type(value)}")
                        if isinstance(value, dict):
                            print(f"      子字段: {list(value.keys())}")
                        elif isinstance(value, list):
                            print(f"      列表长度: {len(value)}")
                            if len(value) > 0:
                                print(f"      第一个元素类型: {type(value[0])}")
                                if isinstance(value[0], dict):
                                    print(f"      第一个元素字段: {list(value[0].keys())}")
                        elif value is not None:
                            print(f"      值: {str(value)[:100]}...")
                    
                    # 查找可能的embedding数据
                    print(f"\n🔍 查找embedding数据...")
                    embedding_found = False
                    
                    def search_embeddings(obj, path=""):
                        nonlocal embedding_found
                        if isinstance(obj, dict):
                            for k, v in obj.items():
                                new_path = f"{path}.{k}" if path else k
                                if k.lower() in ['embedding', 'embeddings', 'vector', 'vectors', 'data']:
                                    if isinstance(v, list) and len(v) > 0:
                                        if isinstance(v[0], (int, float)):
                                            print(f"   ✅ 找到embedding数据在: {new_path}")
                                            print(f"      类型: 数字列表, 长度: {len(v)}")
                                            print(f"      前5个值: {v[:5]}")
                                            embedding_found = True
                                        elif isinstance(v[0], list) and len(v[0]) > 0 and isinstance(v[0][0], (int, float)):
                                            print(f"   ✅ 找到embedding数据在: {new_path}")
                                            print(f"      类型: 嵌套数字列表, 外层长度: {len(v)}, 内层长度: {len(v[0])}")
                                            print(f"      第一个embedding前5个值: {v[0][:5]}")
                                            embedding_found = True
                                search_embeddings(v, new_path)
                        elif isinstance(obj, list):
                            for i, item in enumerate(obj):
                                search_embeddings(item, f"{path}[{i}]")
                    
                    search_embeddings(response_json)
                    
                    if not embedding_found:
                        print("   ❌ 未找到embedding数据")
                        
                        # 打印完整响应以供分析
                        response_str = json.dumps(response_json, indent=2)
                        print(f"\n📄 完整响应:")
                        print(response_str)
                    
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {e}")
                    print(f"原始响应: {response.text}")
            else:
                print(f"❌ 请求失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    print(f"\n{'='*50}")
    print("🔍 尝试其他可能的endpoint...")
    
    # 尝试其他可能的endpoint
    other_endpoints = [
        "/v1/embeddings",
        "/embeddings/create",
        "/api/embeddings"
    ]
    
    for endpoint in other_endpoints:
        test_url = f"{base_url.rstrip('/v1')}{endpoint}"
        print(f"\n🧪 测试endpoint: {test_url}")
        
        try:
            response = requests.post(
                test_url, 
                headers=headers, 
                json={"input": "test", "model": "text-embedding-3-small"},
                timeout=10
            )
            print(f"   状态码: {response.status_code}")
            if response.status_code != 404:
                print(f"   响应: {response.text[:200]}...")
        except Exception as e:
            print(f"   异常: {e}")

if __name__ == "__main__":
    deep_debug_api()
