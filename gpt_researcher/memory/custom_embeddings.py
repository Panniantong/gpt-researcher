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
        model: str = "text-embedding-3-small",
        api_key: str = None,
        base_url: str = None,
        max_retries: int = 5,  # 增加重试次数
        retry_delay: float = 2.0  # 增加基础延迟
    ):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._request_count = 0  # 请求计数器用于控制频率
        
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
            "Content-Type": "application/json",
            "Connection": "close"  # 强制关闭连接避免连接复用问题
        }
        
        data = {
            "input": input_data,
            "model": self.model
        }
        
        for attempt in range(self.max_retries):
            session = None
            try:
                logger.debug(f"Sending embedding request (attempt {attempt + 1}): {url}")
                
                # 使用新的session避免连接复用问题
                session = requests.Session()
                session.headers.update(headers)
                
                # 控制请求频率 - 每个请求之间至少间隔500ms
                self._request_count += 1
                if self._request_count > 1:
                    import time
                    time.sleep(0.5)
                
                # 增加超时时间和chunked传输处理
                response = session.post(
                    url, 
                    json=data, 
                    timeout=(15, 90),  # 增加超时时间 (连接超时, 读取超时)
                    stream=False,  # 不使用流式传输
                    verify=True,
                    allow_redirects=False  # 禁用重定向
                )
                
                # 确保完整读取响应
                response.raise_for_status()
                
                if response.status_code == 200:
                    try:
                        # 尝试解析JSON响应
                        json_data = response.json()
                        return json_data
                    except (ValueError, json.JSONDecodeError) as json_err:
                        logger.error(f"JSON decode error: {json_err}")
                        logger.error(f"Response content (first 500 chars): {response.text[:500]}")
                        if attempt < self.max_retries - 1:
                            import time
                            time.sleep(self.retry_delay * (attempt + 1))
                            continue
                        else:
                            raise Exception(f"Failed to decode JSON response: {json_err}")
                else:
                    logger.warning(f"Embedding request failed with status {response.status_code}: {response.text[:200]}")
                    if attempt < self.max_retries - 1:
                        import time
                        time.sleep(self.retry_delay * (attempt + 1))
                        continue
                    else:
                        raise Exception(f"Embedding request failed: {response.status_code} {response.text[:200]}")
                        
            except requests.exceptions.ChunkedEncodingError as e:
                logger.error(f"Chunked encoding error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    import time
                    # 对chunked encoding错误使用更长的等待时间
                    time.sleep(min(self.retry_delay * (attempt + 2), 10))
                    continue
                else:
                    logger.warning(f"Chunked encoding error after {self.max_retries} attempts, falling back to zero vector")
                    # 返回一个模拟的成功响应，让上层逻辑处理零向量
                    return {"data": None}
                    
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Connection error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    import time
                    # 连接错误使用指数退避
                    time.sleep(min(self.retry_delay * (2 ** attempt), 15))
                    continue
                else:
                    logger.warning(f"Connection error after {self.max_retries} attempts, falling back to zero vector")
                    return {"data": None}
                    
            except requests.exceptions.Timeout as e:
                logger.error(f"Timeout error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    logger.warning(f"Timeout error after {self.max_retries} attempts, falling back to zero vector")
                    return {"data": None}
                    
            except Exception as e:
                logger.error(f"Embedding request attempt {attempt + 1} failed: {e}")
                logger.error(f"Exception type: {type(e).__name__}")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    raise e
                    
            finally:
                # 确保session被正确关闭
                if session:
                    session.close()
                    
        raise Exception("All embedding request attempts failed")
    
    def _extract_embeddings_from_response(self, response: Dict[str, Any], expected_count: int = 1) -> List[List[float]]:
        """从响应中提取embedding数据"""
        logger.debug(f"Processing embedding response: {list(response.keys())}")

        # 标准OpenAI格式：data字段包含embedding列表
        if 'data' in response and response['data'] is not None:
            data_list = response['data']
            if isinstance(data_list, list) and len(data_list) > 0:
                embeddings = []
                for item in data_list:
                    if isinstance(item, dict) and 'embedding' in item:
                        embedding = item['embedding']
                        if isinstance(embedding, list) and len(embedding) > 0:
                            # 验证embedding是否为数值列表
                            if all(isinstance(x, (int, float)) for x in embedding[:10]):
                                embeddings.append(embedding)
                            else:
                                logger.warning(f"Embedding contains non-numeric values: {embedding[:5]}")
                                embeddings.append([0.0] * self._get_dimension())
                        else:
                            logger.warning(f"Invalid embedding format: {embedding}")
                            embeddings.append([0.0] * self._get_dimension())
                    else:
                        logger.warning(f"Unexpected data item format: {item}")
                        embeddings.append([0.0] * self._get_dimension())
                        
                if len(embeddings) > 0:
                    return embeddings
            else:
                logger.warning(f"Empty or invalid data field: {data_list}")

        # 检查是否有其他可能的embedding数据位置
        for key in ['embeddings', 'vectors', 'result']:
            if key in response and response[key] is not None:
                data = response[key]
                if isinstance(data, list) and len(data) > 0:
                    # 检查是否是embedding向量列表
                    if isinstance(data[0], list) and len(data[0]) > 0:
                        # 验证是否为数值列表
                        if all(isinstance(x, (int, float)) for x in data[0][:5]):
                            return data
                    # 检查是否是包含embedding字段的对象列表
                    elif isinstance(data[0], dict) and 'embedding' in data[0]:
                        embeddings = []
                        for item in data:
                            if isinstance(item, dict) and 'embedding' in item:
                                embeddings.append(item['embedding'])
                        if embeddings:
                            return embeddings

        # 检查是否API直接返回了embedding数组
        if isinstance(response, list) and len(response) > 0:
            if isinstance(response[0], list) and all(isinstance(x, (int, float)) for x in response[0][:5]):
                return response

        # 如果都没找到，记录响应内容并返回零向量
        response_preview = json.dumps(response, indent=2, ensure_ascii=False)[:1000]
        logger.error(f"Could not extract embeddings from response. Response structure: {response_preview}...")
        logger.error("This API response format is not supported, using zero vectors")
        
        # 返回预期数量的零向量
        return [[0.0] * self._get_dimension() for _ in range(expected_count)]
    
    def embed_query(self, text: str) -> List[float]:
        """嵌入单个查询文本"""
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return [0.0] * self._get_dimension()
        
        # 清理文本
        text = text.strip()
        
        try:
            response = self._make_request(text)
            embeddings = self._extract_embeddings_from_response(response, expected_count=1)
            
            if embeddings and len(embeddings) > 0 and isinstance(embeddings[0], list):
                embedding = embeddings[0]
                # 验证embedding的质量
                if len(embedding) > 0 and all(isinstance(x, (int, float)) for x in embedding[:10]):
                    logger.debug(f"Successfully generated embedding of length {len(embedding)}")
                    return embedding
                else:
                    logger.warning(f"Invalid embedding format: {embedding[:5] if embedding else 'empty'}")
                    return [0.0] * self._get_dimension()
            else:
                logger.warning("No valid embeddings returned, using zero vector")
                return [0.0] * self._get_dimension()
                
        except Exception as e:
            logger.error(f"Failed to embed query '{text[:50]}...': {e}")
            logger.error(f"Exception details: {type(e).__name__}: {str(e)}")
            return [0.0] * self._get_dimension()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """嵌入多个文档 - 逐个发送请求以避免API兼容性问题"""
        if not texts:
            return []

        logger.info(f"Starting to embed {len(texts)} documents")
        
        # 对于大批量文本，分组处理以减少服务器压力
        if len(texts) > 20:
            logger.info(f"Large batch detected ({len(texts)} texts), processing in smaller groups")
            batch_size = 5
            result = []
            
            for batch_start in range(0, len(texts), batch_size):
                batch_end = min(batch_start + batch_size, len(texts))
                batch_texts = texts[batch_start:batch_end]
                
                logger.info(f"Processing batch {batch_start//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size} ({len(batch_texts)} texts)")
                
                batch_results = self._embed_batch(batch_texts, batch_start)
                result.extend(batch_results)
                
                # 批次之间的延迟
                if batch_end < len(texts):
                    import time
                    time.sleep(3.0)  # 批次间等待3秒
                    
            logger.info(f"Completed all batches, total: {len(result)} embeddings")
            return result
        else:
            return self._embed_batch(texts, 0)
    
    def _embed_batch(self, texts: List[str], start_index: int = 0) -> List[List[float]]:
        """处理一个批次的文本"""
        result = []

        for i, text in enumerate(texts):
            doc_index = start_index + i + 1
            
            if not text or not text.strip():
                # 空文本使用零向量
                logger.debug(f"Document {doc_index}: empty text, using zero vector")
                result.append([0.0] * self._get_dimension())
                continue

            # 清理文本
            text = text.strip()
            
            try:
                logger.debug(f"Embedding document {doc_index}: {text[:50]}...")
                
                # 对每个文本单独发送请求
                response = self._make_request(text)
                embeddings = self._extract_embeddings_from_response(response, expected_count=1)

                if embeddings and len(embeddings) > 0:
                    embedding = embeddings[0]
                    if isinstance(embedding, list) and len(embedding) > 0:
                        # 验证embedding的质量
                        if all(isinstance(x, (int, float)) for x in embedding[:10]):
                            result.append(embedding)
                            logger.debug(f"Document {doc_index}: successfully embedded (length: {len(embedding)})")
                        else:
                            logger.warning(f"Document {doc_index}: invalid embedding format, using zero vector")
                            result.append([0.0] * self._get_dimension())
                    else:
                        logger.warning(f"Document {doc_index}: empty embedding, using zero vector")
                        result.append([0.0] * self._get_dimension())
                else:
                    logger.warning(f"Document {doc_index}: no embedding returned, using zero vector")
                    result.append([0.0] * self._get_dimension())

            except Exception as e:
                logger.error(f"Document {doc_index}: failed to embed '{text[:50]}...': {e}")
                logger.error(f"Exception details: {type(e).__name__}: {str(e)}")
                result.append([0.0] * self._get_dimension())
                
            # 在请求之间添加适当延迟避免过于频繁的请求
            if i < len(texts) - 1:  # 不在最后一个请求后等待
                import time
                # 对于长文本列表，增加更长的延迟
                delay = 0.8 if len(texts) > 10 else 0.3
                time.sleep(delay)

        logger.info(f"Completed batch embedding, {sum(1 for r in result if any(x != 0 for x in r[:5]))} successful out of {len(result)}")
        return result


def create_custom_embeddings(
    model: str = "text-embedding-3-small",
    api_key: str = None,
    base_url: str = None
) -> CustomOpenAIEmbeddings:
    """创建自定义embedding实例"""
    return CustomOpenAIEmbeddings(
        model=model,
        api_key=api_key,
        base_url=base_url
    )
