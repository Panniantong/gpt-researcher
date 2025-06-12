"""
竞品调研 Agent - 完整工作示例
这个示例展示了如何使用竞品调研Agent进行产品分析
"""
import asyncio
import os
from dotenv import load_dotenv
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from competitive_intelligence import CompetitiveIntelligenceAgent
from competitive_intelligence.modules.eight_dimensions import EightDimensionsAnalyzer
from competitive_intelligence.modules.replication_eval import ReplicationEvaluator
from competitive_intelligence.modules.executive_summary import ExecutiveSummaryGenerator


async def analyze_product_complete():
    """完整的产品分析示例"""
    print("🔍 竞品调研 Agent - 完整分析示例")
    print("=" * 50)
    
    # 要分析的产品
    product_name = "Cursor"
    product_url = "https://cursor.sh"
    
    print(f"\n📊 分析产品: {product_name}")
    print(f"🌐 产品URL: {product_url}\n")
    
    # 创建Agent
    agent = CompetitiveIntelligenceAgent(
        query=product_name,
        product_url=product_url,
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    # 步骤1: 基础信息提取
    print("1️⃣ 提取基础信息...")
    await agent._extract_basic_info()
    
    basic_info = agent.results.get("basic_info", {})
    print(f"   ✓ 产品名称: {basic_info.get('name', 'N/A')}")
    print(f"   ✓ 描述: {basic_info.get('one_liner', 'N/A')}")
    print(f"   ✓ 团队规模: {basic_info.get('team_size', 'N/A')}")
    
    # 步骤2: 八维分析（本地部分）
    print("\n2️⃣ 进行产品分析...")
    
    analyzer = EightDimensionsAnalyzer("openai", "gpt-4o-mini")
    
    # 分析不需要搜索的维度
    dimensions_results = {}
    
    # Q1: One-sentence Pitch
    q1 = await analyzer._analyze_q1(basic_info)
    dimensions_results["Q1"] = q1
    print(f"   ✓ Q1 - {q1.question}: {q1.answer}")
    
    # Q4: Who-When-Action
    q4 = await analyzer._analyze_q4(basic_info)
    dimensions_results["Q4"] = q4
    print(f"   ✓ Q4 - {q4.question}: {q4.answer}")
    
    # Q5: Pain & Pain-level
    q5 = await analyzer._analyze_q5(basic_info)
    dimensions_results["Q5"] = q5
    print(f"   ✓ Q5 - {q5.question}: {q5.answer}")
    
    # 步骤3: 复刻难度评估
    print("\n3️⃣ 评估复刻难度...")
    
    evaluator = ReplicationEvaluator("openai", "gpt-4o-mini")
    
    # 模拟技术架构信息
    tech_architecture = """
    Cursor是基于VSCode的AI代码编辑器，主要技术架构包括：
    1. 基于VSCode/Electron的桌面应用
    2. 深度集成OpenAI GPT-4等大语言模型
    3. 自定义的代码上下文理解系统
    4. 实时代码补全和重构功能
    """
    
    evaluation = await evaluator.evaluate_replication_difficulty(
        basic_info,
        tech_architecture
    )
    
    print(f"   ✓ 难度等级: {evaluation.get('difficulty_level')}")
    
    # 步骤4: 生成简化的执行摘要
    print("\n4️⃣ 生成执行摘要...")
    
    # 准备模拟数据
    mock_founder_analysis = {
        "profile": {
            "background": "MIT毕业，前Facebook工程师",
            "technical_skills": "深度学习、编译器设计",
            "industry_depth": "5年+开发工具经验"
        },
        "unfair_advantages": ["AI/ML技术背景", "深厚的编程语言理论基础"],
        "ai_expert_model": {"fits_pattern": True}
    }
    
    mock_marketing_intel = {
        "growth_timeline": {
            "launch_phase": "2022年在HackerNews发布MVP",
            "growth_phase": "2023年获得种子轮融资"
        },
        "growth_channels": {
            "primary_channels": ["开发者社区", "口碑传播", "内容营销"]
        }
    }
    
    # 将结果整合
    agent.results["eight_dimensions"] = dimensions_results
    agent.results["replication_eval"] = evaluation
    
    summary_generator = ExecutiveSummaryGenerator("openai", "gpt-4o-mini")
    
    summary = await summary_generator.generate_summary(
        basic_info,
        mock_founder_analysis,
        dimensions_results,
        mock_marketing_intel,
        evaluation
    )
    
    print(f"   ✓ 核心洞察: {summary.get('core_insights', 'N/A')[:100]}...")
    
    # 步骤5: 生成报告
    print("\n5️⃣ 生成分析报告...")
    
    report = f"""
# 竞品调研报告：{basic_info.get('name', product_name)}

## 基础信息
- **产品名称**: {basic_info.get('name', 'N/A')}
- **一句话描述**: {basic_info.get('one_liner', 'N/A')}
- **产品类型**: {basic_info.get('type', 'N/A')}
- **团队规模**: {basic_info.get('team_size', 'N/A')}

## 产品分析
### Q1 - {q1.question}
{q1.answer}

### Q4 - {q4.question}
{q4.answer}

### Q5 - {q5.question}
{q5.answer}

## 复刻难度评估
**难度等级**: {evaluation.get('difficulty_level', 'N/A')}

**核心挑战**:
"""
    
    if evaluation.get('core_challenges'):
        for i, challenge in enumerate(evaluation['core_challenges'][:3], 1):
            report += f"\n{i}. {challenge}"
    
    report += f"""

## 执行摘要
**核心洞察**: {summary.get('core_insights', 'N/A')}

**增长模式**: {summary.get('growth_model', 'N/A')}

**独立开发者策略**: {summary.get('indie_developer_strategy', 'N/A')}
"""
    
    # 保存报告
    filename = f"{product_name.lower()}_analysis_demo.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"   ✓ 报告已保存到: {filename}")
    
    # 保存JSON结果
    json_filename = f"{product_name.lower()}_analysis_demo.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump({
            "basic_info": basic_info,
            "dimensions": {
                "Q1": {"question": q1.question, "answer": q1.answer},
                "Q4": {"question": q4.question, "answer": q4.answer},
                "Q5": {"question": q5.question, "answer": q5.answer}
            },
            "replication_eval": {
                "difficulty_level": evaluation.get('difficulty_level'),
                "core_challenges": evaluation.get('core_challenges', [])[:3]
            },
            "executive_summary": {
                "core_insights": summary.get('core_insights'),
                "growth_model": summary.get('growth_model'),
                "indie_developer_strategy": summary.get('indie_developer_strategy')
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"   ✓ JSON结果已保存到: {json_filename}")
    
    print("\n✅ 分析完成！")
    print("\n" + "=" * 50)
    print("💡 提示：这是一个简化的演示，完整分析会包含更多维度和深度搜索。")


def main():
    """主函数"""
    load_dotenv()
    
    # 检查环境
    from competitive_intelligence.utils.env_check import print_env_status
    is_valid = print_env_status()
    
    if not is_valid:
        print("\n请先设置必要的环境变量")
        return
    
    print("\n按回车键开始分析...")
    input()
    
    # 运行分析
    asyncio.run(analyze_product_complete())


if __name__ == "__main__":
    main()