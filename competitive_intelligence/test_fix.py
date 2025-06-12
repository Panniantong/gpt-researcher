#!/usr/bin/env python3
"""测试修复的脚本"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from competitive_intelligence import CompetitiveIntelligenceAgent


async def test_analyze():
    """测试产品分析功能"""
    print("🔍 正在测试产品分析功能...")
    
    # 创建agent
    agent = CompetitiveIntelligenceAgent(
        query="Cursor",
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    try:
        # 运行研究
        report = await agent.run_research()
        
        # 保存结果
        await agent.save_results("test_cursor_analysis.json")
        
        print("✅ 分析完成并成功保存到 test_cursor_analysis.json")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_analyze())