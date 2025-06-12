"""
简单的竞品情报研究示例
"""

import asyncio
import os
from dotenv import load_dotenv

# 添加项目根目录到Python路径
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config


async def main():
    # 加载环境变量
    load_dotenv()
    
    # 设置要研究的产品
    product_name = "Cursor"  # 你可以改成任何产品
    product_url = "https://cursor.sh"
    
    print(f"🔍 开始研究 {product_name}...")
    print("=" * 50)
    
    try:
        # 创建配置
        config = Config()
        
        # 创建竞品情报代理
        agent = CompetitiveIntelligenceAgent(
            product_name=product_name,
            product_url=product_url,
            config=config
        )
        
        # 注意：实际执行研究需要调用 GPT API，会产生费用
        # 这里只展示如何使用，不实际执行
        
        print("\n✅ 成功创建竞品情报代理！")
        print(f"\n产品名称: {agent.product_name}")
        print(f"产品URL: {agent.product_url}")
        
        print("\n📋 将要研究的模块：")
        queries = agent.query_builder.build_all_queries()
        for i, (module, template) in enumerate(queries.items(), 1):
            print(f"{i}. {template.module} ({len(template.queries)} 个查询)")
        
        print("\n💡 提示：")
        print("- 执行完整研究会调用 LLM API，请确保已设置 API key")
        print("- 完整研究通常需要 3-5 分钟")
        print("- 会产生一定的 API 费用")
        
        # 如果要实际执行研究，取消下面的注释：
        # result = await agent.conduct_research()
        # print("\n📄 研究报告：")
        # print(result["report"])
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())