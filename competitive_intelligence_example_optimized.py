#!/usr/bin/env python3
"""
优化后的竞品调研使用示例

展示如何使用新的优化功能：
1. 查询优化 - 针对双搜索引擎的智能查询
2. 结果过滤 - 关键平台信息优先
3. 上下文增强 - 平台特定分析指导
4. 双搜索引擎 - Tavily + Google 全面覆盖
"""

import asyncio
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.report_type.competitive_intelligence.competitive_intelligence import (
    CompetitiveIntelligenceReport, 
    CompetitiveIntelligenceDetailedReport
)


async def demo_optimized_summary_research():
    """演示优化后的Summary模式竞品调研"""
    print("🚀 优化后的竞品调研 - Summary模式")
    print("=" * 60)
    print()
    
    # 测试产品
    product_name = "Cursor"
    
    print(f"📋 研究目标: {product_name}")
    print("🔍 搜索引擎: Tavily + Google (自动配置)")
    print("⚡ 模式: Summary (快速概览)")
    print()
    
    try:
        # 创建优化后的竞品调研实例
        ci_report = CompetitiveIntelligenceReport(
            query=product_name,
            report_type="competitive_intelligence",
            report_source="web"
        )
        
        print("✅ 已创建优化后的竞品调研实例")
        print(f"   • 搜索引擎配置: {ci_report.headers.get('retrievers', '默认')}")
        print(f"   • 优先平台数量: {len(ci_report.priority_platforms)}")
        print()
        
        # 展示查询优化效果
        print("📝 查询优化展示:")
        original_query = product_name
        optimized_query = ci_report._enhance_query_for_competitive_research(original_query)
        print(f"   原始查询: {original_query}")
        print(f"   优化查询: {optimized_query[:100]}...")
        print()
        
        print("💡 实际运行时会执行:")
        print("   1. 使用优化查询在Tavily和Google上并行搜索")
        print("   2. 自动过滤和排序结果，优先展示关键平台信息")
        print("   3. 为LLM提供平台特定的分析指导")
        print("   4. 生成结构化的竞品情报报告")
        print()
        
        # 注意：这里不实际运行研究，避免API调用
        # 实际使用时取消注释下面的代码：
        # report = await ci_report.run()
        # print("📄 生成的报告:")
        # print(report)
        
    except Exception as e:
        print(f"❌ 创建实例时出错: {e}")


async def demo_optimized_detailed_research():
    """演示优化后的Detailed模式竞品调研"""
    print("🚀 优化后的竞品调研 - Detailed模式")
    print("=" * 60)
    print()
    
    # 测试产品URL
    product_url = "https://notion.so"
    
    print(f"📋 研究目标: {product_url}")
    print("🔍 搜索引擎: Tavily + Google (自动配置)")
    print("⚡ 模式: Detailed (深度分析)")
    print()
    
    try:
        # 创建优化后的详细竞品调研实例
        detailed_report = CompetitiveIntelligenceDetailedReport(
            query=product_url,
            report_type="competitive_intelligence_detailed",
            report_source="web"
        )
        
        print("✅ 已创建优化后的详细竞品调研实例")
        print(f"   • 搜索引擎配置: {detailed_report.headers.get('retrievers', '默认')}")
        print(f"   • 优先平台数量: {len(detailed_report.priority_platforms)}")
        print()
        
        # 展示详细模式的查询优化
        print("📝 详细模式查询优化展示:")
        original_query = product_url
        optimized_query = detailed_report._enhance_query_for_detailed_research(original_query)
        print(f"   原始查询: {original_query}")
        print(f"   详细优化查询: {optimized_query[:100]}...")
        print()
        
        print("💡 详细模式特色:")
        print("   • 更全面的平台关键词覆盖")
        print("   • 深度分析指导（八维分析、营销情报等）")
        print("   • 更详细的信息验证要求")
        print("   • 结构化的竞品情报框架")
        print()
        
    except Exception as e:
        print(f"❌ 创建实例时出错: {e}")


def show_platform_coverage():
    """展示平台覆盖情况"""
    print("🌐 平台覆盖情况")
    print("=" * 60)
    print()
    
    ci_report = CompetitiveIntelligenceReport(query="TestProduct")
    
    # 按类别展示平台
    platform_categories = {
        "创始人和团队信息": [
            "linkedin.com", "crunchbase.com", "angel.co", "angellist.com"
        ],
        "用户反馈和讨论": [
            "reddit.com", "producthunt.com", "news.ycombinator.com"
        ],
        "技术和开发": [
            "github.com", "stackoverflow.com", "dev.to"
        ],
        "专业评价": [
            "g2.com", "capterra.com", "trustpilot.com", "getapp.com"
        ],
        "媒体和新闻": [
            "techcrunch.com", "venturebeat.com", "theverge.com", "wired.com"
        ],
        "内容和分享": [
            "medium.com", "substack.com", "indiehackers.com"
        ]
    }
    
    for category, platforms in platform_categories.items():
        print(f"📂 {category}:")
        for platform in platforms:
            included = platform in ci_report.priority_platforms
            status = "✓" if included else "✗"
            print(f"   {status} {platform}")
        print()


def show_optimization_benefits():
    """展示优化带来的好处"""
    print("📈 优化效果对比")
    print("=" * 60)
    print()
    
    print("🔍 搜索覆盖对比:")
    print("   优化前: 单一搜索引擎 (Tavily)")
    print("   优化后: 双搜索引擎 (Tavily + Google)")
    print("   提升: 更全面的索引覆盖，减少信息遗漏")
    print()
    
    print("🎯 查询质量对比:")
    print("   优化前: 通用查询")
    print("   优化后: 平台优化查询，包含关键平台关键词")
    print("   提升: 提高关键平台信息返回概率")
    print()
    
    print("📊 结果处理对比:")
    print("   优化前: 随机顺序的搜索结果")
    print("   优化后: 关键平台信息优先排序")
    print("   提升: 确保重要信息不被忽略")
    print()
    
    print("🧠 分析指导对比:")
    print("   优化前: 通用分析指导")
    print("   优化后: 平台特定的分析框架和指导")
    print("   提升: 更专业、更结构化的分析结果")
    print()
    
    print("💰 成本影响:")
    print("   API调用: 无增加 ✓")
    print("   查询数量: 无增加 ✓")
    print("   搜索引擎: 增加Google (并行执行)")
    print("   处理时间: 微小增加")
    print()


async def main():
    """主演示函数"""
    print("🎯 优化后的竞品调研功能演示")
    print("=" * 70)
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 运行各项演示
    await demo_optimized_summary_research()
    print("\n" + "="*70 + "\n")
    
    await demo_optimized_detailed_research()
    print("\n" + "="*70 + "\n")
    
    show_platform_coverage()
    print("="*70 + "\n")
    
    show_optimization_benefits()
    
    print("✅ 演示完成！")
    print()
    print("🚀 下一步:")
    print("   1. 设置必要的API密钥 (OPENAI_API_KEY, TAVILY_API_KEY, GOOGLE_API_KEY等)")
    print("   2. 运行实际的竞品调研测试")
    print("   3. 观察平台信息覆盖率的提升")
    print("   4. 根据效果进一步优化")


if __name__ == "__main__":
    asyncio.run(main())
