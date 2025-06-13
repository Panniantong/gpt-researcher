#!/usr/bin/env python3
"""
调试Deep Research中的embedding问题
"""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_embedding_in_context():
    """测试在上下文压缩中的embedding问题"""
    print("🔍 测试Deep Research中的embedding问题...")
    
    # 加载环境变量
    load_dotenv()
    
    try:
        from gpt_researcher.memory.embeddings import Memory
        from gpt_researcher.context.compression import ContextCompressor
        from gpt_researcher.config.config import Config
        
        # 创建配置
        cfg = Config()
        print(f"✅ 配置加载成功")
        print(f"   Embedding Provider: {cfg.embedding_provider}")
        print(f"   Embedding Model: {cfg.embedding_model}")
        
        # 创建Memory实例
        memory = Memory(cfg.embedding_provider, cfg.embedding_model, **cfg.embedding_kwargs)
        print(f"✅ Memory实例创建成功")
        
        # 获取embeddings
        embeddings = memory.get_embeddings()
        print(f"✅ Embeddings获取成功: {type(embeddings)}")
        
        # 测试简单的embedding
        test_text = "This is a test document for embedding."
        try:
            result = embeddings.embed_query(test_text)
            print(f"✅ 单个查询embedding成功:")
            print(f"   类型: {type(result)}")
            print(f"   长度: {len(result) if hasattr(result, '__len__') else 'N/A'}")
            if isinstance(result, list) and len(result) > 0:
                print(f"   前5个值: {result[:5]}")
        except Exception as e:
            print(f"❌ 单个查询embedding失败: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # 模拟搜索结果数据
        mock_documents = [
            {
                "title": "Test Document 1",
                "body": "This is the first test document with some content about artificial intelligence and machine learning.",
                "href": "https://example.com/doc1"
            },
            {
                "title": "Test Document 2", 
                "body": "This is the second test document discussing natural language processing and deep learning techniques.",
                "href": "https://example.com/doc2"
            },
            {
                "title": "Test Document 3",
                "body": "The third document covers computer vision and neural networks in detail.",
                "href": "https://example.com/doc3"
            }
        ]
        
        print(f"\n📚 测试上下文压缩，文档数量: {len(mock_documents)}")
        
        # 创建ContextCompressor
        try:
            context_compressor = ContextCompressor(
                documents=mock_documents,
                embeddings=embeddings,
                prompt_family=None  # 简化测试
            )
            print(f"✅ ContextCompressor创建成功")
        except Exception as e:
            print(f"❌ ContextCompressor创建失败: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # 测试上下文获取
        test_query = "artificial intelligence and machine learning"
        try:
            print(f"\n🔍 测试查询: '{test_query}'")
            context = await context_compressor.async_get_context(test_query, max_results=3)
            
            print(f"✅ 上下文获取成功:")
            print(f"   类型: {type(context)}")
            print(f"   长度: {len(context) if hasattr(context, '__len__') else 'N/A'}")
            
            if context:
                if isinstance(context, str):
                    print(f"   内容预览: {context[:200]}...")
                elif isinstance(context, list):
                    print(f"   列表长度: {len(context)}")
                    for i, item in enumerate(context[:2]):
                        print(f"   项目 {i+1}: {str(item)[:100]}...")
            else:
                print("   ⚠️ 返回的上下文为空")
                
        except Exception as e:
            print(f"❌ 上下文获取失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 检查是否是embedding相关的错误
            error_str = str(e).lower()
            if 'embedding' in error_str or 'none' in error_str:
                print("\n🔧 这看起来是embedding相关的错误")
                print("   可能的原因:")
                print("   1. API密钥或base_url配置问题")
                print("   2. 逆向API不支持embedding接口")
                print("   3. API响应格式不匹配")
                
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()

async def test_simple_deep_research():
    """测试简化的Deep Research流程"""
    print("\n🚀 测试简化的Deep Research流程...")
    
    try:
        from gpt_researcher.agent import GPTResearcher
        
        # 创建研究员实例
        researcher = GPTResearcher(
            query="What is artificial intelligence?",
            report_type="research_report",
            verbose=True
        )
        
        print(f"✅ GPTResearcher实例创建成功")
        print(f"   查询: {researcher.query}")
        print(f"   报告类型: {researcher.report_type}")
        
        # 测试Deep Research
        from gpt_researcher.skills.deep_research import DeepResearchSkill
        
        deep_research = DeepResearchSkill(researcher)
        print(f"✅ DeepResearchSkill实例创建成功")
        
        # 只测试研究计划生成，不执行完整研究
        try:
            research_plan = await deep_research.generate_research_plan(researcher.query, num_questions=2)
            print(f"✅ 研究计划生成成功:")
            for i, question in enumerate(research_plan, 1):
                print(f"   {i}. {question}")
        except Exception as e:
            print(f"❌ 研究计划生成失败: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Deep Research测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 开始调试Deep Research中的embedding问题...")
    
    # 运行测试
    asyncio.run(test_embedding_in_context())
    asyncio.run(test_simple_deep_research())
    
    print("\n✅ 调试完成")
