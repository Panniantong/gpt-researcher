#!/usr/bin/env python3
"""
竞品调研可视化系统使用演示

展示如何使用新的可视化竞品调研功能，生成现代化的HTML可视化报告。
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

# Add project root to path
import sys
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from backend.report_type.competitive_intelligence.competitive_intelligence import CompetitiveIntelligenceVisualReport


async def demo_visual_report():
    """演示可视化竞品调研报告生成"""
    print("🎯 竞品调研可视化系统演示")
    print("=" * 50)
    
    # 用户输入产品名称
    print("\n请输入要分析的产品名称或URL:")
    print("例如: notion, figma, claude.ai, https://example.com")
    
    # 为了演示，我们使用预设的产品
    product = "chat4data"  # 你可以改成任何产品
    print(f"📊 正在分析产品: {product}")
    
    try:
        # 步骤1: 创建可视化报告实例
        print("\n🔧 初始化可视化报告生成器...")
        visual_report = CompetitiveIntelligenceVisualReport(
            query=product,
            report_type="competitive_intelligence_visual",
            report_source="web"
        )
        
        # 步骤2: 生成结构化JSON数据
        print("🔍 正在调研和生成结构化数据...")
        print("  - 搜索产品信息")
        print("  - 分析竞争对手")
        print("  - 提取关键指标") 
        print("  - 构建可视化数据")
        
        json_data = await visual_report.run()
        
        print("✅ JSON数据生成完成!")
        
        # 步骤3: 显示关键数据摘要
        print("\n📋 核心数据摘要:")
        metadata = json_data.get("metadata", {})
        hero_data = json_data.get("layer_1_hero", {}).get("hero_snapshot", {})
        
        print(f"  产品名称: {metadata.get('product_name', 'Unknown')}")
        print(f"  产品定位: {hero_data.get('tagline', 'Unknown')}")
        print(f"  ARR: {hero_data.get('key_metrics', {}).get('arr', 'Unknown')}")
        print(f"  客户数: {hero_data.get('key_metrics', {}).get('clients', 'Unknown')}")
        print(f"  增长率: {hero_data.get('key_metrics', {}).get('growth_90d', 'Unknown')}")
        print(f"  复刻难度: {hero_data.get('key_metrics', {}).get('replication_difficulty', 'Unknown')}")
        
        # 步骤4: 生成HTML可视化报告
        print("\n🎨 生成HTML可视化报告...")
        html_content = await visual_report.generate_html_report()
        
        # 步骤5: 保存文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存JSON数据
        json_filename = f"outputs/demo_{product}_{timestamp}.json"
        os.makedirs("outputs", exist_ok=True)
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        # 保存HTML报告
        html_filename = f"outputs/demo_{product}_{timestamp}.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("💾 文件保存完成:")
        print(f"  JSON数据: {json_filename}")
        print(f"  HTML报告: {html_filename}")
        
        # 步骤6: 显示报告特色
        print("\n🌟 可视化报告特色:")
        print("  ✨ 4层信息金字塔设计")
        print("    - 0-5秒: Hero Snapshot 快速概览")
        print("    - 5-30秒: 竞争雷达图 + 增长时间轴")
        print("    - 30秒-3分钟: 6大洞察卡片") 
        print("    - 3分钟+: 详细调研数据")
        print("  📊 5个核心可视化组件:")
        print("    - Hero Snapshot: 关键指标概览")
        print("    - Value Curve: 问题→解决方案路径")
        print("    - Competitive Radar: 5维度雷达图")
        print("    - Growth Timeline: 增长里程碑")
        print("    - Founder Moat Canvas: 创始人护城河")
        print("  🎨 现代化UI设计:")
        print("    - TailwindCSS + Chart.js")
        print("    - 响应式布局 + 微动画")
        print("    - 深色模式支持")
        
        print(f"\n🎉 演示完成! 请打开 {html_filename} 查看可视化报告")
        
        return json_data, html_content
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None


def show_usage_examples():
    """显示使用示例"""
    print("\n📚 使用示例:")
    print("""
# 基本用法
from backend.report_type.competitive_intelligence.competitive_intelligence import CompetitiveIntelligenceVisualReport

# 创建可视化报告实例
visual_report = CompetitiveIntelligenceVisualReport(
    query="notion",  # 产品名称或URL
    report_type="competitive_intelligence_visual",
    report_source="web"
)

# 生成JSON数据
json_data = await visual_report.run()

# 生成HTML报告
html_content = await visual_report.generate_html_report()

# 保存文件
with open("report.html", "w", encoding="utf-8") as f:
    f.write(html_content)
""")


def show_data_structure():
    """显示数据结构说明"""
    print("\n🏗️ 数据结构说明:")
    print("""
JSON数据包含4个主要层级:

📦 metadata: 报告元数据
  ├── product_name: 产品名称
  ├── report_date: 报告日期
  ├── version: 版本号
  └── report_type: 报告类型

🎯 layer_1_hero: 英雄区块 (0-5秒)
  ├── hero_snapshot: 核心指标
  │   ├── tagline: 一句话定位
  │   └── key_metrics: ARR, 客户数, 增长率, 复刻难度
  └── value_curve: 价值曲线
      ├── problems: 核心痛点列表
      └── solutions: 解决方案列表

📊 layer_2_visual: 可视化图表 (5-30秒)
  ├── competitive_radar: 竞争雷达图
  ├── growth_timeline: 增长时间轴
  └── metrics_chart: 指标图表

💡 layer_3_cards: 洞察卡片 (30秒-3分钟)
  ├── insight_cards: 6大洞察卡片
  └── founder_moat_canvas: 创始人护城河

📚 layer_4_detailed: 详细数据 (3分钟+)
  ├── detailed_research: 完整分析
  └── competitive_analysis: 竞争分析
""")


async def main():
    """主函数"""
    print("🚀 欢迎使用竞品调研可视化系统!")
    print("这是一个现代化的竞品分析工具，能够生成美观的HTML可视化报告。")
    
    # 显示数据结构
    show_data_structure()
    
    # 显示使用示例
    show_usage_examples()
    
    # 运行演示
    await demo_visual_report()
    
    print("\n" + "=" * 50)
    print("感谢使用竞品调研可视化系统! 🙏")


if __name__ == "__main__":
    asyncio.run(main())