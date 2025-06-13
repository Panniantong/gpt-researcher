#!/usr/bin/env python3
"""
快速模型测试脚本 - 简化版本
Quick model test script - simplified version

用于快速检查逆向API的基本连接性和模型可用性
"""

import os
import asyncio
import json
import requests
from datetime import datetime


class QuickModelTester:
    """快速模型测试器"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://gptgod.cloud/v1")
        self.tavily_key = os.getenv("TAVILY_API_KEY")
        
        # 要测试的模型列表
        self.models_to_test = [
            "gpt-4o-mini",      # FAST_LLM
            "gpt-4.1",          # SMART_LLM  
            "o4-mini",          # STRATEGIC_LLM
            "text-embedding-3-small"  # EMBEDDING
        ]
    
    def print_config(self):
        """打印配置信息"""
        print("🔧 配置检查")
        print("-" * 40)
        print(f"API Key: {'✓ 已设置' if self.api_key else '✗ 未设置'}")
        print(f"Base URL: {self.base_url}")
        print(f"Tavily Key: {'✓ 已设置' if self.tavily_key else '✗ 未设置'}")
        print()
    
    def test_api_connection(self):
        """测试API连接"""
        print("🌐 测试API连接")
        print("-" * 40)
        
        try:
            # 测试获取模型列表
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                models_data = response.json()
                available_models = [model["id"] for model in models_data.get("data", [])]
                print(f"✓ API连接成功")
                print(f"✓ 可用模型数量: {len(available_models)}")
                
                # 检查我们需要的模型是否可用
                print("\n📋 模型可用性检查:")
                for model in self.models_to_test:
                    if model in available_models:
                        print(f"  ✓ {model} - 可用")
                    else:
                        print(f"  ✗ {model} - 不可用")
                        # 查找相似的模型
                        similar = [m for m in available_models if model.split('-')[0] in m]
                        if similar:
                            print(f"    💡 相似模型: {', '.join(similar[:3])}")
                
                return True, available_models
            else:
                print(f"✗ API连接失败: HTTP {response.status_code}")
                print(f"  响应: {response.text}")
                return False, []
                
        except Exception as e:
            print(f"✗ API连接异常: {str(e)}")
            return False, []
    
    def test_chat_completion(self, model: str):
        """测试聊天完成"""
        print(f"\n💬 测试聊天模型: {model}")
        print("-" * 40)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "请回答：1+1等于几？只需要回答数字。"}
                ],
                "max_tokens": 10,
                "temperature": 0.1
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print(f"✓ {model} 响应成功")
                print(f"  回答: {content.strip()}")
                return True
            else:
                print(f"✗ {model} 请求失败: HTTP {response.status_code}")
                print(f"  响应: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ {model} 测试异常: {str(e)}")
            return False
    
    def test_embedding(self, model: str):
        """测试嵌入模型"""
        print(f"\n🔍 测试嵌入模型: {model}")
        print("-" * 40)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "input": "这是一个测试文本"
            }
            
            response = requests.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                embedding = result["data"][0]["embedding"]
                print(f"✓ {model} 嵌入成功")
                print(f"  向量维度: {len(embedding)}")
                return True
            else:
                print(f"✗ {model} 请求失败: HTTP {response.status_code}")
                print(f"  响应: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ {model} 测试异常: {str(e)}")
            return False
    
    def test_tavily_search(self):
        """测试Tavily搜索"""
        print(f"\n🔎 测试Tavily搜索")
        print("-" * 40)
        
        if not self.tavily_key:
            print("✗ Tavily API Key未设置")
            return False
        
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "api_key": self.tavily_key,
                "query": "Python programming",
                "max_results": 2
            }
            
            response = requests.post(
                "https://api.tavily.com/search",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                results = result.get("results", [])
                print(f"✓ Tavily搜索成功")
                print(f"  结果数量: {len(results)}")
                return True
            else:
                print(f"✗ Tavily搜索失败: HTTP {response.status_code}")
                print(f"  响应: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Tavily搜索异常: {str(e)}")
            return False
    
    def run_quick_test(self):
        """运行快速测试"""
        print("🚀 开始快速模型测试")
        print("=" * 50)
        
        # 配置检查
        self.print_config()
        
        # API连接测试
        connection_ok, available_models = self.test_api_connection()
        
        if not connection_ok:
            print("\n❌ API连接失败，无法继续测试")
            return
        
        # 测试聊天模型
        chat_models = ["gpt-4o-mini", "gpt-4.1", "o4-mini"]
        chat_results = []
        
        for model in chat_models:
            if model in available_models:
                result = self.test_chat_completion(model)
                chat_results.append((model, result))
            else:
                print(f"\n💬 跳过不可用的模型: {model}")
                chat_results.append((model, False))
        
        # 测试嵌入模型
        embedding_model = "text-embedding-3-small"
        if embedding_model in available_models:
            embedding_result = self.test_embedding(embedding_model)
        else:
            print(f"\n🔍 跳过不可用的嵌入模型: {embedding_model}")
            embedding_result = False
        
        # 测试搜索
        search_result = self.test_tavily_search()
        
        # 总结
        print("\n" + "=" * 50)
        print("📊 测试总结")
        print("=" * 50)
        
        print("聊天模型:")
        for model, result in chat_results:
            status = "✓" if result else "✗"
            print(f"  {status} {model}")
        
        print(f"嵌入模型:")
        print(f"  {'✓' if embedding_result else '✗'} {embedding_model}")
        
        print(f"搜索引擎:")
        print(f"  {'✓' if search_result else '✗'} Tavily")
        
        # 计算成功率
        total_tests = len(chat_results) + 1 + 1  # 聊天模型 + 嵌入 + 搜索
        passed_tests = sum(1 for _, result in chat_results if result) + (1 if embedding_result else 0) + (1 if search_result else 0)
        
        print(f"\n总体成功率: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
        
        if passed_tests == total_tests:
            print("🎉 所有测试通过！你的逆向API配置正常。")
        else:
            print("⚠️  部分测试失败，请检查相关配置。")


def main():
    """主函数"""
    tester = QuickModelTester()
    tester.run_quick_test()


if __name__ == "__main__":
    main()
