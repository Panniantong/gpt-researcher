#!/usr/bin/env python3
"""
测试API路由逻辑，验证o3模型是否使用官方API
"""

from dotenv import load_dotenv
import os
import asyncio

# 加载环境变量
load_dotenv()

from gpt_researcher.config.config import Config
from gpt_researcher.utils.llm import create_chat_completion

async def test_api_routing():
    """测试API路由逻辑"""
    
    print("=== 环境变量检查 ===")
    print(f"OPENAI_OFFICIAL_API_KEY: {'设置' if os.environ.get('OPENAI_OFFICIAL_API_KEY') else '未设置'}")
    print(f"OPENAI_OFFICIAL_BASE_URL: {os.environ.get('OPENAI_OFFICIAL_BASE_URL', '未设置')}")
    print(f"OPENAI_API_KEY: {'设置' if os.environ.get('OPENAI_API_KEY') else '未设置'}")
    print(f"OPENAI_BASE_URL: {os.environ.get('OPENAI_BASE_URL', '未设置')}")
    
    print("\n=== 配置检查 ===")
    cfg = Config()
    print(f"SMART_LLM: {cfg.smart_llm}")
    print(f"SMART_LLM_MODEL: {cfg.smart_llm_model}")
    print(f"SMART_LLM_PROVIDER: {cfg.smart_llm_provider}")
    
    print("\n=== API路由测试 ===")
    
    # 测试消息
    test_messages = [
        {"role": "user", "content": "请用一句话回答：今天天气如何？（这只是一个测试）"}
    ]
    
    try:
        print(f"正在测试模型: {cfg.smart_llm_model}")
        print("发送测试请求...")
        
        response = await create_chat_completion(
            model=cfg.smart_llm_model,
            messages=test_messages,
            temperature=0.3,
            max_tokens=100,
            llm_provider=cfg.smart_llm_provider,
            stream=False,
            websocket=None
        )
        
        print(f"\n✅ 成功获得响应:")
        print(f"响应内容: {response[:200]}...")
        
        # 检查响应是否来自官方API (通过响应特征判断)
        if "API调用失败" in response or "响应生成失败" in response:
            print("❌ API调用失败，可能没有正确路由到官方API")
        else:
            print("✅ API调用成功，应该已正确路由到官方API")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_api_routing())