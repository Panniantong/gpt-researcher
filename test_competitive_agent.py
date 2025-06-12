"""
Test script for CompetitiveIntelligenceAgent
测试竞品情报代理的脚本
"""

import asyncio
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config


async def test_gadget_research():
    """测试对Gadget产品的研究"""
    # 加载环境变量
    load_dotenv()
    
    # 配置
    product_name = "gadget"
    product_url = "https://gadget.dev"
    
    # 创建配置
    config = Config()
    
    print(f"🔍 开始对 {product_name} 进行深度竞品情报研究...\n")
    print("=" * 60)
    
    try:
        # 创建竞品情报代理
        agent = CompetitiveIntelligenceAgent(
            product_name=product_name,
            product_url=product_url,
            config=config
        )
        
        # 执行研究
        result = await agent.conduct_research()
        
        # 输出结果
        print("\n📊 研究完成！\n")
        print("=" * 60)
        
        # 显示验证结果
        print("\n✅ 核对表验证结果:")
        for check, passed in result["validation"].items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check}")
        
        # 显示报告
        print("\n📄 完整报告:")
        print("=" * 60)
        print(result["report"])
        
        # 显示收集的来源数量
        print(f"\n📌 共收集 {len(result['sources'])} 个信息来源")
        
        # 保存报告到文件
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{output_dir}/{product_name.lower()}_competitive_intelligence_test_{result['timestamp'][:10]}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result["report"])
        
        print(f"\n💾 报告已保存至: {filename}")
        
    except Exception as e:
        print(f"\n❌ 研究过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_gadget_research())