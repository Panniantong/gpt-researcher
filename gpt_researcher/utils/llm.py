# libraries
from __future__ import annotations

import logging
from typing import Any

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

from gpt_researcher.llm_provider.generic.base import NO_SUPPORT_TEMPERATURE_MODELS, SUPPORT_REASONING_EFFORT_MODELS, ReasoningEfforts

from ..prompts import PromptFamily
from .costs import estimate_llm_cost
from .validators import Subtopics
import os


def get_llm(llm_provider, **kwargs):
    from gpt_researcher.llm_provider import GenericLLMProvider
    return GenericLLMProvider.from_provider(llm_provider, **kwargs)


async def create_chat_completion(
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float | None = 0.4,
        max_tokens: int | None = 4000,
        llm_provider: str | None = None,
        stream: bool = False,
        websocket: Any | None = None,
        llm_kwargs: dict[str, Any] | None = None,
        cost_callback: callable = None,
        reasoning_effort: str | None = ReasoningEfforts.Medium.value,
        **kwargs
) -> str:
    """Create a chat completion using the OpenAI API
    Args:
        messages (list[dict[str, str]]): The messages to send to the chat completion.
        model (str, optional): The model to use. Defaults to None.
        temperature (float, optional): The temperature to use. Defaults to 0.4.
        max_tokens (int, optional): The max tokens to use. Defaults to 4000.
        llm_provider (str, optional): The LLM Provider to use.
        stream (bool): Whether to stream the response. Defaults to False.
        webocket (WebSocket): The websocket used in the currect request,
        llm_kwargs (dict[str, Any], optional): Additional LLM keyword arguments. Defaults to None.
        cost_callback: Callback function for updating cost.
        reasoning_effort (str, optional): Reasoning effort for OpenAI's reasoning models. Defaults to 'low'.
        **kwargs: Additional keyword arguments.
    Returns:
        str: The response from the chat completion.
    """
    # validate input
    if model is None:
        raise ValueError("Model cannot be None")
    if max_tokens is not None and max_tokens > 32001:
        raise ValueError(
            f"Max tokens cannot be more than 16,000, but got {max_tokens}")

    # Get the provider from supported providers
    provider_kwargs = {'model': model}

    if llm_kwargs:
        provider_kwargs.update(llm_kwargs)

    if model in SUPPORT_REASONING_EFFORT_MODELS:
        provider_kwargs['reasoning_effort'] = reasoning_effort

    if model not in NO_SUPPORT_TEMPERATURE_MODELS:
        provider_kwargs['temperature'] = temperature
        provider_kwargs['max_tokens'] = max_tokens
    else:
        provider_kwargs['temperature'] = None
        provider_kwargs['max_tokens'] = None

    if llm_provider == "openai":
        # 检查是否是需要使用官方API的模型（如o3系列）
        official_models = ['o3', 'o3-mini', 'o3-2025-04-16', 'o3-mini-2025-01-31']
        use_official_api = any(model.startswith(official_model) for official_model in official_models)
        
        if use_official_api:
            # 使用官方OpenAI API配置
            api_key = os.environ.get("OPENAI_OFFICIAL_API_KEY", None)
            base_url = os.environ.get("OPENAI_OFFICIAL_BASE_URL", "https://api.openai.com/v1")
            if api_key:
                provider_kwargs['openai_api_key'] = api_key
            if base_url:
                provider_kwargs['openai_api_base'] = base_url
        else:
            # 使用逆向API配置（默认行为）
            base_url = os.environ.get("OPENAI_BASE_URL", None)
            if base_url:
                provider_kwargs['openai_api_base'] = base_url

    provider = get_llm(llm_provider, **provider_kwargs)
    response = ""
    last_error = None

    # create response with retry logic
    for attempt in range(3):  # maximum of 3 attempts for better error handling
        try:
            response = await provider.get_chat_response(
                messages, stream, websocket, **kwargs
            )

            # 检查响应是否有效
            if response and response.strip():
                if cost_callback:
                    llm_costs = estimate_llm_cost(str(messages), response)
                    cost_callback(llm_costs)
                return response
            else:
                print(f"Attempt {attempt + 1}: Received empty response, retrying...")
                last_error = "Empty response received"

        except Exception as e:
            last_error = str(e)
            print(f"Attempt {attempt + 1} failed: {last_error}")
            if attempt < 2:  # Don't sleep on the last attempt
                import asyncio
                await asyncio.sleep(1 * (attempt + 1))  # Progressive delay

    # 如果所有尝试都失败了，返回一个错误报告而不是抛出异常
    error_response = f"""# API调用失败

## 错误信息
经过3次尝试后仍无法获取有效响应。

最后一次错误: {last_error}

## 可能的原因
1. API服务暂时不可用
2. 网络连接问题
3. API配置错误
4. 请求超时

## 建议解决方案
1. 检查网络连接
2. 验证API密钥和配置
3. 稍后重试
4. 联系技术支持

---
*错误发生时间: {provider_kwargs.get('model', 'unknown')} via {llm_provider}*
"""

    logging.error(f"Failed to get response from {llm_provider} API after 3 attempts. Last error: {last_error}")
    return error_response


async def construct_subtopics(
    task: str,
    data: str,
    config,
    subtopics: list = [],
    prompt_family: type[PromptFamily] | PromptFamily = PromptFamily,
    **kwargs
) -> list:
    """
    Construct subtopics based on the given task and data.

    Args:
        task (str): The main task or topic.
        data (str): Additional data for context.
        config: Configuration settings.
        subtopics (list, optional): Existing subtopics. Defaults to [].
        prompt_family (PromptFamily): Family of prompts
        **kwargs: Additional keyword arguments.

    Returns:
        list: A list of constructed subtopics.
    """
    try:
        parser = PydanticOutputParser(pydantic_object=Subtopics)

        prompt = PromptTemplate(
            template=prompt_family.generate_subtopics_prompt(),
            input_variables=["task", "data", "subtopics", "max_subtopics"],
            partial_variables={
                "format_instructions": parser.get_format_instructions()},
        )

        provider_kwargs = {'model': config.smart_llm_model}

        if config.llm_kwargs:
            provider_kwargs.update(config.llm_kwargs)

        if config.smart_llm_model in SUPPORT_REASONING_EFFORT_MODELS:
            provider_kwargs['reasoning_effort'] = ReasoningEfforts.High.value
        else:
            provider_kwargs['temperature'] = config.temperature
            provider_kwargs['max_tokens'] = config.smart_token_limit

        # 为construct_subtopics函数也添加官方API支持
        if config.smart_llm_provider == "openai":
            # 检查是否是需要使用官方API的模型（如o3系列）
            official_models = ['o3', 'o3-mini', 'o3-2025-04-16', 'o3-mini-2025-01-31']
            use_official_api = any(config.smart_llm_model.startswith(official_model) for official_model in official_models)
            
            if use_official_api:
                # 使用官方OpenAI API配置
                api_key = os.environ.get("OPENAI_OFFICIAL_API_KEY", None)
                base_url = os.environ.get("OPENAI_OFFICIAL_BASE_URL", "https://api.openai.com/v1")
                if api_key:
                    provider_kwargs['openai_api_key'] = api_key
                if base_url:
                    provider_kwargs['openai_api_base'] = base_url
            else:
                # 使用逆向API配置（默认行为）
                base_url = os.environ.get("OPENAI_BASE_URL", None)
                if base_url:
                    provider_kwargs['openai_api_base'] = base_url

        provider = get_llm(config.smart_llm_provider, **provider_kwargs)

        model = provider.llm

        chain = prompt | model | parser

        output = chain.invoke({
            "task": task,
            "data": data,
            "subtopics": subtopics,
            "max_subtopics": config.max_subtopics
        }, **kwargs)

        return output

    except Exception as e:
        print("Exception in parsing subtopics : ", e)
        return subtopics
