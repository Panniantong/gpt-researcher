#!/usr/bin/env python3
"""
测试修复后的Deep Research功能
"""
import asyncio
from gpt_researcher import GPTResearcher
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

async def test_deep_research():
    print("=== 测试 Deep Research with Fixed Embeddings ===")
    print(f"EMBEDDING 配置: {os.getenv('EMBEDDING')}")
    print(f"使用官方 OpenAI API 进行嵌入")
    print()
    
    query = "What are the key features and applications of GPT-4?"
    researcher = GPTResearcher(
        query=query,
        report_type="deep_research", 
        source_urls=[],
        verbose=True
    )
    
    print(f"研究查询: {query}")
    print(f"报告类型: Deep Research")
    print(f"Embedding Provider: {researcher.cfg.embedding_provider}")
    print(f"Embedding Model: {researcher.cfg.embedding_model}")
    print()
    
    try:
        # 进行深度研究
        print("开始深度研究...")
        report = await researcher.conduct_research()
        
        print("\n=== 研究报告 ===")
        print(report[:1000])  # 只打印前1000个字符
        print(f"\n... (总长度: {len(report)} 字符)")
        
        # 获取研究成本
        costs = researcher.get_costs()
        print(f"\n=== 成本分析 ===")
        print(f"总成本: ${costs:.4f}")
        
        print("\n✅ Deep Research 测试成功！")
        
    except Exception as e:
        print(f"\n❌ Deep Research 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_deep_research())