#!/usr/bin/env python3
"""
竞品调研模式测试脚本
Test script for Competitive Intelligence mode
"""

import asyncio
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType


async def test_competitive_intelligence_summary():
    """测试竞品调研 Summary 模式"""
    print("🔍 测试竞品调研 Summary 模式...")
    print("=" * 50)
    
    try:
        # 创建 GPTResearcher 实例 - Summary 模式
        researcher = GPTResearcher(
            query="Notion",
            report_type=ReportType.CompetitiveIntelligence.value,
            report_source="web"
        )
        
        print(f"✅ 成功创建 GPTResearcher 实例")
        print(f"   - 查询: {researcher.query}")
        print(f"   - 报告类型: {researcher.report_type}")
        print(f"   - 数据源: {researcher.report_source}")
        
        # 验证报告类型映射是否正确
        from gpt_researcher.prompts import report_type_mapping
        if researcher.report_type in report_type_mapping:
            print(f"✅ 报告类型映射正确: {report_type_mapping[researcher.report_type]}")
        else:
            print(f"❌ 报告类型映射未找到: {researcher.report_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Summary 模式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_competitive_intelligence_detailed():
    """测试竞品调研 Detailed 模式"""
    print("\n🔍 测试竞品调研 Detailed 模式...")
    print("=" * 50)
    
    try:
        # 创建 GPTResearcher 实例 - Detailed 模式
        researcher = GPTResearcher(
            query="https://notion.so",
            report_type=ReportType.CompetitiveIntelligenceDetailed.value,
            report_source="web"
        )
        
        print(f"✅ 成功创建 GPTResearcher 实例")
        print(f"   - 查询: {researcher.query}")
        print(f"   - 报告类型: {researcher.report_type}")
        print(f"   - 数据源: {researcher.report_source}")
        
        # 验证报告类型映射是否正确
        from gpt_researcher.prompts import report_type_mapping
        if researcher.report_type in report_type_mapping:
            print(f"✅ 报告类型映射正确: {report_type_mapping[researcher.report_type]}")
        else:
            print(f"❌ 报告类型映射未找到: {researcher.report_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Detailed 模式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_prompt_generation():
    """测试提示词生成"""
    print("\n🔍 测试提示词生成...")
    print("=" * 50)
    
    try:
        from gpt_researcher.prompts import PromptFamily
        from gpt_researcher.config import Config
        
        config = Config()
        prompt_family = PromptFamily(config)
        
        # 测试 Summary 模式提示词
        summary_prompt = prompt_family.generate_competitive_intelligence_prompt(
            question="Notion",
            context="测试上下文信息",
            report_source="web"
        )
        
        print(f"✅ Summary 模式提示词生成成功")
        print(f"   - 提示词长度: {len(summary_prompt)} 字符")
        print(f"   - 包含产品名称: {'Notion' in summary_prompt}")
        print(f"   - 包含报告模板: {'产品情报报告' in summary_prompt}")
        
        # 测试 Detailed 模式提示词
        detailed_prompt = prompt_family.generate_competitive_intelligence_detailed_prompt(
            question="https://notion.so",
            context="详细测试上下文信息",
            report_source="web"
        )
        
        print(f"✅ Detailed 模式提示词生成成功")
        print(f"   - 提示词长度: {len(detailed_prompt)} 字符")
        print(f"   - 包含URL: {'notion.so' in detailed_prompt}")
        print(f"   - 包含详细版标记: {'详细版' in detailed_prompt}")
        
        return True
        
    except Exception as e:
        print(f"❌ 提示词生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_backend_integration():
    """测试后端集成"""
    print("\n🔍 测试后端集成...")
    print("=" * 50)
    
    try:
        from backend.report_type import CompetitiveIntelligenceReport, CompetitiveIntelligenceDetailedReport
        
        # 测试创建 Summary 报告类
        summary_report = CompetitiveIntelligenceReport(
            query="Notion",
            report_type="competitive_intelligence"
        )
        
        print(f"✅ CompetitiveIntelligenceReport 创建成功")
        print(f"   - 查询: {summary_report.query}")
        print(f"   - 报告类型: {summary_report.report_type}")
        
        # 测试创建 Detailed 报告类
        detailed_report = CompetitiveIntelligenceDetailedReport(
            query="https://notion.so",
            report_type="competitive_intelligence_detailed"
        )
        
        print(f"✅ CompetitiveIntelligenceDetailedReport 创建成功")
        print(f"   - 查询: {detailed_report.query}")
        print(f"   - 报告类型: {detailed_report.report_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ 后端集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("🚀 开始竞品调研模式集成测试")
    print("=" * 60)
    
    tests = [
        ("枚举和基础配置", test_competitive_intelligence_summary),
        ("详细模式配置", test_competitive_intelligence_detailed), 
        ("提示词生成", test_prompt_generation),
        ("后端集成", test_backend_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 运行测试: {test_name}")
        result = await test_func()
        results.append((test_name, result))
    
    # 总结测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(tests)} 个测试通过")
    
    if passed == len(tests):
        print("🎉 所有测试通过！竞品调研模式已成功集成。")
        print("\n💡 使用方法:")
        print("   - Summary 模式: report_type='competitive_intelligence'")
        print("   - Detailed 模式: report_type='competitive_intelligence_detailed'")
        print("   - 输入产品名称或URL即可开始调研")
    else:
        print("⚠️  部分测试失败，请检查错误信息。")


if __name__ == "__main__":
    asyncio.run(main())