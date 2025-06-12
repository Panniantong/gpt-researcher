"""
测试完整的 Gadget 产品研究流程
"""

import asyncio
import os
from dotenv import load_dotenv

from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config


async def test_full_gadget_research():
    """测试完整的 Gadget 产品研究流程"""
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
        
        print("\n🔍 开始完整研究...")
        result = await agent.conduct_research()
        
        print("\n📄 研究报告生成完成！")
        print(f"- 收集的源数量: {len(result['sources'])}")
        print(f"- 验证结果: {result['validation']}")
        
        # 保存报告
        with open("gadget_research_output.md", "w", encoding="utf-8") as f:
            f.write(result["report"])
        print("\n📝 报告已保存到 gadget_research_output.md")
        
        # 显示部分报告内容
        print("\n📊 报告预览：")
        print("=" * 60)
        lines = result["report"].split("\n")[:50]  # 显示前50行
        print("\n".join(lines))
        print("\n... (更多内容请查看完整报告)")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_full_gadget_research())