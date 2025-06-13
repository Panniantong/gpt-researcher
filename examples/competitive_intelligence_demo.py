#!/usr/bin/env python3
"""
竞品调研模式使用示例
Competitive Intelligence Mode Demo

这个示例展示了如何使用新的竞品调研模式来分析产品。
"""

import asyncio
import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType


async def demo_summary_mode():
    """演示 Summary 模式的竞品调研"""
    print("🔍 竞品调研 - Summary 模式演示")
    print("=" * 50)
    print("输入：产品名称")
    print("模式：快速概览分析")
    print("适用：初步了解产品情况")
    print()
    
    # 创建研究员实例
    researcher = GPTResearcher(
        query="Notion",  # 可以是产品名称
        report_type=ReportType.CompetitiveIntelligence.value,
        report_source="web"
    )
    
    print(f"✅ 已创建竞品调研员")
    print(f"   - 目标产品: {researcher.query}")
    print(f"   - 报告类型: {researcher.report_type}")
    print(f"   - 分析模式: Summary (概览)")
    print()
    
    # 注意：实际运行会调用 API 并产生费用，这里只演示配置
    print("💡 实际使用时，运行以下代码:")
    print("   await researcher.conduct_research()")
    print("   report = await researcher.write_report()")
    print()
    
    return researcher


async def demo_detailed_mode():
    """演示 Detailed 模式的竞品调研"""
    print("🔍 竞品调研 - Detailed 模式演示")
    print("=" * 50)
    print("输入：产品URL")
    print("模式：深度全面分析")
    print("适用：详细竞争情报研究")
    print()
    
    # 创建研究员实例
    researcher = GPTResearcher(
        query="https://notion.so",  # 可以是产品URL
        report_type=ReportType.CompetitiveIntelligenceDetailed.value,
        report_source="web"
    )
    
    print(f"✅ 已创建竞品调研员")
    print(f"   - 目标产品: {researcher.query}")
    print(f"   - 报告类型: {researcher.report_type}")
    print(f"   - 分析模式: Detailed (详细)")
    print()
    
    # 注意：实际运行会调用 API 并产生费用，这里只演示配置
    print("💡 实际使用时，运行以下代码:")
    print("   await researcher.conduct_research()")
    print("   report = await researcher.write_report()")
    print()
    
    return researcher


async def demo_backend_usage():
    """演示后端报告类的直接使用"""
    print("🔧 后端报告类使用演示")
    print("=" * 50)
    
    from backend.report_type import CompetitiveIntelligenceReport, CompetitiveIntelligenceDetailedReport
    
    # Summary 模式
    summary_report = CompetitiveIntelligenceReport(
        query="Claude",
        report_type="competitive_intelligence"
    )
    
    print(f"✅ 创建 Summary 报告类")
    print(f"   - 类名: {summary_report.__class__.__name__}")
    print(f"   - 查询: {summary_report.query}")
    
    # Detailed 模式
    detailed_report = CompetitiveIntelligenceDetailedReport(
        query="https://claude.ai",
        report_type="competitive_intelligence_detailed"
    )
    
    print(f"✅ 创建 Detailed 报告类")
    print(f"   - 类名: {detailed_report.__class__.__name__}")
    print(f"   - 查询: {detailed_report.query}")
    print()
    
    return summary_report, detailed_report


def show_prompt_preview():
    """显示提示词预览"""
    print("📝 提示词模板预览")
    print("=" * 50)
    
    from gpt_researcher.prompts import PromptFamily
    from gpt_researcher.config import Config
    
    config = Config()
    prompt_family = PromptFamily(config)
    
    # 生成示例提示词
    sample_prompt = prompt_family.generate_competitive_intelligence_prompt(
        question="示例产品",
        context="这里是研究上下文信息...",
        report_source="web"
    )
    
    # 显示提示词结构
    lines = sample_prompt.split('\n')
    structure_lines = [line for line in lines if any(keyword in line for keyword in [
        '# 身份', '# 核心任务', '# 核心视角', '# 执行规则', 
        '### Part', '### 【', '- Q', '- 📈', '- 🎯'
    ])]
    
    print("📋 报告结构预览:")
    for line in structure_lines[:20]:  # 显示前20行结构
        if line.strip():
            print(f"   {line.strip()}")
    
    print(f"   ... (完整提示词共 {len(lines)} 行)")
    print()


async def main():
    """主演示函数"""
    print("🚀 竞品调研模式功能演示")
    print("=" * 60)
    print("✨ 新功能特点:")
    print("   • 专门针对产品竞争情报分析")
    print("   • 支持产品名称和URL输入")
    print("   • 提供Summary和Detailed两种模式")
    print("   • 内置结构化报告模板")
    print("   • focus商业壁垒和竞争优势分析")
    print()
    
    # 演示各种使用方式
    demos = [
        ("Summary 模式", demo_summary_mode),
        ("Detailed 模式", demo_detailed_mode),
        ("后端集成", demo_backend_usage),
    ]
    
    for demo_name, demo_func in demos:
        print(f"🎯 {demo_name}")
        await demo_func()
        print()
    
    # 显示提示词预览
    show_prompt_preview()
    
    # 使用指南
    print("📖 使用指南")
    print("=" * 50)
    print("1️⃣ 基础用法 (GPTResearcher):")
    print("   researcher = GPTResearcher(")
    print("       query='产品名称或URL',")
    print("       report_type='competitive_intelligence'  # 或 'competitive_intelligence_detailed'")
    print("   )")
    print()
    
    print("2️⃣ 后端用法 (Report Classes):")
    print("   from backend.report_type import CompetitiveIntelligenceReport")
    print("   report = CompetitiveIntelligenceReport(query='产品名称')")
    print()
    
    print("3️⃣ API用法 (通过服务器):")
    print("   POST /research")
    print("   {")
    print("     'task': '产品名称或URL',")
    print("     'report_type': 'competitive_intelligence',")
    print("     'report_source': 'web'")
    print("   }")
    print()
    
    print("⚠️  注意事项:")
    print("   • 实际运行会调用LLM API，请注意费用控制")
    print("   • 建议先用测试数据验证配置")
    print("   • Summary模式适合快速概览")
    print("   • Detailed模式提供更深入分析")
    print()
    
    print("🎉 竞品调研模式已成功集成到GPT Researcher!")


if __name__ == "__main__":
    asyncio.run(main())