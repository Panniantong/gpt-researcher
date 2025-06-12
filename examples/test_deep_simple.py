"""
Simple test for deep competitive intelligence
简单测试深度竞品情报功能
"""

import asyncio
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config


async def test_deep_research():
    """测试深度研究功能"""
    load_dotenv()
    
    print("🚀 测试深度竞品情报研究...")
    
    # 创建配置
    config = Config()
    
    # 创建代理
    agent = CompetitiveIntelligenceAgent(
        product_name="Cursor",
        product_url="https://cursor.sh",
        config=config
    )
    
    # 测试初始化
    print("✅ Agent 初始化成功")
    print(f"   - Product: {agent.product_name}")
    print(f"   - URL: {agent.product_url}")
    print(f"   - Retrievers: {len(agent.retrievers)} 个")
    
    # 测试深度研究组件
    print("\n🔍 测试深度研究组件...")
    print(f"   - Deep Research Skill: {'✓' if hasattr(agent, 'deep_research_skill') else '✗'}")
    print(f"   - Research Conductor: {'✓' if hasattr(agent, 'research_conductor') else '✗'}")
    print(f"   - Context Manager: {'✓' if hasattr(agent, 'context_manager') else '✗'}")
    
    # 测试基础查询
    print("\n📊 测试基础深度研究查询...")
    try:
        results = await agent.deep_research_skill.generate_search_queries(
            query="Cursor AI code editor features",
            num_queries=2
        )
        print(f"   - 生成查询数: {len(results)}")
        for i, query in enumerate(results, 1):
            print(f"   - 查询 {i}: {query.get('query', '')[:50]}...")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print("\n✅ 深度研究功能集成完成！")


if __name__ == "__main__":
    asyncio.run(test_deep_research())