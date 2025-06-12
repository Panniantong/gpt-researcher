"""
测试实际运行时的问题
"""
import asyncio
import os
from dotenv import load_dotenv
import sys

# 添加父目录到路径以便导入 gpt_researcher
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from competitive_intelligence.modules.basic_info import BasicInfoExtractor
from gpt_researcher.scraper import Scraper
from gpt_researcher.utils.workers import WorkerPool
from gpt_researcher.config import Config


async def test_real_scraping():
    """测试实际的网页抓取和信息提取"""
    print("=== 测试实际网页抓取 ===\n")
    
    # 初始化配置
    config = Config()
    worker_pool = WorkerPool(max_workers=5)
    
    # 抓取 Cursor 文档页面
    url = "https://docs.cursor.com/welcome"
    
    try:
        scraper = Scraper(
            [url], 
            user_agent=config.user_agent,
            scraper=config.scraper,
            worker_pool=worker_pool
        )
        
        results = await asyncio.wait_for(
            scraper.run(),
            timeout=10
        )
        
        if results and len(results) > 0:
            content = results[0].get('raw_content', '')
            print(f"抓取内容长度: {len(content)} 字符")
            print(f"内容预览:\n{content[:500]}...")
            
            # 使用 BasicInfoExtractor 提取信息
            extractor = BasicInfoExtractor("openai", "gpt-4o-mini")
            info = await extractor.extract_from_content(content, url)
            
            print(f"\n提取的信息:")
            print(info)
            
            # 验证信息
            validated = extractor.validate_info(info)
            print(f"\n验证后的信息:")
            print(validated)
            
        else:
            print("抓取失败：没有返回结果")
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


async def test_cursor_main_site():
    """测试抓取 Cursor 主站"""
    print("\n\n=== 测试抓取 Cursor 主站 ===\n")
    
    # 初始化配置
    config = Config()
    worker_pool = WorkerPool(max_workers=5)
    
    # 抓取 Cursor 主站
    url = "https://www.cursor.com"
    
    try:
        scraper = Scraper(
            [url], 
            user_agent=config.user_agent,
            scraper=config.scraper,
            worker_pool=worker_pool
        )
        
        results = await asyncio.wait_for(
            scraper.run(),
            timeout=10
        )
        
        if results and len(results) > 0:
            content = results[0].get('raw_content', '')
            print(f"抓取内容长度: {len(content)} 字符")
            print(f"内容预览:\n{content[:500]}...")
            
            # 使用 BasicInfoExtractor 提取信息
            extractor = BasicInfoExtractor("openai", "gpt-4o-mini")
            info = await extractor.extract_from_content(content, url)
            
            print(f"\n提取的信息:")
            print(info)
            
        else:
            print("抓取失败：没有返回结果")
            
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
    
    # 运行测试
    asyncio.run(test_real_scraping())
    asyncio.run(test_cursor_main_site())