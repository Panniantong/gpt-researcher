"""
测试部分研究功能 - 只执行基础信息收集
"""

import asyncio
import os
from dotenv import load_dotenv

from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config


async def test_partial_research():
    """测试部分研究功能"""
    # 加载环境变量
    load_dotenv()
    
    # 设置产品信息
    product_name = "gadget"
    product_url = "https://gadget.dev"
    
    print(f"🔍 测试 {product_name} 的基础信息收集...")
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
        
        print("✅ 成功创建代理\n")
        
        # 只测试基础信息收集
        print("📊 开始收集基础信息...")
        await agent._research_basic_info()
        
        print("\n📝 收集到的基础信息：")
        print(f"- 产品名称: {agent.product_info.name}")
        print(f"- 产品URL: {agent.product_info.url}")
        print(f"- 团队规模: {agent.product_info.team_size}")
        print(f"- 一句话介绍: {agent.product_info.one_liner}")
        print(f"- 产品类型: {agent.product_info.type}")
        print(f"- 发布状态: {agent.product_info.launch_status}")
        print(f"- 成立时间: {agent.product_info.founded}")
        
        if agent.product_info.search_traces:
            print(f"\n🔍 搜索轨迹 ({len(agent.product_info.search_traces)} 个查询):")
            for i, trace in enumerate(agent.product_info.search_traces[:3], 1):
                print(f"   {i}. {trace}")
        
        # 生成部分报告
        print("\n📄 生成部分报告...")
        partial_data = {
            "product_info": agent._dataclass_to_dict(agent.product_info),
            "founder_info": {},
            "eight_dimensions": {},
            "growth_intelligence": {},
            "feasibility": {},
            "executive_summary": {}
        }
        
        partial_report = agent.report_generator.generate_report(partial_data)
        
        print("\n--- 报告预览 ---")
        # 只显示基础信息部分
        lines = partial_report.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("### 【基础信息"):
                # 打印基础信息部分
                j = i
                while j < len(lines) and not (lines[j].startswith("### 【") and j > i):
                    print(lines[j])
                    j += 1
                break
        
        print("\n✅ 测试完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_partial_research())