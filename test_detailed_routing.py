#!/usr/bin/env python3
"""
详细测试不同模型的API路由
"""

from dotenv import load_dotenv
import os
import asyncio

# 加载环境变量
load_dotenv()

from gpt_researcher.utils.llm import create_chat_completion

async def test_model_routing(model_name, expected_api):
    """测试特定模型的路由"""
    print(f"\n🧪 测试模型: {model_name}")
    print(f"预期使用: {expected_api}")
    
    test_messages = [
        {"role": "user", "content": "请简单回复'测试成功'"}
    ]
    
    try:
        response = await create_chat_completion(
            model=model_name,
            messages=test_messages,
            temperature=0.1,
            max_tokens=50,
            llm_provider="openai",
            stream=False,
            websocket=None
        )
        
        if "API调用失败" in response or "响应生成失败" in response:
            print(f"❌ 模型 {model_name} 调用失败")
            print(f"错误响应: {response[:100]}...")
        else:
            print(f"✅ 模型 {model_name} 调用成功")
            print(f"响应: {response[:50]}...")
            
    except Exception as e:
        print(f"❌ 模型 {model_name} 出现异常: {str(e)}")

async def main():
    print("=== 详细API路由测试 ===")
    
    # 测试不同类型的模型
    test_cases = [
        ("o3-mini", "官方OpenAI API"),
        ("o3", "官方OpenAI API"), 
        ("o3-2025-04-16", "官方OpenAI API"),
        ("gpt-4o-mini", "逆向API"),
        ("gpt-4", "逆向API"),
        ("gpt-3.5-turbo", "逆向API")
    ]
    
    for model, expected_api in test_cases:
        await test_model_routing(model, expected_api)
        await asyncio.sleep(1)  # 避免请求过快

    print("\n=== 检查当前项目配置 ===")
    from gpt_researcher.config.config import Config
    cfg = Config()
    print(f"当前SMART_LLM配置: {cfg.smart_llm}")
    print(f"解析后的模型: {cfg.smart_llm_model}")
    print(f"解析后的提供商: {cfg.smart_llm_provider}")

if __name__ == "__main__":
    asyncio.run(main())