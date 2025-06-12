#!/usr/bin/env python3
"""
调试embedding API的原始响应
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_raw_embedding_api():
    """直接测试embedding API的原始响应"""
    print("🔍 测试原始embedding API响应...")
    
    # 加载环境变量
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    print(f"API Key: {api_key[:20]}...")
    print(f"Base URL: {base_url}")
    
    # 构建请求
    url = f"{base_url}/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "input": "This is a test sentence.",
        "model": "text-embedding-3-large"
    }
    
    try:
        print(f"\n📤 发送请求到: {url}")
        print(f"📤 请求数据: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, headers=headers, json=data)
        
        print(f"\n📥 响应状态码: {response.status_code}")
        print(f"📥 响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                print(f"\n📊 响应JSON结构:")
                print(f"   类型: {type(response_json)}")
                print(f"   键: {list(response_json.keys()) if isinstance(response_json, dict) else 'Not a dict'}")
                
                if isinstance(response_json, dict):
                    # 检查data字段
                    if 'data' in response_json:
                        data_field = response_json['data']
                        print(f"   data字段类型: {type(data_field)}")
                        print(f"   data字段值: {data_field}")
                        
                        if data_field is None:
                            print("   ❌ data字段为None - 这就是问题所在！")
                        elif isinstance(data_field, list):
                            print(f"   ✅ data字段是列表，长度: {len(data_field)}")
                            if len(data_field) > 0:
                                first_item = data_field[0]
                                print(f"   第一个元素类型: {type(first_item)}")
                                print(f"   第一个元素: {first_item}")
                                
                                if isinstance(first_item, dict) and 'embedding' in first_item:
                                    embedding = first_item['embedding']
                                    print(f"   embedding类型: {type(embedding)}")
                                    print(f"   embedding长度: {len(embedding) if hasattr(embedding, '__len__') else 'N/A'}")
                                    if isinstance(embedding, list) and len(embedding) > 0:
                                        print(f"   embedding前5个值: {embedding[:5]}")
                        else:
                            print(f"   ❌ data字段不是列表: {data_field}")
                    else:
                        print("   ❌ 响应中没有data字段")
                        
                    # 打印完整响应（截断）
                    response_str = json.dumps(response_json, indent=2)
                    if len(response_str) > 1000:
                        print(f"\n📄 完整响应（前1000字符）:")
                        print(response_str[:1000] + "...")
                    else:
                        print(f"\n📄 完整响应:")
                        print(response_str)
                        
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"原始响应: {response.text[:500]}...")
        else:
            print(f"❌ 请求失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()

def test_multiple_inputs():
    """测试多个输入的情况"""
    print(f"\n🔍 测试多个输入...")
    
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    url = f"{base_url}/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "input": ["First text", "Second text"],
        "model": "text-embedding-3-large"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            response_json = response.json()
            print(f"响应结构: {list(response_json.keys()) if isinstance(response_json, dict) else 'Not a dict'}")
            
            if 'data' in response_json:
                data_field = response_json['data']
                print(f"data字段: {type(data_field)}, 值: {data_field}")
        else:
            print(f"请求失败: {response.text}")
            
    except Exception as e:
        print(f"异常: {e}")

if __name__ == "__main__":
    print("🚀 开始调试embedding API原始响应...")
    test_raw_embedding_api()
    test_multiple_inputs()
    print("\n✅ 调试完成")
