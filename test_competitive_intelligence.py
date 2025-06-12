"""
Quick test script for CompetitiveIntelligenceAgent
快速测试竞品情报代理功能
"""

import asyncio
import os
from dotenv import load_dotenv

from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config


async def test_basic_functionality():
    """测试基本功能"""
    print("🧪 测试竞品情报代理基本功能...\n")
    
    # 加载环境变量
    load_dotenv()
    
    # 测试产品
    test_product = "Notion"
    test_url = "https://notion.so"
    
    try:
        # 创建代理
        config = Config()
        agent = CompetitiveIntelligenceAgent(
            product_name=test_product,
            product_url=test_url,
            config=config
        )
        
        print(f"✅ 成功创建代理: {agent.product_name}")
        
        # 测试查询构建器
        print("\n📝 测试查询构建器:")
        queries = agent.query_builder.build_all_queries()
        for module, template in queries.items():
            print(f"\n[{module}]")
            print(f"  查询数: {len(template.queries)}")
            print(f"  首个查询: {template.queries[0]}")
            print(f"  优先来源: {template.sources[:2]}")
        
        # 测试报告生成器
        print("\n📄 测试报告生成器:")
        test_data = {
            "product_info": {
                "name": test_product,
                "url": test_url,
                "team_size": "100-500",
                "one_liner": "All-in-one workspace",
                "type": "SaaS",
                "launch_status": "GA",
                "founded": "2016"
            },
            "founder_info": {
                "profile": {
                    "identity_background": "前Linkedin工程师",
                    "technical_ability": "全栈开发经验",
                    "industry_depth": "10年生产力工具经验"
                },
                "unfair_advantages": {
                    "industry_insight": "深刻理解知识工作者痛点",
                    "technical_implementation": "创新的块编辑器架构"
                },
                "validation": "被业界认可为协作工具革新者",
                "sources": ["https://example.com/founder-interview"]
            },
            "eight_dimensions": {
                "pitch": "重新定义文档协作",
                "fixed_broken_spot": {
                    "description": "解决了传统文档工具功能单一的问题",
                    "sources": ["https://example.com/problem"]
                },
                "user_urgency": {
                    "description": "用户迫切需要统一的工作空间",
                    "sources": ["https://example.com/reviews"]
                },
                "who_when_action": "知识工作者在需要组织信息时使用",
                "pain_and_level": "信息碎片化，痛点程度高",
                "arena_and_scoring": {
                    "arena_description": "协作文档与知识管理赛道",
                    "scoring_metrics": [
                        {
                            "metric": "功能丰富度",
                            "evidence": "集成数据库、看板、日历等",
                            "source": "https://example.com/features"
                        }
                    ],
                    "competitor_scoring": {
                        "metrics": ["功能", "易用性", "协作"],
                        "scores": {
                            "Notion": {"功能": 9, "易用性": 8, "协作": 9},
                            "Confluence": {"功能": 7, "易用性": 6, "协作": 8},
                            "Obsidian": {"功能": 8, "易用性": 7, "协作": 5}
                        }
                    },
                    "leading_logic": "通过All-in-one理念占据用户心智"
                },
                "first_only_number": {
                    "description": "首个真正实现块编辑的协作工具",
                    "sources": ["https://example.com/innovation"]
                },
                "implementation_architecture": {
                    "feature_breakdown": "块编辑器、数据库、API",
                    "api_composition": "RESTful API + Webhooks",
                    "innovation_points": "实时协作、灵活的内容块"
                }
            },
            "growth_intelligence": {
                "timeline_milestones": [
                    {"date": "2016", "event": "产品发布"},
                    {"date": "2019", "event": "用户破百万"},
                    {"date": "2021", "event": "估值破20亿美元"}
                ],
                "channels_tactics": [
                    {"channel": "社区", "tactic": "模板生态系统"},
                    {"channel": "内容", "tactic": "用户案例分享"}
                ],
                "sources": ["https://example.com/growth"]
            },
            "feasibility": {
                "difficulty_level": "高",
                "ai_stack_analysis": "需要复杂的实时协作基础设施",
                "technical_challenges": ["实时同步", "块编辑器", "权限系统"],
                "ai_advantages": "AI可辅助内容生成和组织",
                "industry_barriers": "网络效应和用户习惯"
            },
            "executive_summary": {
                "core_insight": "Notion通过重新定义文档协作，成功占据知识管理工具的心智高地",
                "growth_model": "模板生态+社区驱动，形成强大的网络效应",
                "founder_advantage": "深厚的技术背景与对生产力工具的独特理解",
                "transferable_elements": ["模块化设计", "社区运营", "模板策略"],
                "trend_judgment": "All-in-one工作空间是未来趋势",
                "indie_developer_strategy": "聚焦垂直场景，打造轻量级专注工具，避免正面竞争"
            }
        }
        
        report = agent.report_generator.generate_report(test_data)
        print("\n生成的报告预览（前500字）:")
        print(report[:500] + "...")
        
        print("\n\n✅ 所有测试通过！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


async def test_query_generation():
    """测试查询生成功能"""
    print("🧪 测试查询生成功能...\n")
    
    from gpt_researcher.agents.utils import CompetitiveQueryBuilder
    
    # 测试不同产品的查询生成
    test_cases = [
        {"name": "ChatGPT", "url": "https://chat.openai.com"},
        {"name": "Claude", "url": "https://claude.ai"},
        {"name": "Perplexity", "url": None}
    ]
    
    for test in test_cases:
        print(f"\n测试产品: {test['name']}")
        builder = CompetitiveQueryBuilder(test['name'], test['url'])
        
        # 测试基础信息查询
        basic_queries = builder._build_basic_info_queries()
        print(f"  基础信息查询数: {len(basic_queries.queries)}")
        
        # 测试竞品查询
        competitors = ["Competitor1", "Competitor2"]
        comp_queries = builder.get_competitor_queries(competitors)
        print(f"  竞品查询数: {len(comp_queries)}")


async def test_competitor_identification():
    """测试竞品识别功能"""
    print("🧪 测试竞品识别功能...\n")
    
    from gpt_researcher.agents.utils import CompetitorAnalyzer
    
    analyzer = CompetitorAnalyzer()
    
    # 模拟搜索结果
    mock_search_results = [
        {
            "title": "ChatGPT vs Claude: Which AI Assistant is Better?",
            "content": "Comparing ChatGPT and Claude features..."
        },
        {
            "title": "Best ChatGPT Alternatives: Bard, Claude, and Perplexity",
            "content": "Looking for alternatives to ChatGPT? Try Bard or Claude..."
        },
        {
            "title": "Competitors of ChatGPT in 2024",
            "content": "Main competitors to ChatGPT include Google Bard and Anthropic Claude..."
        }
    ]
    
    # 测试竞品识别
    competitors = await analyzer.identify_competitors("ChatGPT", mock_search_results)
    print(f"识别到的竞品: {competitors}")
    
    # 测试评分指标定义
    metrics = analyzer.define_scoring_metrics("ai_tool")
    print(f"\nAI工具类评分指标: {metrics}")
    
    # 测试评分矩阵生成
    scoring_data = analyzer.generate_scoring_matrix(
        "ChatGPT",
        ["Claude", "Bard"],
        {
            "ChatGPT": {"模型质量": 9, "响应速度": 8, "准确率": 8.5},
            "Claude": {"模型质量": 9.5, "响应速度": 7.5, "准确率": 9},
            "Bard": {"模型质量": 8, "响应速度": 9, "准确率": 7.5}
        }
    )
    print(f"\n评分矩阵指标: {scoring_data['metrics']}")
    
    # 测试竞争优势分析
    advantage = analyzer.analyze_competitive_advantage("ChatGPT")
    print(f"\n竞争优势分析: {advantage}")


async def main():
    """运行所有测试"""
    print("🚀 开始测试竞品情报代理...\n")
    print("=" * 60)
    
    # 运行各项测试
    await test_basic_functionality()
    print("\n" + "=" * 60 + "\n")
    
    await test_query_generation()
    print("\n" + "=" * 60 + "\n")
    
    await test_competitor_identification()
    print("\n" + "=" * 60 + "\n")
    
    print("✅ 所有测试完成！")


if __name__ == "__main__":
    asyncio.run(main())