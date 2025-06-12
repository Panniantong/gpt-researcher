"""
测试通过URL分析产品的功能
"""
import asyncio
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from competitive_intelligence import CompetitiveIntelligenceAgent


async def test_url_analysis():
    """测试通过URL分析"""
    print("=== 测试通过URL分析产品 ===\n")
    
    # 测试一个简单的产品
    product_url = "https://v0.dev"
    
    print(f"分析产品: {product_url}")
    print("注意：这个测试会跳过搜索功能，只测试基础信息提取\n")
    
    # 创建Agent
    agent = CompetitiveIntelligenceAgent(
        query="v0",
        product_url=product_url,
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    # 只测试基础信息提取
    print("1. 提取基础信息...")
    try:
        await agent._extract_basic_info()
        
        info = agent.results.get("basic_info", {})
        print("\n提取结果:")
        for key, value in info.items():
            print(f"  {key}: {value}")
            
        # 如果基础信息成功，尝试快速的八维分析（不需要搜索的部分）
        print("\n2. 测试八维分析（仅本地分析部分）...")
        
        # 分析不需要搜索的维度
        from competitive_intelligence.modules.eight_dimensions import EightDimensionsAnalyzer
        analyzer = EightDimensionsAnalyzer("openai", "gpt-4o-mini")
        
        # Q1: One-sentence Pitch
        q1_result = await analyzer._analyze_q1(info)
        print(f"\nQ1 - {q1_result.question}: {q1_result.answer}")
        
        # Q4: Who-When-Action
        q4_result = await analyzer._analyze_q4(info)
        print(f"\nQ4 - {q4_result.question}: {q4_result.answer}")
        
        # Q5: Pain & Pain-level
        q5_result = await analyzer._analyze_q5(info)
        print(f"\nQ5 - {q5_result.question}: {q5_result.answer}")
        
        print("\n✅ 测试完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


async def test_quick_analysis_no_search():
    """快速分析（不使用搜索）"""
    print("\n=== 快速分析模式（无搜索）===\n")
    
    from competitive_intelligence.modules.basic_info import BasicInfoExtractor
    from competitive_intelligence.modules.replication_eval import ReplicationEvaluator
    
    # 模拟已知的产品信息
    product_info = {
        "name": "Cursor",
        "one_liner": "The AI-first code editor",
        "type": "AI开发工具",
        "team_size": "小团队(2-5人)",
        "url": "https://cursor.sh"
    }
    
    print("产品信息:")
    for key, value in product_info.items():
        print(f"  {key}: {value}")
    
    # 评估复刻难度
    print("\n评估复刻难度...")
    evaluator = ReplicationEvaluator("openai", "gpt-4o-mini")
    
    evaluation = await evaluator.evaluate_replication_difficulty(
        product_info,
        tech_architecture="基于VSCode的AI集成开发环境，深度集成GPT-4等模型"
    )
    
    print(f"\n难度等级: {evaluation.get('difficulty_level')}")
    
    if evaluation.get("core_challenges"):
        print("\n核心挑战:")
        for i, challenge in enumerate(evaluation["core_challenges"][:3], 1):
            print(f"  {i}. {challenge}")
    
    print("\n✅ 分析完成！")


def main():
    """主函数"""
    load_dotenv()
    
    # 检查环境
    from competitive_intelligence.utils.env_check import print_env_status
    print_env_status()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ 请设置 OPENAI_API_KEY")
        return
    
    print("\n选择测试模式:")
    print("1. 测试URL分析（需要网络）")
    print("2. 快速本地分析（无需网络）")
    
    choice = input("\n请选择 (1-2): ").strip()
    
    if choice == "1":
        asyncio.run(test_url_analysis())
    elif choice == "2":
        asyncio.run(test_quick_analysis_no_search())
    else:
        print("无效选择")


if __name__ == "__main__":
    main()