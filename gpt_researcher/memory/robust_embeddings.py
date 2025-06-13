"""
Robust OpenAI Embeddings wrapper that handles errors gracefully
"""
import time
from typing import List
import logging

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings

logger = logging.getLogger(__name__)


def create_robust_embeddings(provider: str, model: str, **kwargs):
    """Create a robust embeddings instance that handles errors gracefully."""
    try:
        if provider == "openai":
            base_embeddings = OpenAIEmbeddings(model=model, **kwargs)
            return RobustOpenAIEmbeddings(base_embeddings, provider="openai")
        elif provider == "azure_openai":
            base_embeddings = AzureOpenAIEmbeddings(model=model, **kwargs)
            return RobustOpenAIEmbeddings(base_embeddings, provider="azure_openai")
        else:
            return None
    except Exception as e:
        logger.error(f"Failed to create robust embeddings: {e}")
        return None


class RobustOpenAIEmbeddings(Embeddings):
    """
    A robust wrapper for OpenAI embeddings that handles errors gracefully.
    """
    
    def __init__(self, base_embeddings, provider="openai"):
        """
        Initialize with base embeddings instance.
        
        Args:
            base_embeddings: The base embeddings instance (OpenAIEmbeddings or AzureOpenAIEmbeddings)
            provider: The provider type ("openai" or "azure_openai")
        """
        self.base_embeddings = base_embeddings
        self.provider = provider
        self._dimension = None
        self._max_retries = 3
        self._retry_delay = 1  # seconds
        
    def _get_dimension(self) -> int:
        """Get the dimension of embeddings for this model."""
        if self._dimension is not None:
            return self._dimension
            
        # Try to get dimension from a test embedding
        try:
            test_embedding = self._embed_with_retry(["test"], is_query=True)
            if test_embedding and len(test_embedding) > 0:
                self._dimension = len(test_embedding[0])
                return self._dimension
        except Exception:
            pass
            
        # Default dimensions for known models
        model_dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-small": 3072,
            "text-embedding-ada-002": 1536,
        }
        
        # Try to get model name from base embeddings
        model_name = getattr(self.base_embeddings, "model", "text-embedding-3-small")
        return model_dimensions.get(model_name, 1536)  # Default to 1536
    
    def _embed_with_retry(self, texts: List[str], is_query: bool = False) -> List[List[float]]:
        """
        Embed texts with retry logic.

        Args:
            texts: List of texts to embed
            is_query: Whether this is a query (True) or documents (False)

        Returns:
            List of embeddings
        """
        for attempt in range(self._max_retries):
            try:
                if is_query and len(texts) == 1:
                    # For single query, use embed_query
                    result = self.base_embeddings.embed_query(texts[0])

                    # Debug: Log the actual response
                    logger.debug(f"Embedding API response type: {type(result)}")
                    logger.debug(f"Embedding API response content: {str(result)[:200]}...")

                    # Check if result is None or empty
                    if result is None:
                        logger.warning(f"Embedding returned None for query on attempt {attempt + 1}")
                        if attempt < self._max_retries - 1:
                            time.sleep(self._retry_delay * (attempt + 1))
                            continue
                        else:
                            return [[]]

                    # Check if result is a valid list of numbers
                    if isinstance(result, list) and len(result) > 0:
                        # Verify it's actually a list of numbers
                        if all(isinstance(x, (int, float)) for x in result[:5]):  # Check first 5 elements
                            return [result]
                        else:
                            logger.error(f"Embedding result contains non-numeric values: {result[:5]}")
                            return [[]]
                    else:
                        logger.error(f"Embedding result is not a valid list: {type(result)}, {result}")
                        return [[]]
                else:
                    # For documents, use embed_documents
                    result = self.base_embeddings.embed_documents(texts)

                    # Debug: Log the actual response
                    logger.debug(f"Embedding API response type: {type(result)}")
                    logger.debug(f"Embedding API response length: {len(result) if result else 'None'}")
                    if result and len(result) > 0:
                        logger.debug(f"First embedding type: {type(result[0])}")
                        logger.debug(f"First embedding sample: {str(result[0])[:100]}...")

                    # Check if result is None
                    if result is None:
                        logger.warning(f"Embedding returned None for documents on attempt {attempt + 1}")
                        if attempt < self._max_retries - 1:
                            time.sleep(self._retry_delay * (attempt + 1))
                            continue
                        else:
                            return []

                    # Validate the result structure
                    if isinstance(result, list):
                        # Check if all embeddings are valid
                        valid_embeddings = []
                        for i, embedding in enumerate(result):
                            if isinstance(embedding, list) and len(embedding) > 0:
                                if all(isinstance(x, (int, float)) for x in embedding[:5]):  # Check first 5 elements
                                    valid_embeddings.append(embedding)
                                else:
                                    logger.error(f"Embedding {i} contains non-numeric values: {embedding[:5]}")
                                    valid_embeddings.append([0.0] * self._get_dimension())
                            else:
                                logger.error(f"Embedding {i} is not a valid list: {type(embedding)}")
                                valid_embeddings.append([0.0] * self._get_dimension())
                        return valid_embeddings
                    else:
                        logger.error(f"Embedding result is not a list: {type(result)}")
                        return []

            except Exception as e:
                error_msg = str(e)

                # Categorize common embedding errors
                if "'NoneType' object is not iterable" in error_msg:
                    logger.debug(f"Embedding attempt {attempt + 1} failed: API returned None")
                elif "None" in error_msg:
                    logger.debug(f"Embedding attempt {attempt + 1} failed: None-related error")
                elif "rate limit" in error_msg.lower():
                    logger.warning(f"Embedding attempt {attempt + 1} failed: Rate limit exceeded")
                elif "api key" in error_msg.lower() or "unauthorized" in error_msg.lower():
                    logger.error(f"Embedding failed: API authentication issue - {error_msg}")
                    # Don't retry on auth errors
                    break
                elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
                    logger.warning(f"Embedding attempt {attempt + 1} failed: Network issue")
                else:
                    logger.warning(f"Embedding attempt {attempt + 1} failed: {error_msg}")

                if attempt < self._max_retries - 1:
                    time.sleep(self._retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    # Only log final failure if it's not an auth issue
                    if "api key" not in error_msg.lower() and "unauthorized" not in error_msg.lower():
                        logger.warning(f"All {self._max_retries} embedding attempts failed. Using zero vectors.")

        return []
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text.

        Args:
            text: The query text to embed

        Returns:
            List of floats representing the embedding
        """
        if not text:
            logger.warning("Empty text provided for embedding")
            return [0.0] * self._get_dimension()

        embeddings = self._embed_with_retry([text], is_query=True)

        if embeddings and len(embeddings) > 0 and embeddings[0] is not None:
            # Ensure the embedding is a valid list of floats
            embedding = embeddings[0]
            if isinstance(embedding, list) and len(embedding) > 0:
                return embedding
            else:
                logger.warning("Invalid embedding format received")
                return [0.0] * self._get_dimension()
        else:
            # Return zero vector of appropriate dimension
            logger.debug("Returning zero vector due to embedding failure")
            return [0.0] * self._get_dimension()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple documents.
        
        Args:
            texts: List of document texts to embed
            
        Returns:
            List of embeddings (one per document)
        """
        if not texts:
            return []
            
        # Filter out empty texts but keep track of indices
        non_empty_texts = []
        non_empty_indices = []
        for i, text in enumerate(texts):
            if text:
                non_empty_texts.append(text)
                non_empty_indices.append(i)
                
        if not non_empty_texts:
            # All texts were empty, return zero vectors
            return [[0.0] * self._get_dimension() for _ in texts]
            
        # Get embeddings for non-empty texts
        embeddings = self._embed_with_retry(non_empty_texts, is_query=False)

        # Prepare result with zero vectors for empty texts
        dimension = self._get_dimension()
        result = [[0.0] * dimension for _ in texts]

        # Fill in the actual embeddings
        if embeddings:
            for i, embedding in enumerate(embeddings):
                if i < len(non_empty_indices) and embedding is not None:
                    # Validate embedding format
                    if isinstance(embedding, list) and len(embedding) > 0:
                        result[non_empty_indices[i]] = embedding
                    else:
                        logger.warning(f"Invalid embedding format for text {i}")
                        result[non_empty_indices[i]] = [0.0] * dimension

        # Ensure all embeddings have the correct dimension
        for i, embedding in enumerate(result):
            if not embedding or len(embedding) != dimension:
                result[i] = [0.0] * dimension

        return result