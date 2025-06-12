"""
调试 Cursor 竞品调研 - 查看 LLM 响应
"""
import asyncio
import os
from dotenv import load_dotenv
import sys
import json

# 添加父目录到路径以便导入 gpt_researcher
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from competitive_intelligence.utils.llm_helper import get_llm_response
from competitive_intelligence.prompts.competitive_prompts import BASIC_INFO_PROMPT


async def test_llm_extraction():
    """测试 LLM 提取信息"""
    print("=== 测试 LLM 信息提取 ===\n")
    
    # 模拟的 Cursor 网页内容
    content = """
    Cursor – Welcome to Cursor
    Cursor is an AI code editor used by millions of engineers. It is powered by a series of custom models that generate more code than almost any LLMs in the world.
    
    Get Started
    If you're new to Cursor, you can get started using the guides below.
    Introduction
    Learn about Cursor's core features and concepts.
    
    The Editor
    Cursor has a number of core features that will seamlessly integrate with your workflow.
    Tab
    Tab, Tab, Tab. Powered by our state-of-the-art model series, Tab predicts your next series of edits.
    Agent
    Your AI pair programmer for complex code changes. Make large-scale edits with context control and automatic fixes.
    Cmd-K
    Quick inline code editing and generation. Perfect for making precise changes without breaking your flow.
    
    How do I get started?
    You can download Cursor from the Cursor website for your platform of choice.
    """
    
    # 构建提示词
    prompt = BASIC_INFO_PROMPT.format(content=content)
    
    print("提示词:")
    print("-" * 80)
    print(prompt[:500] + "...")
    print("-" * 80)
    
    # 调用 LLM
    response = await get_llm_response(
        prompt,
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    print("\nLLM 原始响应:")
    print("-" * 80)
    print(response)
    print("-" * 80)
    
    # 尝试解析 JSON
    try:
        import re
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            info = json.loads(json_match.group())
            print("\n解析后的 JSON:")
            print(json.dumps(info, indent=2, ensure_ascii=False))
        else:
            print("\n无法找到 JSON 格式的响应")
    except json.JSONDecodeError as e:
        print(f"\nJSON 解析错误: {e}")


if __name__ == "__main__":
    load_dotenv()
    
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY"):
        print("错误：缺少 OPENAI_API_KEY 环境变量")
        exit(1)
    
    # 运行测试
    asyncio.run(test_llm_extraction())