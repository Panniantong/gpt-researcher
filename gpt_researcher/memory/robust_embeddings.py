"""
Robust OpenAI Embeddings wrapper that handles errors gracefully
"""
import os
import time
from typing import List, Optional
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
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
        
        # Try to get model name from base embeddings
        model_name = getattr(self.base_embeddings, "model", "text-embedding-3-large")
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
                    return [result] if isinstance(result, list) else [[]]
                else:
                    # For documents, use embed_documents
                    result = self.base_embeddings.embed_documents(texts)
                    return result if result is not None else []
                    
            except Exception as e:
                error_msg = str(e)
                if "'NoneType' object is not iterable" in error_msg:
                    logger.warning(f"Error on attempt {attempt + 1}: {error_msg}")
                else:
                    logger.error(f"Unexpected error on attempt {attempt + 1}: {error_msg}")
                
                if attempt < self._max_retries - 1:
                    time.sleep(self._retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    logger.error("All embedding attempts failed")
                    
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
        
        if embeddings and len(embeddings) > 0:
            return embeddings[0]
        else:
            # Return zero vector of appropriate dimension
            logger.warning("Returning zero vector due to embedding failure")
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
        for i, embedding in enumerate(embeddings):
            if i < len(non_empty_indices):
                result[non_empty_indices[i]] = embedding
                
        # Ensure all embeddings have the correct dimension
        for i, embedding in enumerate(result):
            if not embedding or len(embedding) != dimension:
                result[i] = [0.0] * dimension
                
        return result