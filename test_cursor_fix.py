#!/usr/bin/env python
"""测试修复后的竞品调研功能"""
import asyncio
import json
from competitive_intelligence import CompetitiveIntelligenceAgent

async def test_cursor_analysis():
    """测试Cursor的竞品调研"""
    print("🔍 开始测试Cursor竞品调研...")
    print("=" * 50)
    
    # 创建调研agent
    agent = CompetitiveIntelligenceAgent(
        query="Cursor",
        report_type="competitive_analysis"
    )
    
    # 运行调研
    report_text = await agent.run_research()
    
    # 获取结果数据
    report = agent.results
    
    # 保存结果
    with open("cursor_test_result.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印基础信息部分以验证修复
    print("\n📊 基础信息部分：")
    print("-" * 50)
    basic_info = report.get("basic_info", {})
    print(f"产品名称: {basic_info.get('name', 'N/A')}")
    print(f"一句话描述: {basic_info.get('one_liner', 'N/A')}")
    print(f"产品类型: {basic_info.get('type', 'N/A')}")
    print(f"官方网址: {basic_info.get('url', 'N/A')}")
    print(f"团队规模: {basic_info.get('team_size', 'N/A')}")
    
    # 检查创始人分析是否正常
    print("\n👤 创始人分析部分：")
    print("-" * 50)
    founder = report.get("founder_analysis", {})
    if "sources" in founder:
        print(f"找到 {len(founder['sources'])} 个信息源")
        # 显示前3个源
        for i, source in enumerate(founder['sources'][:3]):
            print(f"  {i+1}. {source}")
    
    print("\n✅ 测试完成！")
    print(f"完整报告已保存到: cursor_test_result.json")

if __name__ == "__main__":
    asyncio.run(test_cursor_analysis())