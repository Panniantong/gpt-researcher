"""
Test script for Deep Competitive Intelligence Agent
测试深度竞品情报研究代理
"""

import asyncio
import os
from dotenv import load_dotenv

# 添加项目根目录到Python路径
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config


def progress_callback(progress):
    """进度回调函数"""
    if hasattr(progress, 'current_depth'):
        print(f"📊 深度研究进度: 第 {progress.current_depth}/{progress.total_depth} 层, "
              f"广度 {progress.current_breadth}/{progress.total_breadth}")
    if hasattr(progress, 'current_query'):
        print(f"   🔍 当前查询: {progress.current_query}")


async def test_deep_competitive_intelligence():
    """
    测试深度竞品情报研究功能
    """
    # 加载环境变量
    load_dotenv()
    
    # 配置研究参数
    product_name = "Cursor"  # 测试产品
    product_url = "https://cursor.sh"
    
    # 创建配置
    config = Config()
    
    # 可选：配置深度研究参数
    config.deep_research_breadth = 3  # 每层搜索广度
    config.deep_research_depth = 2    # 搜索深度
    config.deep_research_concurrency = 2  # 并发限制
    
    print(f"🚀 开始对 {product_name} 进行深度竞品情报研究...")
    print("=" * 60)
    print("📌 深度研究配置:")
    print(f"   - 搜索广度: {config.deep_research_breadth}")
    print(f"   - 搜索深度: {config.deep_research_depth}")
    print(f"   - 并发限制: {config.deep_research_concurrency}")
    print("=" * 60)
    
    try:
        # 创建竞品情报代理
        agent = CompetitiveIntelligenceAgent(
            product_name=product_name,
            product_url=product_url,
            config=config
        )
        
        # 设置详细模式
        agent.verbose = True
        
        # 执行深度研究
        result = await agent.conduct_research(on_progress=progress_callback)
        
        # 输出结果
        print("\n✅ 深度研究完成！\n")
        print("=" * 60)
        
        # 显示验证结果
        print("\n📋 核对表验证结果:")
        for check, passed in result["validation"].items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check}")
        
        # 显示成本
        if "total_costs" in result:
            print(f"\n💰 总研究成本: ${result['total_costs']:.2f}")
        
        # 显示收集的来源数量
        print(f"\n📚 深度研究来源: {len(result['sources'])} 个")
        print("\n前5个来源:")
        for i, source in enumerate(result['sources'][:5], 1):
            print(f"  {i}. {source}")
        
        # 保存报告
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{output_dir}/{product_name.lower()}_deep_competitive_intelligence_{result['timestamp'][:10]}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result["report"])
        
        print(f"\n💾 深度研究报告已保存至: {filename}")
        
        # 显示报告摘要（前500字符）
        print("\n📄 报告摘要:")
        print("=" * 60)
        print(result["report"][:500] + "...")
        
    except Exception as e:
        print(f"\n❌ 深度研究过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


async def test_basic_vs_deep():
    """
    对比测试：基础研究 vs 深度研究
    """
    print("🔬 对比测试：基础研究 vs 深度研究")
    print("=" * 60)
    
    product_name = "Windsurf"
    
    # 1. 基础研究（禁用深度研究）
    print("\n1️⃣ 执行基础研究...")
    config1 = Config()
    config1.deep_research_breadth = 1
    config1.deep_research_depth = 1
    
    agent1 = CompetitiveIntelligenceAgent(product_name, config=config1)
    result1 = await agent1.conduct_research()
    
    print(f"   - 来源数量: {len(result1['sources'])}")
    print(f"   - 成本: ${result1.get('total_costs', 0):.2f}")
    
    # 2. 深度研究
    print("\n2️⃣ 执行深度研究...")
    config2 = Config()
    config2.deep_research_breadth = 3
    config2.deep_research_depth = 2
    
    agent2 = CompetitiveIntelligenceAgent(product_name, config=config2)
    result2 = await agent2.conduct_research()
    
    print(f"   - 来源数量: {len(result2['sources'])}")
    print(f"   - 成本: ${result2.get('total_costs', 0):.2f}")
    
    # 对比结果
    print("\n📊 对比分析:")
    print(f"   - 来源增加: {len(result2['sources']) - len(result1['sources'])} 个")
    print(f"   - 成本增加: ${(result2.get('total_costs', 0) - result1.get('total_costs', 0)):.2f}")
    
    # 检查信息完整性提升
    validation_improvement = 0
    for check in result1['validation']:
        if not result1['validation'][check] and result2['validation'][check]:
            validation_improvement += 1
    
    print(f"   - 验证改善: {validation_improvement} 项")


def main():
    """
    主函数
    """
    print("🤖 深度竞品情报研究代理测试\n")
    
    # 直接运行深度研究测试
    asyncio.run(test_deep_competitive_intelligence())


if __name__ == "__main__":
    main()