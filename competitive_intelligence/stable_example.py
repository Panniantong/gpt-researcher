"""
竞品调研 Agent - 稳定版示例
包含完善的错误处理和超时控制
"""
import asyncio
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from competitive_intelligence import CompetitiveIntelligenceAgent
from competitive_intelligence.utils.env_check import print_env_status


async def analyze_with_timeout(product_name, product_url=None, timeout=60):
    """
    带超时控制的产品分析
    
    Args:
        product_name: 产品名称
        product_url: 产品URL（可选）
        timeout: 超时时间（秒）
    """
    print(f"\n📊 开始分析: {product_name}")
    if product_url:
        print(f"🌐 产品URL: {product_url}")
    print(f"⏱️  超时设置: {timeout}秒\n")
    
    # 创建Agent
    agent = CompetitiveIntelligenceAgent(
        query=product_name,
        product_url=product_url,
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    try:
        # 使用超时控制
        report = await asyncio.wait_for(
            agent.run_research(),
            timeout=timeout
        )
        
        # 保存结果
        filename = f"{product_name.lower().replace(' ', '_')}_report.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ 分析完成！报告已保存到: {filename}")
        
        # 显示摘要
        if agent.results.get("executive_summary"):
            summary = agent.results["executive_summary"]
            print("\n📋 执行摘要:")
            print(f"  核心洞察: {summary.get('core_insights', 'N/A')[:100]}...")
        
        return True
        
    except asyncio.TimeoutError:
        print(f"\n⏱️  分析超时（{timeout}秒）")
        print("💡 建议：增加超时时间或使用快速分析模式")
        return False
        
    except Exception as e:
        print(f"\n❌ 分析失败: {str(e)}")
        return False


async def fast_analysis_mode(product_name, product_url):
    """
    快速分析模式 - 跳过耗时的搜索操作
    """
    print(f"\n⚡ 快速分析模式: {product_name}")
    print("（跳过深度搜索，只进行基础分析）\n")
    
    # 创建Agent
    agent = CompetitiveIntelligenceAgent(
        query=product_name,
        product_url=product_url,
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    try:
        # 1. 基础信息
        print("1️⃣ 提取基础信息...")
        await agent._extract_basic_info()
        
        info = agent.results.get("basic_info", {})
        print(f"   ✓ 产品名称: {info.get('name', product_name)}")
        print(f"   ✓ 产品描述: {info.get('one_liner', 'N/A')}")
        print(f"   ✓ 团队规模: {info.get('team_size', 'N/A')}")
        
        # 2. 快速八维分析（只分析不需要搜索的维度）
        print("\n2️⃣ 快速产品分析...")
        
        from competitive_intelligence.modules.eight_dimensions import EightDimensionsAnalyzer
        analyzer = EightDimensionsAnalyzer("openai", "gpt-4o-mini")
        
        # 如果没有获取到基础信息，使用默认值
        if not info.get('name'):
            info = {
                'name': product_name,
                'one_liner': f'{product_name} - 产品描述待补充',
                'type': '待分类',
                'url': product_url or f'https://{product_name.lower()}.com'
            }
        
        # Q1: One-sentence Pitch
        q1 = await analyzer._analyze_q1(info)
        print(f"   ✓ 核心价值: {q1.answer}")
        
        # Q4: Who-When-Action  
        q4 = await analyzer._analyze_q4(info)
        print(f"   ✓ 使用场景: {q4.answer}")
        
        # 3. 复刻难度评估
        print("\n3️⃣ 评估复刻难度...")
        
        from competitive_intelligence.modules.replication_eval import ReplicationEvaluator
        evaluator = ReplicationEvaluator("openai", "gpt-4o-mini")
        
        evaluation = await evaluator.evaluate_replication_difficulty(info)
        print(f"   ✓ 难度等级: {evaluation.get('difficulty_level', 'N/A')}")
        
        # 生成简报
        report = f"""
# {product_name} - 快速竞品分析

## 基础信息
- 产品名称: {info.get('name', product_name)}
- 产品描述: {info.get('one_liner', 'N/A')}
- 团队规模: {info.get('team_size', 'N/A')}

## 产品定位
- 核心价值: {q1.answer}
- 使用场景: {q4.answer}

## 复刻评估
- 难度等级: {evaluation.get('difficulty_level', 'N/A')}

---
*注：这是快速分析模式，如需深度分析请使用完整模式*
"""
        
        filename = f"{product_name.lower().replace(' ', '_')}_quick_analysis.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ 快速分析完成！报告已保存到: {filename}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 快速分析失败: {str(e)}")
        return False


async def batch_analysis_with_fallback():
    """批量分析多个产品，失败时自动降级到快速模式"""
    products = [
        {"name": "Cursor", "url": "https://cursor.sh", "timeout": 30},
        {"name": "v0", "url": "https://v0.dev", "timeout": 30},
        {"name": "Perplexity", "url": "https://www.perplexity.ai", "timeout": 30}
    ]
    
    print("📦 批量分析模式")
    print(f"将分析 {len(products)} 个产品\n")
    
    results = []
    
    for product in products:
        print(f"\n{'='*50}")
        print(f"分析第 {products.index(product)+1}/{len(products)} 个产品")
        
        # 先尝试完整分析
        success = await analyze_with_timeout(
            product["name"], 
            product["url"],
            product["timeout"]
        )
        
        if not success:
            # 如果失败，降级到快速分析
            print("\n🔄 切换到快速分析模式...")
            success = await fast_analysis_mode(
                product["name"],
                product["url"]
            )
        
        results.append({
            "product": product["name"],
            "success": success,
            "mode": "完整分析" if success else "快速分析"
        })
        
        # 短暂休息，避免API限制
        await asyncio.sleep(2)
    
    # 打印总结
    print(f"\n{'='*50}")
    print("📊 批量分析总结:")
    for result in results:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['product']} - {result['mode']}")


def main():
    """主函数"""
    load_dotenv()
    
    # 检查环境
    if not print_env_status():
        print("\n请设置必要的环境变量后重试")
        return
    
    print("\n选择分析模式:")
    print("1. 单个产品分析（带超时控制）")
    print("2. 快速分析模式（跳过搜索）")
    print("3. 批量分析（自动降级）")
    print("0. 退出")
    
    choice = input("\n请选择 (0-3): ").strip()
    
    if choice == "1":
        product = input("请输入产品名称: ").strip()
        url = input("请输入产品URL（可选，直接回车跳过）: ").strip()
        timeout = input("设置超时时间（秒，默认60）: ").strip()
        
        asyncio.run(analyze_with_timeout(
            product,
            url if url else None,
            int(timeout) if timeout else 60
        ))
        
    elif choice == "2":
        product = input("请输入产品名称: ").strip()
        url = input("请输入产品URL（可选，直接回车跳过）: ").strip()
        
        asyncio.run(fast_analysis_mode(
            product,
            url if url else None
        ))
        
    elif choice == "3":
        asyncio.run(batch_analysis_with_fallback())
        
    elif choice == "0":
        print("退出程序")
    else:
        print("无效选择")


if __name__ == "__main__":
    main()