#!/usr/bin/env python3
"""
快速生成可视化竞品调研报告

使用方法:
python run_visual_report.py [产品名称]
"""

import asyncio
import sys
import json
import os
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from backend.report_type.competitive_intelligence.competitive_intelligence import CompetitiveIntelligenceVisualReport


async def generate_visual_report(product_name: str):
    """生成可视化竞品调研报告"""
    print(f"🎯 开始生成 {product_name} 的可视化竞品调研报告...")
    print("=" * 60)
    
    try:
        # 创建可视化报告实例
        print("🔧 初始化可视化报告生成器...")
        visual_report = CompetitiveIntelligenceVisualReport(
            query=product_name,
            report_type="competitive_intelligence_visual",
            report_source="web"
        )
        
        print("🔍 正在进行深度调研...")
        print("  - 搜索产品信息和竞争对手")
        print("  - 分析关键指标和增长数据")
        print("  - 提取创始人和团队信息")
        print("  - 构建可视化数据结构")
        
        # 生成JSON数据
        json_data = await visual_report.run()
        
        # 生成HTML可视化报告
        print("🎨 生成HTML可视化报告...")
        html_content = await visual_report.generate_html_report()
        
        # 保存文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = product_name.replace('/', '_').replace('.', '_').replace(':', '_')
        
        # 确保输出目录存在
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        # 保存JSON数据
        json_file = output_dir / f"visual_{safe_name}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        # 保存HTML报告
        html_file = output_dir / f"visual_{safe_name}_{timestamp}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ 报告生成完成!")
        print(f"📊 JSON数据: {json_file}")
        print(f"🌐 HTML报告: {html_file}")
        
        # 显示关键信息摘要
        print("\n📋 报告摘要:")
        metadata = json_data.get("metadata", {})
        hero_data = json_data.get("layer_1_hero", {}).get("hero_snapshot", {})
        key_metrics = hero_data.get("key_metrics", {})
        
        print(f"  产品名称: {metadata.get('product_name', 'Unknown')}")
        print(f"  产品定位: {hero_data.get('tagline', 'Unknown')[:80]}...")
        print(f"  ARR: {key_metrics.get('arr', '未知')}")
        print(f"  客户数: {key_metrics.get('clients', '未知')}")
        print(f"  增长率: {key_metrics.get('growth_90d', '未知')}")
        print(f"  复刻难度: {key_metrics.get('replication_difficulty', '未知')}")
        
        print(f"\n🎉 请在浏览器中打开 {html_file} 查看可视化报告!")
        
        # 尝试自动打开HTML文件
        try:
            import webbrowser
            webbrowser.open(f'file://{html_file.absolute()}')
            print("🌐 正在自动打开浏览器...")
        except:
            print("💡 请手动在浏览器中打开HTML文件")
        
        return str(html_file.absolute())
        
    except Exception as e:
        print(f"❌ 生成报告时出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    # 获取产品名称
    if len(sys.argv) > 1:
        product_name = sys.argv[1]
    else:
        print("🎯 可视化竞品调研报告生成器")
        print("=" * 40)
        print("请输入要分析的产品名称或URL:")
        print("例如: notion, figma, claude.ai, https://example.com")
        print()
        product_name = input("产品名称: ").strip()
        
        if not product_name:
            print("❌ 请提供产品名称!")
            return
    
    # 生成报告
    html_path = asyncio.run(generate_visual_report(product_name))
    
    if html_path:
        print("\n" + "=" * 60)
        print("🎉 可视化报告已生成!")
        print(f"📂 文件位置: {html_path}")
        print("💡 提示: 可视化报告包含4层信息结构:")
        print("   - 0-5秒: Hero快照 + 关键指标")
        print("   - 5-30秒: 竞争雷达图 + 增长时间轴")
        print("   - 30秒-3分钟: 洞察卡片 + 护城河分析")
        print("   - 3分钟+: 详细调研数据")


if __name__ == "__main__":
    main()