"""
竞品调研 Agent 演示脚本
展示如何使用该工具进行产品竞品分析
"""
import asyncio
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from competitive_intelligence import CompetitiveIntelligenceAgent


async def demo_competitive_analysis():
    """演示竞品分析功能"""
    print("🔍 竞品调研 Agent - 演示")
    print("=" * 50)
    
    # 选择要分析的产品
    product_name = "Cursor"  # 可以改为其他产品
    product_url = "https://cursor.sh"
    
    print(f"\n📊 正在分析产品: {product_name}")
    print(f"🌐 产品网址: {product_url}")
    print("\n⏳ 这可能需要2-3分钟，请耐心等待...\n")
    
    # 创建 Agent
    agent = CompetitiveIntelligenceAgent(
        query=product_name,
        product_url=product_url,
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    try:
        # 运行调研
        report = await agent.run_research()
        
        # 保存报告
        filename = f"{product_name.lower().replace(' ', '_')}_analysis.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ 调研完成！")
        print(f"📄 完整报告已保存到: {filename}")
        
        # 显示摘要
        print("\n" + "=" * 50)
        print("📋 执行摘要")
        print("=" * 50)
        
        summary = agent.results.get("executive_summary", {})
        
        if summary.get("core_insights"):
            print(f"\n🎯 核心洞察:\n{summary['core_insights']}")
        
        if summary.get("growth_model"):
            print(f"\n🚀 增长模式:\n{summary['growth_model']}")
        
        if summary.get("indie_developer_strategy"):
            print(f"\n⭐ 独立开发者策略:\n{summary['indie_developer_strategy']}")
        
        # 显示复刻难度
        replication = agent.results.get("replication_eval", {})
        if replication.get("difficulty_level"):
            print(f"\n💡 复刻难度: {replication['difficulty_level']}")
        
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()


async def quick_analysis_demo():
    """快速分析演示（只分析部分维度）"""
    print("\n⚡ 快速分析模式")
    print("=" * 50)
    
    from competitive_intelligence.modules.basic_info import BasicInfoExtractor
    from competitive_intelligence.modules.replication_eval import ReplicationEvaluator
    
    product_url = "https://v0.dev"
    
    print(f"分析产品: {product_url}")
    
    # 1. 获取基础信息
    print("\n1️⃣ 获取基础信息...")
    extractor = BasicInfoExtractor("openai", "gpt-4o-mini")
    
    # 模拟抓取内容（实际使用时需要真实抓取）
    mock_content = """
    <html>
    <head>
        <title>v0 by Vercel - AI-Powered UI Generation</title>
        <meta name="description" content="Generate UI with simple text prompts. Copy, paste, ship.">
    </head>
    <body>
        <h1>v0</h1>
        <p>Chat with v0. Generate UI with simple text prompts. Copy, paste, ship.</p>
        <p>Built by Vercel</p>
    </body>
    </html>
    """
    
    basic_info = await extractor.extract_from_content(mock_content, product_url)
    
    print(f"  产品名称: {basic_info.get('name', 'N/A')}")
    print(f"  产品描述: {basic_info.get('one_liner', 'N/A')}")
    print(f"  团队规模: {basic_info.get('team_size', 'N/A')}")
    
    # 2. 评估复刻难度
    print("\n2️⃣ 评估复刻难度...")
    evaluator = ReplicationEvaluator("openai", "gpt-4o-mini")
    
    evaluation = await evaluator.evaluate_replication_difficulty(
        basic_info,
        tech_architecture="使用 AI 模型生成 React/Tailwind 代码"
    )
    
    print(f"  难度等级: {evaluation.get('difficulty_level', 'N/A')}")
    print(f"  整体评估: {evaluation.get('overall_assessment', 'N/A')[:200]}...")
    
    print("\n✅ 快速分析完成！")


def main():
    """主函数"""
    load_dotenv()
    
    # 检查 API 密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误: 请设置 OPENAI_API_KEY 环境变量")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print("选择演示模式:")
    print("1. 完整竞品分析（2-3分钟）")
    print("2. 快速分析演示（30秒）")
    
    choice = input("\n请选择 (1 或 2): ").strip()
    
    if choice == "1":
        asyncio.run(demo_competitive_analysis())
    elif choice == "2":
        asyncio.run(quick_analysis_demo())
    else:
        print("无效选择")


if __name__ == "__main__":
    main()