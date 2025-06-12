"""
LLM辅助函数
提供简化的LLM调用接口
"""
from typing import List, Dict, Any
from gpt_researcher.utils.llm import get_llm


async def get_llm_response(
    prompt: str, 
    llm_provider: str = None, 
    model: str = None,
    temperature: float = 0.1
) -> str:
    """
    获取LLM响应的简化接口
    
    Args:
        prompt: 提示词
        llm_provider: LLM提供商
        model: 模型名称
        temperature: 温度参数
        
    Returns:
        LLM的响应文本
    """
    llm = get_llm(llm_provider, model=model, temperature=temperature)
    
    # 构造消息格式
    messages = [
        {"role": "system", "content": "You are a helpful assistant for competitive intelligence research."},
        {"role": "user", "content": prompt}
    ]
    
    # 调用LLM
    response = await llm.get_chat_response(
        messages=messages,
        stream=False
    )
    
    return response