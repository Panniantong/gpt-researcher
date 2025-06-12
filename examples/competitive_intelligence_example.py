"""
Example of using CompetitiveIntelligenceAgent
竞品情报研究代理使用示例
"""

import asyncio
import os
from dotenv import load_dotenv

# 添加项目根目录到Python路径
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config


async def run_competitive_intelligence_research():
    """
    运行竞品情报研究示例
    """
    # 加载环境变量
    load_dotenv()
    
    # 配置研究参数
    product_name = "gadget"  # 可以换成任何你想研究的产品
    product_url = "https://gadget.dev"  # 可选，提供更准确的信息
    
    # 创建配置
    config = Config()
    
    # 可选：自定义配置
    # config.llm_provider = "openai"  # 或 "anthropic", "google", 等
    # config.fast_llm_model = "gpt-3.5-turbo-16k"
    # config.smart_llm_model = "gpt-4"
    
    print(f"🔍 开始对 {product_name} 进行深度竞品情报研究...\n")
    print("=" * 60)
    
    try:
        # 创建竞品情报代理
        agent = CompetitiveIntelligenceAgent(
            product_name=product_name,
            product_url=product_url,
            config=config
        )
        
        # 执行研究
        result = await agent.conduct_research()
        
        # 输出结果
        print("\n📊 研究完成！\n")
        print("=" * 60)
        
        # 显示验证结果
        print("\n✅ 核对表验证结果:")
        for check, passed in result["validation"].items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check}")
        
        # 显示报告
        print("\n📄 完整报告:")
        print("=" * 60)
        print(result["report"])
        
        # 显示收集的来源数量
        print(f"\n📌 共收集 {len(result['sources'])} 个信息来源")
        
        # 可选：保存报告到文件
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{output_dir}/{product_name.lower()}_competitive_intelligence_{result['timestamp'][:10]}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result["report"])
        
        print(f"\n💾 报告已保存至: {filename}")
        
    except Exception as e:
        print(f"\n❌ 研究过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


async def run_batch_research():
    """
    批量研究多个产品的示例
    """
    products = [
        {"name": "Cursor", "url": "https://cursor.sh"},
        {"name": "GitHub Copilot", "url": "https://github.com/features/copilot"},
        {"name": "Codeium", "url": "https://codeium.com"}
    ]
    
    print("🚀 开始批量竞品情报研究...\n")
    
    # 创建配置
    config = Config()
    
    # 创建所有研究任务
    tasks = []
    for product in products:
        agent = CompetitiveIntelligenceAgent(
            product_name=product["name"],
            product_url=product.get("url"),
            config=config
        )
        tasks.append(agent.conduct_research())
    
    # 并行执行所有研究
    results = await asyncio.gather(*tasks)
    
    # 输出结果摘要
    print("\n📊 批量研究完成！摘要如下：\n")
    for i, (product, result) in enumerate(zip(products, results)):
        print(f"{i+1}. {product['name']}:")
        validation = result["validation"]
        passed = sum(1 for v in validation.values() if v)
        total = len(validation)
        print(f"   - 验证通过率: {passed}/{total} ({passed/total*100:.1f}%)")
        print(f"   - 信息来源数: {len(result['sources'])}")
        print()


def main():
    """
    主函数
    """
    print("🤖 竞品情报研究代理示例\n")
    print("选择运行模式:")
    print("1. 单个产品深度研究")
    print("2. 批量产品研究")
    
    choice = input("\n请输入选择 (1/2): ").strip()
    
    if choice == "1":
        # 可以让用户输入产品信息
        product_name = input("请输入产品名称 (默认: Cursor): ").strip() or "Cursor"
        product_url = input("请输入产品URL (可选): ").strip() or None
        
        # 修改运行的产品
        import competitive_intelligence_example
        competitive_intelligence_example.product_name = product_name
        if product_url:
            competitive_intelligence_example.product_url = product_url
        
        asyncio.run(run_competitive_intelligence_research())
    
    elif choice == "2":
        asyncio.run(run_batch_research())
    
    else:
        print("无效选择")


if __name__ == "__main__":
    main()