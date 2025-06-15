#!/usr/bin/env python3
"""
竞品分析 Summary 模式测试 - chat4data
Test Competitive Intelligence Summary Mode for chat4data

This test demonstrates how to use the competitive intelligence feature
to analyze chat4data product using summary mode.
"""

import asyncio
import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType
from backend.report_type.competitive_intelligence.competitive_intelligence import CompetitiveIntelligenceReport


async def test_gpt_researcher_summary():
    """使用 GPTResearcher 类测试 Summary 模式"""
    print("🔍 测试 GPTResearcher - Summary 模式")
    print("=" * 60)
    print("目标产品: chat4data")
    print("分析模式: Summary (快速概览)")
    print()
    
    # 创建研究员实例
    researcher = GPTResearcher(
        query="chat4data",
        report_type=ReportType.CompetitiveIntelligence.value,
        report_source="web"
    )
    
    print(f"✅ 已创建竞品调研员")
    print(f"   - 目标产品: {researcher.query}")
    print(f"   - 报告类型: {researcher.report_type}")
    print(f"   - 数据来源: {researcher.report_source}")
    print()
    
    # 执行研究（注意：这会调用API并产生费用）
    print("🔄 开始执行竞品分析...")
    print("⚠️  注意：执行以下代码会调用LLM API，会产生费用")
    
    # 取消下面的注释来实际执行研究
    await researcher.conduct_research()
    report = await researcher.write_report()
    
#     # 模拟报告内容用于演示
#     mock_report = """
# # chat4data 竞品分析报告

# ## Part 1: 核心档案 (Executive Profile)

# ### 【创始人画像】
# [需深度调研] 创始人背景信息...

# ### 【产品定位】
# chat4data 是一个数据分析对话平台...

# ## Part 2: 创始人深度分析
# [创始人相关深度分析内容...]

# ## Part 3: 产品与市场分析
# [产品功能、市场定位等分析...]
# """
    
    # 保存报告（实际使用时替换为真实报告）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"tests/chat4data_summary_report_{timestamp}.md"
    
    # 实际使用时的代码
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"✅ 报告已保存至: {report_path}")
    
    # print("📝 报告示例预览:")
    # print("-" * 40)
    # print(mock_report[:300] + "...")
    # print("-" * 40)
    
    return researcher


async def test_backend_class_summary():
    """直接使用后端报告类测试 Summary 模式"""
    print("\n🔧 测试后端报告类 - Summary 模式")
    print("=" * 60)
    print("目标产品: chat4data")
    print("使用类: CompetitiveIntelligenceReport")
    print()
    
    # 创建报告实例
    report = CompetitiveIntelligenceReport(
        query="chat4data",
        report_type="competitive_intelligence",
        report_source="web"
    )
    
    print(f"✅ 已创建报告实例")
    print(f"   - 类名: {report.__class__.__name__}")
    print(f"   - 查询: {report.query}")
    print(f"   - 类型: {report.report_type}")
    print()
    
    # 获取报告数据的方法
    print("📋 可用方法:")
    print("   • report.run() - 执行完整的研究流程")
    print("   • 内部会创建 GPTResearcher 实例并执行研究")
    print()
    
    # 实际执行（注意费用）
    print("⚠️  执行以下代码会产生API费用:")
    print("   result = await report.run()")
    print("   # result 包含完整的报告内容")
    
    return report


async def test_with_specific_sources():
    """测试指定特定信息源的情况"""
    print("\n🎯 测试指定信息源 - Summary 模式")
    print("=" * 60)
    print("目标产品: chat4data")
    print("指定来源: LinkedIn, Product Hunt, Reddit")
    print()
    
    # 创建带有特定域名限制的研究员
    researcher = GPTResearcher(
        query="chat4data",
        report_type=ReportType.CompetitiveIntelligence.value,
        report_source="web"
    )
    
    # 竞品分析模式会自动优化搜索这些平台
    print("✅ 竞品分析模式特性:")
    print("   • 自动优化搜索关键平台（LinkedIn, Reddit, Product Hunt）")
    print("   • 使用双搜索引擎（Tavily + Google）提高覆盖率")
    print("   • 强制信息溯源，标注引用来源")
    print()
    
    return researcher


async def main():
    """主测试函数"""
    print("🚀 chat4data 竞品分析测试")
    print("=" * 80)
    print("📌 测试说明:")
    print("   本测试展示如何使用竞品分析功能的 Summary 模式")
    print("   分析目标产品: chat4data")
    print("   适用场景: 快速了解产品概况、创始人背景、市场定位等")
    print()
    
    # 运行各项测试
    tests = [
        ("GPTResearcher 类测试", test_gpt_researcher_summary),
        ("后端报告类测试", test_backend_class_summary),
        ("指定信息源测试", test_with_specific_sources)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        await test_func()
    
    # 使用建议
    print("\n📚 使用建议")
    print("=" * 60)
    print("1. Summary 模式特点:")
    print("   • 2000字左右的精炼报告")
    print("   • 快速获取产品核心信息")
    print("   • 适合初步调研和快速决策")
    print()
    print("2. 报告结构包含:")
    print("   • Part 1: 核心档案 (创始人、产品定位、融资等)")
    print("   • Part 2: 创始人深度分析")
    print("   • Part 3: 产品与市场分析 (八维分析、营销情报等)")
    print()
    print("3. 实际使用步骤:")
    print("   ① 取消代码中的注释来执行真实研究")
    print("   ② 等待研究完成（约2-3分钟）")
    print("   ③ 查看生成的报告文件")
    print()
    print("⚠️  重要提醒: 执行实际研究会调用 LLM API 并产生费用!")
    print("💡 建议先在测试环境验证配置，确认无误后再执行生产环境调用")


if __name__ == "__main__":
    print("开始运行 chat4data 竞品分析测试...")
    print()
    asyncio.run(main())