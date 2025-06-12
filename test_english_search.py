#!/usr/bin/env python3
"""
Test script to verify English search query generation
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpt_researcher import GPTResearcher
from gpt_researcher.config.config import Config

async def test_chinese_query():
    """Test with Chinese query to verify it gets translated to English"""
    # Load environment variables
    load_dotenv()
    
    # Test queries
    test_queries = [
        "Tavily 创始人背景和专业经验",
        "分析Tavily的产品功能迭代历史",
        "Tavily用户增长和营销策略研究"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing query: {query}")
        print(f"{'='*60}")
        
        try:
            # Create researcher instance
            researcher = GPTResearcher(
                query=query,
                report_type="research_report",
                verbose=True
            )
            
            # Get configuration
            cfg = Config()
            
            # Test sub-query generation
            from gpt_researcher.actions.query_processing import generate_sub_queries
            
            sub_queries = await generate_sub_queries(
                query=query,
                parent_query="",
                report_type="research_report",
                context=[],
                cfg=cfg
            )
            
            print(f"\nGenerated sub-queries:")
            for i, sq in enumerate(sub_queries, 1):
                print(f"{i}. {sq}")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chinese_query())