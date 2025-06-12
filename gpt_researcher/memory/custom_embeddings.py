"""
自定义embedding客户端，用于处理非标准API响应格式
"""

import os
import json
import requests
import logging
from typing import List, Dict, Any
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)


class CustomOpenAIEmbeddings(Embeddings):
    """
    自定义OpenAI embedding客户端，处理非标准响应格式
    """
    
    def __init__(
        self,
        model: str = "text-embedding-3-large",
        api_key: str = None,
        base_url: str = None,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # 确保base_url不以/结尾
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]
            
        self._dimension = None
        
    def _get_dimension(self) -> int:
        """获取embedding维度"""
        if self._dimension is not None:
            return self._dimension
            
        # 根据模型返回默认维度
        model_dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
        
        self._dimension = model_dimensions.get(self.model, 1536)
        return self._dimension
    
    def _make_request(self, input_data: List[str] | str) -> Dict[str, Any]:
        """发送embedding请求"""
        url = f"{self.base_url}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "input": input_data,
            "model": self.model
        }
        
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"Sending embedding request (attempt {attempt + 1}): {url}")
                response = requests.post(url, headers=headers, json=data, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"Embedding request failed with status {response.status_code}: {response.text}")
                    if attempt < self.max_retries - 1:
                        import time
                        time.sleep(self.retry_delay * (attempt + 1))
                        continue
                    else:
                        raise Exception(f"Embedding request failed: {response.status_code} {response.text}")
                        
            except Exception as e:
                logger.error(f"Embedding request attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    raise e
                    
        raise Exception("All embedding request attempts failed")
    
    def _extract_embeddings_from_response(self, response: Dict[str, Any]) -> List[List[float]]:
        """从响应中提取embedding数据"""
        logger.debug(f"Processing embedding response: {list(response.keys())}")

        # 标准OpenAI格式：data字段包含embedding列表
        if 'data' in response and response['data'] is not None:
            embeddings = []
            for item in response['data']:
                if isinstance(item, dict) and 'embedding' in item:
                    embeddings.append(item['embedding'])
                else:
                    logger.warning(f"Unexpected data item format: {item}")
                    embeddings.append([0.0] * self._get_dimension())
            return embeddings

        # 检查是否有其他可能的embedding数据位置
        # 有些API可能把embedding直接放在其他字段中
        for key in ['embeddings', 'vectors']:
            if key in response and response[key] is not None:
                data = response[key]
                if isinstance(data, list):
                    # 检查是否是embedding向量列表
                    if len(data) > 0 and isinstance(data[0], list) and all(isinstance(x, (int, float)) for x in data[0][:5]):
                        return data
                    # 检查是否是包含embedding字段的对象列表
                    elif len(data) > 0 and isinstance(data[0], dict) and 'embedding' in data[0]:
                        return [item['embedding'] for item in data]

        # 如果都没找到，记录响应内容并返回零向量
        logger.warning(f"Could not extract embeddings from response: {json.dumps(response, indent=2)[:500]}...")
        logger.warning("This API response format is not supported, using zero vectors")

        # 尝试推断输入数量
        input_count = 1  # 默认假设单个输入
        return [[0.0] * self._get_dimension() for _ in range(input_count)]
    
    def embed_query(self, text: str) -> List[float]:
        """嵌入单个查询文本"""
        if not text:
            logger.warning("Empty text provided for embedding")
            return [0.0] * self._get_dimension()
        
        try:
            response = self._make_request(text)
            embeddings = self._extract_embeddings_from_response(response)
            
            if embeddings and len(embeddings) > 0:
                return embeddings[0]
            else:
                logger.warning("No embeddings returned, using zero vector")
                return [0.0] * self._get_dimension()
                
        except Exception as e:
            logger.error(f"Failed to embed query '{text[:50]}...': {e}")
            return [0.0] * self._get_dimension()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """嵌入多个文档 - 逐个发送请求以避免API兼容性问题"""
        if not texts:
            return []

        result = []

        for text in texts:
            if not text:
                # 空文本使用零向量
                result.append([0.0] * self._get_dimension())
                continue

            try:
                # 对每个文本单独发送请求
                response = self._make_request(text)  # 发送单个字符串而不是数组
                embeddings = self._extract_embeddings_from_response(response)

                if embeddings and len(embeddings) > 0:
                    result.append(embeddings[0])  # 取第一个embedding
                else:
                    logger.warning(f"No embedding returned for text: {text[:50]}...")
                    result.append([0.0] * self._get_dimension())

            except Exception as e:
                logger.error(f"Failed to embed text '{text[:50]}...': {e}")
                result.append([0.0] * self._get_dimension())

        return result


def create_custom_embeddings(
    model: str = "text-embedding-3-large",
    api_key: str = None,
    base_url: str = None
) -> CustomOpenAIEmbeddings:
    """创建自定义embedding实例"""
    return CustomOpenAIEmbeddings(
        model=model,
        api_key=api_key,
        base_url=base_url
    )
