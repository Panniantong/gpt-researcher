"""
最小化测试脚本 - 只测试基础功能
"""
import asyncio
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from competitive_intelligence.modules.basic_info import BasicInfoExtractor


async def test_basic_extraction():
    """只测试基础信息提取"""
    print("=== 测试基础信息提取 ===\n")
    
    # 模拟HTML内容
    html_content = """
    <html>
    <head>
        <title>ChatGPT - OpenAI</title>
        <meta name="description" content="ChatGPT is an AI-powered language model developed by OpenAI, capable of generating human-like text based on context and past conversations.">
    </head>
    <body>
        <h1>ChatGPT</h1>
        <p>AI assistant that helps with writing, analysis, and problem-solving</p>
        <p>Built by OpenAI team of researchers and engineers</p>
    </body>
    </html>
    """
    
    # 创建提取器
    extractor = BasicInfoExtractor(
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    # 提取信息
    try:
        info = await extractor.extract_from_content(html_content, "https://chat.openai.com")
        
        print("提取结果：")
        for key, value in info.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY 环境变量")
        exit(1)
    
    asyncio.run(test_basic_extraction())