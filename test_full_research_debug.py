"""
调试完整的调研流程
"""
import asyncio
import os
from dotenv import load_dotenv
import sys
import json

# 添加父目录到路径以便导入 gpt_researcher
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from competitive_intelligence import CompetitiveIntelligenceAgent


async def test_research_with_debug():
    """测试调研流程并打印调试信息"""
    print("=== 测试 Cursor 完整调研流程 ===\n")
    
    # 创建竞品调研Agent
    agent = CompetitiveIntelligenceAgent(
        query="Cursor",
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    # 仅运行前几个步骤
    try:
        # 1. 获取基础信息
        print("步骤 1: 获取基础信息...")
        await agent._extract_basic_info()
        print(f"基础信息: {json.dumps(agent.results['basic_info'], indent=2, ensure_ascii=False)}")
        print(f"产品URL: {agent.product_url}")
        print()
        
        # 2. 创始人背景调研
        print("步骤 2: 调研创始人/团队背景...")
        await agent._research_founder_background()
        print(f"搜索的URL数量: {len(agent.results['sources'])}")
        print(f"前5个URL:")
        for url in agent.results['sources'][:5]:
            print(f"  - {url}")
        print()
        
        # 3. 检查创始人分析的搜索查询
        product_name = agent.results["basic_info"].get("name", agent.query)
        queries = await agent.founder_analyzer.generate_search_queries(
            product_name,
            agent.product_url
        )
        print(f"创始人分析的搜索查询:")
        for q in queries[:5]:
            print(f"  - {q}")
        print()
        
        # 4. 八维分析
        print("步骤 3: 进行八维分析...")
        await agent._analyze_eight_dimensions()
        print(f"总URL数量: {len(agent.results['sources'])}")
        print(f"最后添加的5个URL:")
        for url in agent.results['sources'][-5:]:
            print(f"  - {url}")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    
    # 保存结果以供分析
    await agent.save_results("cursor_debug_analysis.json")
    print(f"\n结果已保存到: cursor_debug_analysis.json")


if __name__ == "__main__":
    load_dotenv()
    
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY"):
        print("错误：缺少 OPENAI_API_KEY 环境变量")
        exit(1)
    
    if not os.getenv("TAVILY_API_KEY"):
        print("警告：缺少 TAVILY_API_KEY 环境变量，搜索功能可能受限")
    
    # 运行测试
    asyncio.run(test_research_with_debug())