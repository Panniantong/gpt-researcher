#!/usr/bin/env python3
"""
测试修复后的embedding配置
"""
import os
import asyncio
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置日志级别
import logging
logging.basicConfig(level=logging.DEBUG)

async def test_embeddings():
    """测试embedding功能"""
    print("=== 测试 Embedding 配置 ===")
    print(f"EMBEDDING: {os.getenv('EMBEDDING')}")
    print(f"OPENAI_EMBEDDING_API_KEY: {os.getenv('OPENAI_EMBEDDING_API_KEY', 'Not set')[:20]}...")
    print(f"OPENAI_EMBEDDING_BASE_URL: {os.getenv('OPENAI_EMBEDDING_BASE_URL')}")
    print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'Not set')[:20]}...")
    print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL')}")
    print()
    
    # 测试Memory初始化
    from gpt_researcher.memory import Memory
    
    try:
        print("初始化 Memory...")
        memory = Memory(
            embedding_provider="openai",
            model="text-embedding-3-small"
        )
        embeddings = memory.get_embeddings()
        print(f"✓ Memory 初始化成功")
        print(f"Embeddings 类型: {type(embeddings)}")
        
        # 测试实际的embedding功能
        print("\n测试 embed_query...")
        test_query = "What is artificial intelligence?"
        result = embeddings.embed_query(test_query)
        print(f"✓ Embedding 成功")
        print(f"Embedding 维度: {len(result)}")
        print(f"前5个值: {result[:5]}")
        
        # 测试 embed_documents
        print("\n测试 embed_documents...")
        test_docs = [
            "AI is transforming the world",
            "Machine learning is a subset of AI"
        ]
        results = embeddings.embed_documents(test_docs)
        print(f"✓ Documents embedding 成功")
        print(f"返回了 {len(results)} 个embeddings")
        for i, emb in enumerate(results):
            print(f"  文档 {i+1} embedding 维度: {len(emb)}")
        
        # 测试 GPTResearcher 初始化
        print("\n测试 GPTResearcher 初始化...")
        from gpt_researcher import GPTResearcher
        
        researcher = GPTResearcher(
            query="What is AI?",
            report_type="research_report"
        )
        print(f"✓ GPTResearcher 初始化成功")
        print(f"Embedding provider: {researcher.cfg.embedding_provider}")
        print(f"Embedding model: {researcher.cfg.embedding_model}")
        
        # 测试 context compression
        print("\n测试 Context Compression...")
        from gpt_researcher.context.compression import ContextCompressor
        
        test_documents = [
            {"title": "AI Overview", "body": "Artificial Intelligence is...", "href": "http://example.com/1"},
            {"title": "ML Basics", "body": "Machine Learning fundamentals...", "href": "http://example.com/2"}
        ]
        
        compressor = ContextCompressor(
            documents=test_documents,
            embeddings=researcher.memory.get_embeddings(),
            max_results=5
        )
        
        context = await compressor.async_get_context("What is AI?", max_results=2)
        print(f"✓ Context compression 成功")
        print(f"返回的context长度: {len(context)} 字符")
        
        print("\n✅ 所有测试通过！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_embeddings())