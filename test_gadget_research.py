"""
测试 Gadget 产品研究
"""

import asyncio
import os
from dotenv import load_dotenv

from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config


async def test_gadget_research():
    """测试 Gadget 产品研究"""
    # 加载环境变量
    load_dotenv()
    
    # 设置产品信息
    product_name = "gadget"
    product_url = "https://gadget.dev"
    
    print(f"🔍 开始对 {product_name} 进行深度竞品情报研究...")
    print("=" * 60)
    
    try:
        # 创建配置
        config = Config()
        
        # 创建竞品情报代理
        agent = CompetitiveIntelligenceAgent(
            product_name=product_name,
            product_url=product_url,
            config=config
        )
        
        print("✅ 成功创建代理")
        print(f"- 产品名称: {agent.product_name}")
        print(f"- 产品URL: {agent.product_url}")
        print(f"- 查询: {agent.query}")
        
        # 测试搜索功能
        print("\n📊 测试搜索功能...")
        test_query = f"{product_name} company information"
        
        from gpt_researcher.actions.query_processing import get_search_results
        
        # 确保有 retrievers
        if hasattr(agent, 'retrievers') and agent.retrievers:
            print(f"- 使用 retriever: {agent.retrievers[0].__class__.__name__}")
            
            # 执行单个搜索测试
            search_results = await get_search_results(
                query=test_query,
                retriever=agent.retrievers[0],
                query_domains=None,
                researcher=agent
            )
            
            print(f"- 搜索结果数量: {len(search_results)}")
            if search_results:
                print(f"- 第一个结果: {search_results[0].get('title', 'No title')[:50]}...")
                print(f"\n搜索结果详情（前3个）：")
                for i, result in enumerate(search_results[:3]):
                    print(f"\n结果 {i+1}:")
                    print(f"  - URL: {result.get('href', 'No URL')}")
                    print(f"  - Body: {result.get('body', 'No body')[:200]}...")
                    print(f"  - Keys: {list(result.keys())}")
        else:
            print("❌ 没有找到 retrievers")
        
        print("\n✅ 搜索功能测试完成！")
        
        # 如果要执行完整研究，取消下面的注释
        # print("\n🔍 开始完整研究...")
        # result = await agent.conduct_research()
        # print("\n📄 研究报告：")
        # print(result["report"])
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_gadget_research())