#!/usr/bin/env python3
"""
测试逆向API中使用的模型是否可用
Test script to check if models used in reverse API are available

这个脚本会测试：
1. LLM模型（通过逆向API）：gpt-4o-mini, gpt-4.1, o4-mini
2. Embedding模型（通过官方OpenAI API）：text-embedding-3-small
3. 搜索引擎：Tavily API
"""

import os
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime
import sys

# 添加项目路径以便导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gpt_researcher.config.config import Config
from gpt_researcher.llm_provider.generic.base import GenericLLMProvider
from gpt_researcher.memory.embeddings import get_embeddings_model


class ModelTester:
    """模型可用性测试器"""
    
    def __init__(self):
        """初始化测试器"""
        self.config = Config()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "llm_models": {},
            "embedding_model": {},
            "search_engines": {},
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0
            }
        }
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """记录测试结果"""
        print(f"[{status}] {test_name}")
        if details:
            print(f"    详情: {details}")
        
        self.results["summary"]["total_tests"] += 1
        if status == "PASS":
            self.results["summary"]["passed"] += 1
        else:
            self.results["summary"]["failed"] += 1
    
    async def test_llm_model(self, model_type: str, provider: str, model: str) -> bool:
        """测试LLM模型"""
        try:
            print(f"\n🧠 测试 {model_type} 模型: {provider}:{model}")
            
            # 创建LLM实例
            llm_provider = GenericLLMProvider.create_llm(
                provider=provider,
                model=model,
                temperature=0.1,
                max_tokens=100
            )
            
            # 测试简单对话
            test_prompt = "请回答：1+1等于几？只需要回答数字。"
            response = await llm_provider.get_chat_response(test_prompt)
            
            if response and len(response.strip()) > 0:
                self.log_test(f"{model_type} ({provider}:{model})", "PASS", f"响应: {response[:50]}...")
                self.results["llm_models"][model_type] = {
                    "provider": provider,
                    "model": model,
                    "status": "available",
                    "response_sample": response[:100]
                }
                return True
            else:
                self.log_test(f"{model_type} ({provider}:{model})", "FAIL", "无响应")
                self.results["llm_models"][model_type] = {
                    "provider": provider,
                    "model": model,
                    "status": "no_response",
                    "error": "Empty response"
                }
                return False
                
        except Exception as e:
            error_msg = str(e)
            self.log_test(f"{model_type} ({provider}:{model})", "FAIL", error_msg)
            self.results["llm_models"][model_type] = {
                "provider": provider,
                "model": model,
                "status": "error",
                "error": error_msg
            }
            return False
    
    async def test_embedding_model(self) -> bool:
        """测试Embedding模型"""
        try:
            print(f"\n🔍 测试 Embedding 模型: {self.config.embedding}")
            
            # 获取embedding模型
            embeddings = get_embeddings_model(
                provider=self.config.embedding_provider,
                model=self.config.embedding_model,
                config=self.config
            )
            
            # 测试embedding
            test_text = "这是一个测试文本"
            embedding_result = await embeddings.aembed_query(test_text)
            
            if embedding_result and len(embedding_result) > 0:
                self.log_test(f"Embedding ({self.config.embedding})", "PASS", 
                            f"向量维度: {len(embedding_result)}")
                self.results["embedding_model"] = {
                    "provider": self.config.embedding_provider,
                    "model": self.config.embedding_model,
                    "status": "available",
                    "dimension": len(embedding_result)
                }
                return True
            else:
                self.log_test(f"Embedding ({self.config.embedding})", "FAIL", "无法生成向量")
                self.results["embedding_model"] = {
                    "provider": self.config.embedding_provider,
                    "model": self.config.embedding_model,
                    "status": "no_embedding",
                    "error": "Empty embedding result"
                }
                return False
                
        except Exception as e:
            error_msg = str(e)
            self.log_test(f"Embedding ({self.config.embedding})", "FAIL", error_msg)
            self.results["embedding_model"] = {
                "provider": self.config.embedding_provider,
                "model": self.config.embedding_model,
                "status": "error",
                "error": error_msg
            }
            return False
    
    async def test_tavily_search(self) -> bool:
        """测试Tavily搜索引擎"""
        try:
            print(f"\n🔎 测试 Tavily 搜索引擎")
            
            # 导入Tavily搜索器
            from gpt_researcher.retrievers.tavily.tavily import TavilySearch
            
            # 创建搜索实例
            tavily = TavilySearch()
            
            # 测试搜索
            test_query = "Python programming"
            search_results = await tavily.search(test_query, max_results=2)
            
            if search_results and len(search_results) > 0:
                self.log_test("Tavily Search", "PASS", f"返回 {len(search_results)} 个结果")
                self.results["search_engines"]["tavily"] = {
                    "status": "available",
                    "results_count": len(search_results)
                }
                return True
            else:
                self.log_test("Tavily Search", "FAIL", "无搜索结果")
                self.results["search_engines"]["tavily"] = {
                    "status": "no_results",
                    "error": "Empty search results"
                }
                return False
                
        except Exception as e:
            error_msg = str(e)
            self.log_test("Tavily Search", "FAIL", error_msg)
            self.results["search_engines"]["tavily"] = {
                "status": "error",
                "error": error_msg
            }
            return False
    
    def print_environment_info(self):
        """打印环境信息"""
        print("=" * 60)
        print("🔧 环境配置信息")
        print("=" * 60)
        print(f"OPENAI_API_KEY: {'✓ 已设置' if os.getenv('OPENAI_API_KEY') else '✗ 未设置'}")
        print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL', '未设置')}")
        print(f"TAVILY_API_KEY: {'✓ 已设置' if os.getenv('TAVILY_API_KEY') else '✗ 未设置'}")
        print(f"EMBEDDING: {self.config.embedding}")
        print(f"FAST_LLM: {self.config.fast_llm}")
        print(f"SMART_LLM: {self.config.smart_llm}")
        print(f"STRATEGIC_LLM: {self.config.strategic_llm}")
        print()
    
    def print_summary(self):
        """打印测试总结"""
        print("\n" + "=" * 60)
        print("📊 测试总结")
        print("=" * 60)
        summary = self.results["summary"]
        print(f"总测试数: {summary['total_tests']}")
        print(f"通过: {summary['passed']} ✓")
        print(f"失败: {summary['failed']} ✗")
        print(f"成功率: {(summary['passed']/summary['total_tests']*100):.1f}%")
        
        if summary['failed'] > 0:
            print("\n⚠️  失败的测试:")
            for category, tests in self.results.items():
                if category in ["llm_models", "embedding_model", "search_engines"]:
                    if isinstance(tests, dict):
                        for test_name, result in tests.items():
                            if result.get("status") != "available":
                                print(f"  - {test_name}: {result.get('error', 'Unknown error')}")
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始模型可用性测试")
        self.print_environment_info()
        
        # 测试LLM模型
        await self.test_llm_model("FAST_LLM", self.config.fast_llm_provider, self.config.fast_llm_model)
        await self.test_llm_model("SMART_LLM", self.config.smart_llm_provider, self.config.smart_llm_model)
        await self.test_llm_model("STRATEGIC_LLM", self.config.strategic_llm_provider, self.config.strategic_llm_model)
        
        # 测试Embedding模型
        await self.test_embedding_model()
        
        # 测试搜索引擎
        await self.test_tavily_search()
        
        # 打印总结
        self.print_summary()
        
        # 保存结果到文件
        with open("model_test_results.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n📄 详细结果已保存到: model_test_results.json")


async def main():
    """主函数"""
    tester = ModelTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
