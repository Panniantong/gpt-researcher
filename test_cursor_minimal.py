"""
最小化测试 Cursor 竞品调研 - 仅获取基础信息
"""
import asyncio
import os
from dotenv import load_dotenv
import sys
import logging

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 添加父目录到路径以便导入 gpt_researcher
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from competitive_intelligence import CompetitiveIntelligenceAgent
from gpt_researcher.actions.query_processing import get_search_results


async def test_search_only():
    """仅测试搜索功能"""
    print("=== 测试搜索功能 ===\n")
    
    # 初始化Agent获取retriever
    agent = CompetitiveIntelligenceAgent(
        query="Cursor",
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    # 测试搜索
    if agent._retriever:
        print(f"使用的检索器: {agent._retriever.__name__}")
        
        # 搜索 Cursor official website
        query = "Cursor official website"
        print(f"\n搜索查询: {query}")
        
        try:
            search_results = await get_search_results(
                query,
                agent._retriever,
                researcher=None
            )
            
            print(f"\n搜索结果数量: {len(search_results)}")
            
            # 打印前3个结果
            for i, result in enumerate(search_results[:3]):
                print(f"\n结果 {i+1}:")
                print(f"  URL: {result.get('href', result.get('url', 'N/A'))}")
                print(f"  标题: {result.get('title', 'N/A')}")
                print(f"  内容预览: {result.get('body', '')[:100]}...")
                
        except Exception as e:
            print(f"搜索错误: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("没有可用的检索器")


async def test_basic_info_only():
    """仅测试基础信息获取"""
    print("\n\n=== 测试基础信息获取 ===\n")
    
    agent = CompetitiveIntelligenceAgent(
        query="Cursor",
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    try:
        # 仅运行基础信息提取
        await agent._extract_basic_info()
        
        print("基础信息结果:")
        print(agent.results["basic_info"])
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    load_dotenv()
    
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY"):
        print("错误：缺少 OPENAI_API_KEY 环境变量")
        exit(1)
    
    print(f"TAVILY_API_KEY 设置: {'是' if os.getenv('TAVILY_API_KEY') else '否'}")
    
    # 运行测试
    asyncio.run(test_search_only())
    asyncio.run(test_basic_info_only())