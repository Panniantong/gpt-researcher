"""
简单的测试脚本，测试竞品调研Agent的基本功能
"""
import asyncio
import os
from dotenv import load_dotenv

# 添加父目录到路径
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from competitive_intelligence import CompetitiveIntelligenceAgent


async def test_basic_functionality():
    """测试基本功能"""
    print("=== 测试竞品调研 Agent ===\n")
    
    # 创建Agent - 使用一个知名产品测试
    agent = CompetitiveIntelligenceAgent(
        query="ChatGPT",
        product_url="https://chat.openai.com",
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    print("1. 测试基础信息提取...")
    try:
        await agent._extract_basic_info()
        print(f"✅ 产品名称: {agent.results['basic_info'].get('name', 'N/A')}")
        print(f"✅ 产品描述: {agent.results['basic_info'].get('one_liner', 'N/A')}")
        print(f"✅ 团队规模: {agent.results['basic_info'].get('team_size', 'N/A')}")
    except Exception as e:
        print(f"❌ 基础信息提取失败: {e}")
    
    print("\n2. 完整调研流程测试...")
    print("（这可能需要几分钟时间...）")
    
    # 运行完整调研
    try:
        report = await agent.run_research()
        
        # 保存报告
        with open("chatgpt_test_report.md", "w", encoding="utf-8") as f:
            f.write(report)
        
        print("✅ 调研完成！报告已保存到 chatgpt_test_report.md")
        
        # 打印部分报告
        print("\n=== 报告预览（前1000字符）===")
        print(report[:1000])
        print("\n...")
        
    except Exception as e:
        print(f"❌ 调研失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()
    
    # 检查API密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("错误：请设置 OPENAI_API_KEY 环境变量")
        print("export OPENAI_API_KEY='your-api-key'")
        exit(1)
    
    # 运行测试
    asyncio.run(test_basic_functionality())