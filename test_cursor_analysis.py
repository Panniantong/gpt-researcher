"""
测试 Cursor 竞品调研
"""
import asyncio
import os
from dotenv import load_dotenv
import sys

# 添加父目录到路径以便导入 gpt_researcher
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from competitive_intelligence import CompetitiveIntelligenceAgent


async def test_cursor_analysis():
    """测试分析 Cursor"""
    print("=== 测试分析 Cursor ===\n")
    
    # 创建竞品调研Agent
    agent = CompetitiveIntelligenceAgent(
        query="Cursor",  # 分析 Cursor
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    # 运行调研
    print("开始调研...")
    report = await agent.run_research()
    
    # 打印报告
    print("\n" + "="*80 + "\n")
    print(report)
    print("\n" + "="*80 + "\n")
    
    # 保存结果
    await agent.save_results("cursor_test_analysis.json")
    
    # 打印调试信息
    print("\n调试信息：")
    print(f"产品URL: {agent.product_url}")
    print(f"基础信息: {agent.results['basic_info']}")
    print(f"信息来源: {agent.results['sources']}")
    
    return report


if __name__ == "__main__":
    load_dotenv()
    
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY"):
        print("错误：缺少 OPENAI_API_KEY 环境变量")
        exit(1)
    
    if not os.getenv("TAVILY_API_KEY"):
        print("警告：缺少 TAVILY_API_KEY 环境变量，搜索功能可能受限")
    
    # 运行测试
    asyncio.run(test_cursor_analysis())