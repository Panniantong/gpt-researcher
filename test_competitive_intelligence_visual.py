#!/usr/bin/env python3
"""
竞品调研可视化报告测试脚本

测试新的可视化竞品调研功能，包括JSON数据生成和HTML可视化输出。
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from backend.report_type.competitive_intelligence.competitive_intelligence import CompetitiveIntelligenceVisualReport


async def test_visual_report_generation():
    """测试可视化报告生成功能"""
    print("🚀 开始测试竞品调研可视化报告生成...")
    
    # 测试产品列表
    test_products = [
        "notion",
        "figma", 
        "claude.ai",
        "https://gadget.dev"
    ]
    
    for product in test_products:
        print(f"\n📊 测试产品: {product}")
        
        try:
            # 创建可视化报告实例
            visual_report = CompetitiveIntelligenceVisualReport(
                query=product,
                report_type="competitive_intelligence_visual",
                report_source="web"
            )
            
            print(f"  ✅ 创建报告实例成功")
            
            # 生成JSON数据
            print(f"  🔍 开始调研和数据生成...")
            json_data = await visual_report.run()
            
            print(f"  ✅ JSON数据生成成功")
            print(f"  📝 数据结构验证:")
            
            # 验证数据结构
            required_keys = ["metadata", "layer_1_hero", "layer_2_visual", "layer_3_cards"]
            for key in required_keys:
                if key in json_data:
                    print(f"    ✅ {key}: 存在")
                else:
                    print(f"    ❌ {key}: 缺失")
            
            # 保存JSON数据
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = f"outputs/visual_report_{product.replace('/', '_').replace('.', '_')}_{timestamp}.json"
            
            os.makedirs("outputs", exist_ok=True)
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            print(f"  💾 JSON数据已保存: {json_filename}")
            
            # 生成HTML报告
            print(f"  🎨 生成HTML可视化报告...")
            html_content = await visual_report.generate_html_report()
            
            # 保存HTML报告
            html_filename = f"outputs/visual_report_{product.replace('/', '_').replace('.', '_')}_{timestamp}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"  ✅ HTML报告已保存: {html_filename}")
            print(f"  📏 HTML文件大小: {len(html_content):,} 字符")
            
            # 验证关键数据
            hero_data = json_data.get("layer_1_hero", {}).get("hero_snapshot", {})
            tagline = hero_data.get("tagline", "")
            metrics = hero_data.get("key_metrics", {})
            
            print(f"  📋 核心数据摘要:")
            print(f"    - 产品定位: {tagline[:50]}...")
            print(f"    - ARR: {metrics.get('arr', '未知')}")
            print(f"    - 客户数: {metrics.get('clients', '未知')}")
            print(f"    - 增长率: {metrics.get('growth_90d', '未知')}")
            print(f"    - 复刻难度: {metrics.get('replication_difficulty', '未知')}")
            
            print(f"  🎉 产品 {product} 测试完成!\n")
            
        except Exception as e:
            print(f"  ❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print("🏁 所有测试完成!")


async def test_template_rendering():
    """测试模板渲染功能"""
    print("\n🎨 测试模板渲染功能...")
    
    # 创建测试数据
    test_data = {
        "metadata": {
            "product_name": "测试产品",
            "report_date": "2025-06-14",
            "version": "2.0"
        },
        "layer_1_hero": {
            "hero_snapshot": {
                "tagline": "AI驱动的测试产品解决方案",
                "key_metrics": {
                    "arr": "$500K",
                    "clients": 25,
                    "growth_90d": "+25%",
                    "replication_difficulty": "中等"
                }
            },
            "value_curve": {
                "problems": ["测试问题1", "测试问题2", "测试问题3"],
                "solutions": ["测试解决方案1", "测试解决方案2", "测试解决方案3"]
            }
        },
        "layer_2_visual": {
            "competitive_radar": {
                "dimensions": ["定制化", "自动化深度", "开源透明", "生态", "价格"],
                "scores": [3.5, 4.0, 3.0, 3.5, 4.2],
                "competitors": [
                    {"name": "竞品A", "scores": [3.0, 3.5, 4.0, 3.0, 3.8]},
                    {"name": "竞品B", "scores": [4.0, 3.0, 2.5, 4.0, 3.0]}
                ]
            },
            "growth_timeline": [
                {
                    "date": "2024-01",
                    "milestone": "产品发布",
                    "type": "product",
                    "description": "初版产品正式发布"
                },
                {
                    "date": "2024-03", 
                    "milestone": "种子轮融资",
                    "type": "funding",
                    "description": "完成100万美元种子轮融资"
                }
            ],
            "metrics_chart": {
                "revenue_data": [
                    {"period": "2024-Q1", "value": 50, "growth_rate": 0},
                    {"period": "2024-Q2", "value": 125, "growth_rate": 150},
                    {"period": "2024-Q3", "value": 300, "growth_rate": 140},
                    {"period": "2024-Q4", "value": 500, "growth_rate": 67}
                ],
                "user_data": [
                    {"period": "2024-Q1", "value": 500, "growth_rate": 0},
                    {"period": "2024-Q2", "value": 1200, "growth_rate": 140},
                    {"period": "2024-Q3", "value": 2800, "growth_rate": 133},
                    {"period": "2024-Q4", "value": 5000, "growth_rate": 79}
                ]
            }
        },
        "layer_3_cards": {
            "insight_cards": {
                "pain_points": {
                    "title": "核心痛点",
                    "icon": "AlertTriangle",
                    "content": "用户在使用传统工具时面临效率低下、成本高昂、操作复杂等问题。",
                    "evidence_url": "https://example.com/evidence"
                },
                "target_users": {
                    "title": "目标用户",
                    "icon": "Users",
                    "content": "主要面向中小企业的技术团队和创业公司，需要高效协作工具。",
                    "evidence_url": ""
                },
                "core_scenarios": {
                    "title": "核心场景",
                    "icon": "Workflow",
                    "content": "团队协作、项目管理、文档共享、实时沟通等日常工作场景。",
                    "evidence_url": ""
                }
            },
            "founder_moat_canvas": {
                "founder_info": {
                    "name": "张三",
                    "avatar_url": "",
                    "title": "CEO & 创始人"
                },
                "quadrants": {
                    "industry_knowhow": "拥有10年企业级软件开发经验",
                    "capital_backing": "获得知名投资机构A轮投资",
                    "channel_resources": "建立了覆盖全国的销售网络",
                    "community_influence": "技术社区意见领袖，5万粉丝"
                }
            }
        },
        "layer_4_detailed": {
            "detailed_research": {
                "full_analysis": "这是一个详细的分析报告，包含对产品的全面评估...",
                "methodology": "采用多维度竞品分析方法，结合用户调研和市场数据",
                "research_sources": [
                    {
                        "url": "https://example.com/source1",
                        "title": "行业报告1",
                        "source_type": "行业报告",
                        "reliability": 4
                    },
                    {
                        "url": "https://example.com/source2", 
                        "title": "用户评价汇总",
                        "source_type": "用户反馈",
                        "reliability": 3
                    }
                ],
                "data_gaps": [
                    "具体财务数据缺失",
                    "用户留存率数据不完整"
                ]
            }
        },
        "ui_config": {
            "theme": {
                "primary_color": "#0EA5E9",
                "accent_color": "#06B6D4"
            }
        }
    }
    
    try:
        # 测试模板渲染
        from templates.renderer import TemplateRenderer
        
        templates_dir = Path("templates")
        renderer = TemplateRenderer(str(templates_dir))
        
        print("  🔧 创建模板渲染器...")
        html_content = renderer.render_competitive_intelligence_visual(test_data)
        
        print("  ✅ 模板渲染成功")
        print(f"  📏 HTML内容长度: {len(html_content):,} 字符")
        
        # 保存测试HTML
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_html_file = f"outputs/template_test_{timestamp}.html"
        
        os.makedirs("outputs", exist_ok=True)
        with open(test_html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  💾 测试HTML已保存: {test_html_file}")
        print("  🎉 模板渲染测试完成!")
        
    except Exception as e:
        print(f"  ❌ 模板渲染测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


def test_data_validation():
    """测试数据验证功能"""
    print("\n🔍 测试数据验证功能...")
    
    try:
        # 创建不完整的测试数据
        incomplete_data = {
            "metadata": {"product_name": "不完整产品"},
            "layer_1_hero": {}
        }
        
        # 创建可视化报告实例进行验证
        visual_report = CompetitiveIntelligenceVisualReport(
            query="test",
            report_type="competitive_intelligence_visual"
        )
        
        print("  🔧 测试数据验证和补全...")
        validated_data = visual_report._validate_and_enhance_json(incomplete_data)
        
        print("  ✅ 数据验证完成")
        
        # 检查必要字段是否被补全
        required_checks = [
            ("metadata.product_name", validated_data.get("metadata", {}).get("product_name")),
            ("metadata.report_date", validated_data.get("metadata", {}).get("report_date")),
            ("layer_1_hero.hero_snapshot", validated_data.get("layer_1_hero", {}).get("hero_snapshot")),
            ("layer_2_visual.competitive_radar", validated_data.get("layer_2_visual", {}).get("competitive_radar")),
            ("ui_config", validated_data.get("ui_config"))
        ]
        
        print("  📋 验证结果:")
        for check_name, value in required_checks:
            if value:
                print(f"    ✅ {check_name}: 已补全")
            else:
                print(f"    ❌ {check_name}: 仍缺失")
        
        print("  🎉 数据验证测试完成!")
        
    except Exception as e:
        print(f"  ❌ 数据验证测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


async def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 竞品调研可视化系统集成测试")
    print("=" * 60)
    
    # 检查环境
    print("\n🔧 检查测试环境...")
    
    required_files = [
        "gpt_researcher/prompts.py",
        "backend/report_type/competitive_intelligence/competitive_intelligence.py",
        "templates/competitive_intelligence_visual.html",
        "templates/renderer.py",
        "schemas/competitive_intelligence_visual_schema.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ 缺失必要文件:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return
    
    print("  🎉 环境检查通过!")
    
    # 运行测试
    try:
        # 测试1: 数据验证
        test_data_validation()
        
        # 测试2: 模板渲染
        await test_template_rendering()
        
        # 测试3: 完整报告生成（仅测试一个产品）
        print("\n📊 快速功能测试（测试一个产品）...")
        
        test_visual_report = CompetitiveIntelligenceVisualReport(
            query="notion",
            report_type="competitive_intelligence_visual",
            report_source="web"
        )
        
        print("  🔍 生成测试报告...")
        json_data = await test_visual_report.run()
        
        if json_data and "metadata" in json_data:
            print("  ✅ 快速功能测试通过!")
            
            # 保存快速测试结果
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            quick_test_file = f"outputs/quick_test_{timestamp}.json"
            
            os.makedirs("outputs", exist_ok=True)
            with open(quick_test_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            print(f"  💾 快速测试结果已保存: {quick_test_file}")
        else:
            print("  ❌ 快速功能测试失败")
    
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🏁 测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())