"""
Demo: Deep Competitive Intelligence Research
演示：深度竞品情报研究
"""

import asyncio
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config


async def demo_deep_research():
    """演示深度竞品研究"""
    load_dotenv()
    
    product_name = "Windsurf"  # Cursor 的竞品
    product_url = "https://codeium.com/windsurf"
    
    print(f"🎯 深度竞品情报研究演示: {product_name}")
    print("=" * 60)
    
    # 创建配置
    config = Config()
    config.deep_research_breadth = 2  # 降低广度以加快演示
    config.deep_research_depth = 1    # 降低深度以加快演示
    
    # 创建代理
    agent = CompetitiveIntelligenceAgent(
        product_name=product_name,
        product_url=product_url,
        config=config
    )
    
    print("\n1️⃣ 测试单个方面的深度研究...")
    print("-" * 40)
    
    # 测试创始人研究
    founder_results = await agent.deep_research_skill.research_aspect(
        aspect="founder team background experience",
        breadth=2,
        depth=1
    )
    
    print(f"✅ 创始人研究完成:")
    print(f"   - 学习要点: {len(founder_results.get('learnings', []))} 个")
    print(f"   - 引用来源: {len(founder_results.get('citations', {}))} 个")
    print(f"   - 访问URL: {len(founder_results.get('visited_urls', []))} 个")
    
    # 显示前2个学习要点
    learnings = founder_results.get('learnings', [])[:2]
    citations = founder_results.get('citations', {})
    
    print("\n   关键发现:")
    for i, learning in enumerate(learnings, 1):
        citation = citations.get(learning, '无来源')
        print(f"   {i}. {learning[:100]}...")
        print(f"      来源: {citation}")
    
    print("\n2️⃣ 测试并行多维度研究...")
    print("-" * 40)
    
    # 定义要研究的维度
    dimensions = {
        "product": "product features capabilities",
        "market": "market position competitors",
        "technology": "technology stack architecture"
    }
    
    # 并行研究多个维度
    multi_results = await agent.deep_research_skill.parallel_research_aspects(
        aspects=dimensions,
        breadth=2,
        depth=1
    )
    
    print(f"✅ 多维度研究完成:")
    print(f"   - 总学习要点: {len(multi_results.get('learnings', []))} 个")
    print(f"   - 总引用来源: {len(multi_results.get('citations', {}))} 个")
    
    # 显示每个维度的结果
    by_aspect = multi_results.get('by_aspect', {})
    for aspect_name, aspect_data in by_aspect.items():
        learnings_count = len(aspect_data.get('learnings', []))
        print(f"   - {aspect_name}: {learnings_count} 个发现")
    
    print("\n3️⃣ 对比：普通搜索 vs 深度研究")
    print("-" * 40)
    
    # 普通搜索（使用 _parallel_search）
    normal_queries = [f"{product_name} features", f"{product_name} team"]
    normal_results = await agent._parallel_search(normal_queries)
    
    print(f"普通搜索:")
    print(f"   - 结果数量: {len(normal_results)}")
    print(f"   - 结构化程度: 低（原始搜索结果）")
    
    print(f"\n深度研究:")
    print(f"   - 学习要点: {len(multi_results.get('learnings', []))} 个")
    print(f"   - 带引用来源: 是")
    print(f"   - 迭代深化: 是")
    print(f"   - 结构化程度: 高（提炼的知识点）")
    
    print("\n✨ 深度研究优势:")
    print("   1. 自动生成后续查询，深入挖掘信息")
    print("   2. 提取关键学习要点，而非原始内容")
    print("   3. 每个发现都有明确的来源引用")
    print("   4. 并行处理多个研究方向，效率更高")
    
    print("\n" + "=" * 60)
    print("🎉 深度竞品情报研究功能演示完成！")


if __name__ == "__main__":
    asyncio.run(demo_deep_research())