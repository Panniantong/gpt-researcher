"""
竞品调研 Agent 使用示例
展示如何使用 CompetitiveIntelligenceAgent 进行产品竞品调研
"""
import asyncio
import os
from dotenv import load_dotenv
import sys

# 添加父目录到路径以便导入 gpt_researcher
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from competitive_intelligence import CompetitiveIntelligenceAgent


async def analyze_product_by_name():
    """通过产品名称进行竞品调研"""
    print("=== 通过产品名称进行竞品调研 ===\n")
    
    # 创建竞品调研Agent
    agent = CompetitiveIntelligenceAgent(
        query="Cursor",  # 可以改为任何产品名称
        llm_provider="openai",  # 或 "anthropic", "google" 等
        model="gpt-4o-mini"  # 或其他模型
    )
    
    # 运行调研
    report = await agent.run_research()
    
    # 打印报告
    print(report)
    
    # 保存结果
    await agent.save_results("cursor_competitive_analysis.json")
    
    return report


async def analyze_product_by_url():
    """通过产品URL进行竞品调研"""
    print("=== 通过产品URL进行竞品调研 ===\n")
    
    # 创建竞品调研Agent
    agent = CompetitiveIntelligenceAgent(
        query="v0",
        product_url="https://v0.dev",  # 直接提供产品URL
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    # 运行调研
    report = await agent.run_research()
    
    # 打印报告
    print(report)
    
    # 保存结果
    await agent.save_results("v0_competitive_analysis.json")
    
    return report


async def analyze_multiple_products():
    """批量分析多个产品"""
    print("=== 批量分析多个产品 ===\n")
    
    products = [
        {"name": "Perplexity", "url": "https://www.perplexity.ai"},
        {"name": "Claude", "url": "https://claude.ai"},
        {"name": "ChatGPT", "url": "https://chat.openai.com"}
    ]
    
    reports = []
    
    for product in products:
        print(f"\n正在分析 {product['name']}...")
        
        agent = CompetitiveIntelligenceAgent(
            query=product['name'],
            product_url=product.get('url'),
            llm_provider="openai",
            model="gpt-4o-mini"
        )
        
        try:
            report = await agent.run_research()
            reports.append({
                "product": product['name'],
                "report": report,
                "results": agent.results
            })
            
            # 保存单个产品的结果
            await agent.save_results(f"{product['name'].lower()}_analysis.json")
            
        except Exception as e:
            print(f"分析 {product['name']} 时出错：{str(e)}")
    
    return reports


async def analyze_with_custom_config():
    """使用自定义配置进行分析"""
    print("=== 使用自定义配置进行分析 ===\n")
    
    # 创建自定义配置文件（如果需要）
    config_content = """
# 自定义配置
llm_provider: "anthropic"
fast_llm_model: "claude-3-haiku-20240307"
smart_llm_model: "claude-3-opus-20240229"
temperature: 0.2
max_tokens: 3000
"""
    
    # 保存配置文件
    with open("custom_config.yaml", "w") as f:
        f.write(config_content)
    
    # 使用自定义配置创建Agent
    agent = CompetitiveIntelligenceAgent(
        query="Midjourney",
        config_path="custom_config.yaml"
    )
    
    # 运行调研
    report = await agent.run_research()
    
    print(report)
    
    # 清理配置文件
    os.remove("custom_config.yaml")
    
    return report


async def quick_analysis():
    """快速分析（使用便捷函数）"""
    print("=== 快速竞品分析 ===\n")
    
    from competitive_intelligence.agent import analyze_competitor
    
    # 直接调用便捷函数
    report = await analyze_competitor(
        query="Notion",
        product_url="https://www.notion.so",
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    print(report)
    
    return report


async def analyze_specific_aspects():
    """只分析特定方面"""
    print("=== 分析特定方面 ===\n")
    
    from competitive_intelligence.modules.basic_info import BasicInfoExtractor
    from competitive_intelligence.modules.marketing_intel import MarketingIntelAnalyzer
    
    product_url = "https://gamma.app"
    
    # 只获取基础信息
    print("1. 获取基础信息...")
    extractor = BasicInfoExtractor(llm_provider="openai", model="gpt-4o-mini")
    
    # 模拟获取网页内容（实际使用时需要真实的抓取）
    content = "<html><title>Gamma App</title><body>AI presentation tool...</body></html>"
    
    basic_info = await extractor.extract_from_content(content, product_url)
    print(f"产品名称：{basic_info.get('name')}")
    print(f"产品描述：{basic_info.get('one_liner')}")
    print(f"团队规模：{basic_info.get('team_size')}")
    
    # 只分析营销策略
    print("\n2. 分析营销策略...")
    marketing_analyzer = MarketingIntelAnalyzer(llm_provider="openai", model="gpt-4o-mini")
    
    # 这里需要先获取搜索结果（简化示例）
    search_results = [
        {
            "query": "Gamma app marketing strategy",
            "url": "https://example.com",
            "title": "How Gamma Grew to 1M Users",
            "content": "Gamma used content marketing and Product Hunt launch..."
        }
    ]
    
    marketing_analysis = await marketing_analyzer.analyze_marketing_strategy(
        "Gamma",
        search_results
    )
    
    print(f"主要渠道：{marketing_analysis.get('growth_channels', {}).get('primary_channels', [])}")
    
    return {
        "basic_info": basic_info,
        "marketing_analysis": marketing_analysis
    }


def main():
    """主函数：选择要运行的示例"""
    load_dotenv()  # 加载环境变量
    
    # 环境检查
    from competitive_intelligence.utils.env_check import print_env_status
    if not print_env_status():
        print("\n请先设置必要的环境变量")
        return
    
    print("\n竞品调研 Agent 示例程序")
    print("========================\n")
    print("请选择要运行的示例：")
    print("1. 通过产品名称分析")
    print("2. 通过产品URL分析")
    print("3. 批量分析多个产品")
    print("4. 使用自定义配置分析")
    print("5. 快速分析（便捷函数）")
    print("6. 只分析特定方面")
    print("0. 退出")
    
    choice = input("\n请输入选项 (0-6): ").strip()
    
    if choice == "0":
        print("退出程序")
        return
    
    # 运行选择的示例
    examples = {
        "1": analyze_product_by_name,
        "2": analyze_product_by_url,
        "3": analyze_multiple_products,
        "4": analyze_with_custom_config,
        "5": quick_analysis,
        "6": analyze_specific_aspects
    }
    
    if choice in examples:
        print(f"\n开始运行示例 {choice}...\n")
        asyncio.run(examples[choice]())
    else:
        print("无效选项，请重新运行程序")


if __name__ == "__main__":
    # 确保已设置必要的环境变量
    required_env_vars = ["OPENAI_API_KEY"]  # 或其他LLM的API密钥
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("错误：缺少必要的环境变量")
        print("请在 .env 文件中设置以下变量：")
        for var in missing_vars:
            print(f"  {var}=your_api_key_here")
        print("\n或者直接设置环境变量：")
        for var in missing_vars:
            print(f"  export {var}=your_api_key_here")
        exit(1)
    
    main()