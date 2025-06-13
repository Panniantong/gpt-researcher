#!/usr/bin/env python3
"""
逆向API模型测试脚本
测试所有配置的模型是否可用，包括LLM和Embedding模型
"""

import asyncio
import os
import sys
import traceback
from typing import Dict, List, Tuple
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gpt_researcher.config.config import Config
from gpt_researcher.utils.llm import create_chat_completion
from gpt_researcher.memory.embeddings import Memory

# 加载环境变量
load_dotenv()

class ModelTester:
    """模型测试器类"""
    
    def __init__(self):
        self.config = Config()
        self.results = {}
        
    def print_config_info(self):
        """打印当前配置信息"""
        print("=" * 60)
        print("🔧 当前配置信息")
        print("=" * 60)
        
        # API配置
        print("\n📡 API配置:")
        print(f"  OPENAI_API_KEY: {'✓ 已设置' if os.getenv('OPENAI_API_KEY') else '✗ 未设置'}")
        print(f"  OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL', '未设置')}")
        print(f"  OPENAI_EMBEDDING_API_KEY: {'✓ 已设置' if os.getenv('OPENAI_EMBEDDING_API_KEY') else '✗ 未设置'}")
        print(f"  OPENAI_EMBEDDING_BASE_URL: {os.getenv('OPENAI_EMBEDDING_BASE_URL', '未设置')}")
        print(f"  TAVILY_API_KEY: {'✓ 已设置' if os.getenv('TAVILY_API_KEY') else '✗ 未设置'}")
        
        # LLM配置
        print("\n🤖 LLM模型配置:")
        print(f"  FAST_LLM: {self.config.fast_llm}")
        print(f"  SMART_LLM: {self.config.smart_llm}")
        print(f"  STRATEGIC_LLM: {self.config.strategic_llm}")
        print(f"  解析后的Fast LLM: {self.config.fast_llm_provider}:{self.config.fast_llm_model}")
        print(f"  解析后的Smart LLM: {self.config.smart_llm_provider}:{self.config.smart_llm_model}")
        print(f"  解析后的Strategic LLM: {self.config.strategic_llm_provider}:{self.config.strategic_llm_model}")
        
        # Embedding配置
        print("\n🔍 Embedding配置:")
        print(f"  EMBEDDING: {self.config.embedding}")
        print(f"  解析后的Embedding: {self.config.embedding_provider}:{self.config.embedding_model}")
        
        # Token限制
        print("\n📊 Token限制:")
        print(f"  FAST_TOKEN_LIMIT: {self.config.fast_token_limit}")
        print(f"  SMART_TOKEN_LIMIT: {self.config.smart_token_limit}")
        print(f"  STRATEGIC_TOKEN_LIMIT: {self.config.strategic_token_limit}")
        
        print("\n" + "=" * 60)

    async def test_llm_model(self, model_name: str, provider: str, model: str, token_limit: int) -> Tuple[bool, str]:
        """测试单个LLM模型"""
        try:
            print(f"🧪 测试 {model_name} ({provider}:{model})...")
            
            # 创建测试消息
            test_messages = [
                {"role": "user", "content": "请简单回答：你是什么模型？用一句话回答即可。"}
            ]
            
            # 调用LLM
            response = await create_chat_completion(
                model=model,
                messages=test_messages,
                temperature=0.1,
                llm_provider=provider,
                stream=False,  # 不使用流式输出以便获取完整响应
                max_tokens=100,  # 限制token数量
                llm_kwargs=self.config.llm_kwargs
            )
            
            if response and len(response.strip()) > 0:
                print(f"  ✅ {model_name} 测试成功")
                print(f"  📝 响应: {response[:100]}{'...' if len(response) > 100 else ''}")
                return True, response[:200]
            else:
                print(f"  ❌ {model_name} 返回空响应")
                return False, "空响应"
                
        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ {model_name} 测试失败: {error_msg}")
            return False, error_msg

    async def test_embedding_model(self) -> Tuple[bool, str]:
        """测试Embedding模型"""
        try:
            print(f"🧪 测试 Embedding ({self.config.embedding_provider}:{self.config.embedding_model})...")
            
            # 创建Memory实例
            memory = Memory(
                embedding_provider=self.config.embedding_provider,
                model=self.config.embedding_model
            )
            
            # 获取embeddings对象
            embeddings = memory.get_embeddings()
            
            # 测试文本
            test_text = "这是一个测试句子，用于验证embedding功能是否正常工作。"
            
            # 生成embedding
            embedding_vector = embeddings.embed_query(test_text)
            
            if embedding_vector and len(embedding_vector) > 0:
                print(f"  ✅ Embedding 测试成功")
                print(f"  📊 向量维度: {len(embedding_vector)}")
                print(f"  🔢 前5个值: {embedding_vector[:5]}")
                return True, f"向量维度: {len(embedding_vector)}"
            else:
                print(f"  ❌ Embedding 返回空向量")
                return False, "空向量"
                
        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ Embedding 测试失败: {error_msg}")
            return False, error_msg

    async def test_all_models(self):
        """测试所有模型"""
        print("🚀 开始测试所有模型...")
        print()
        
        # 测试LLM模型
        llm_tests = [
            ("Fast LLM", self.config.fast_llm_provider, self.config.fast_llm_model, self.config.fast_token_limit),
            ("Smart LLM", self.config.smart_llm_provider, self.config.smart_llm_model, self.config.smart_token_limit),
            ("Strategic LLM", self.config.strategic_llm_provider, self.config.strategic_llm_model, self.config.strategic_token_limit),
        ]
        
        for model_name, provider, model, token_limit in llm_tests:
            success, result = await self.test_llm_model(model_name, provider, model, token_limit)
            self.results[model_name] = {
                "success": success,
                "result": result,
                "config": f"{provider}:{model}"
            }
            print()  # 空行分隔
        
        # 测试Embedding模型
        success, result = await self.test_embedding_model()
        self.results["Embedding"] = {
            "success": success,
            "result": result,
            "config": f"{self.config.embedding_provider}:{self.config.embedding_model}"
        }
        print()

    def print_summary(self):
        """打印测试结果摘要"""
        print("=" * 60)
        print("📋 测试结果摘要")
        print("=" * 60)
        
        success_count = 0
        total_count = len(self.results)
        
        for model_name, result in self.results.items():
            status = "✅ 成功" if result["success"] else "❌ 失败"
            print(f"{model_name:15} | {status:8} | {result['config']}")
            if result["success"]:
                success_count += 1
            else:
                print(f"                  错误: {result['result']}")
        
        print("-" * 60)
        print(f"总计: {success_count}/{total_count} 个模型可用")
        
        if success_count == total_count:
            print("🎉 所有模型都可以正常使用！")
        elif success_count > 0:
            print("⚠️  部分模型可用，请检查失败的模型配置")
        else:
            print("🚨 所有模型都无法使用，请检查API配置")
        
        print("=" * 60)

async def main():
    """主函数"""
    print("🔍 GPT-Researcher 逆向API模型测试工具")
    print()
    
    try:
        # 创建测试器
        tester = ModelTester()
        
        # 打印配置信息
        tester.print_config_info()
        
        # 测试所有模型
        await tester.test_all_models()
        
        # 打印摘要
        tester.print_summary()
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
