import os
import asyncio
from typing import Optional
from .retriever import SearchAPIRetriever, SectionRetriever
from langchain.retrievers import (
    ContextualCompressionRetriever,
)
from langchain.retrievers.document_compressors import (
    DocumentCompressorPipeline,
    EmbeddingsFilter,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..vector_store import VectorStoreWrapper
from ..utils.costs import estimate_embedding_cost
from ..memory.embeddings import OPENAI_EMBEDDING_MODEL
from ..prompts import PromptFamily


class VectorstoreCompressor:
    def __init__(
        self,
        vector_store: VectorStoreWrapper,
        max_results:int = 7,
        filter: Optional[dict] = None,
        prompt_family: type[PromptFamily] | PromptFamily = PromptFamily,
        **kwargs,
    ):

        self.vector_store = vector_store
        self.max_results = max_results
        self.filter = filter
        self.kwargs = kwargs
        self.prompt_family = prompt_family

    async def async_get_context(self, query, max_results=5):
        """Get relevant context from vector store"""
        results = await self.vector_store.asimilarity_search(query=query, k=max_results, filter=self.filter)
        return self.prompt_family.pretty_print_docs(results)


class ContextCompressor:
    def __init__(
        self,
        documents,
        embeddings,
        max_results=5,
        prompt_family: type[PromptFamily] | PromptFamily = PromptFamily,
        **kwargs,
    ):
        self.max_results = max_results
        self.documents = documents
        self.kwargs = kwargs
        self.embeddings = embeddings
        self.similarity_threshold = os.environ.get("SIMILARITY_THRESHOLD", 0.35)
        self.prompt_family = prompt_family

    def __get_contextual_retriever(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        relevance_filter = EmbeddingsFilter(embeddings=self.embeddings,
                                            similarity_threshold=self.similarity_threshold)
        pipeline_compressor = DocumentCompressorPipeline(
            transformers=[splitter, relevance_filter]
        )
        base_retriever = SearchAPIRetriever(
            pages=self.documents
        )
        contextual_retriever = ContextualCompressionRetriever(
            base_compressor=pipeline_compressor, base_retriever=base_retriever
        )
        return contextual_retriever

    async def async_get_context(self, query, max_results=5, cost_callback=None):
        try:
            # 首先检查文档是否为空
            if not self.documents:
                print("Warning: No documents provided to ContextCompressor")
                return ""

            # 检查embedding是否可用
            if not self.embeddings:
                print("Warning: No embeddings provided to ContextCompressor")
                return ""

            # 尝试创建contextual retriever
            compressed_docs = self.__get_contextual_retriever()
            if cost_callback and self.documents:
                cost_callback(estimate_embedding_cost(model=OPENAI_EMBEDDING_MODEL, docs=self.documents))

            # 执行检索，添加更详细的错误处理
            relevant_docs = await asyncio.to_thread(compressed_docs.invoke, query, **self.kwargs)

            # 检查返回的文档
            if not relevant_docs:
                print(f"Warning: No relevant documents found for query: {query}")
                return ""

            return self.prompt_family.pretty_print_docs(relevant_docs, max_results)

        except Exception as e:
            error_msg = str(e)
            print(f"Error in ContextCompressor.async_get_context: {error_msg}")

            # 提供更具体的错误信息
            if "index 0 is out of bounds" in error_msg:
                print("This error is likely due to embedding compatibility issues with LangChain's EmbeddingsFilter")
                print("Falling back to simple document retrieval without embedding filtering...")

                # 尝试简单的文档检索作为后备方案
                try:
                    return await self._fallback_simple_retrieval(query, max_results)
                except Exception as fallback_error:
                    print(f"Fallback retrieval also failed: {fallback_error}")

            # Return empty string on error to prevent cascading failures
            return ""

    async def _fallback_simple_retrieval(self, query, max_results=5):
        """
        简单的后备检索方法，不使用embedding过滤
        当EmbeddingsFilter出现问题时使用
        """
        try:
            # 简单的关键词匹配
            query_lower = query.lower()
            query_words = set(query_lower.split())

            scored_docs = []

            for doc in self.documents:
                # 获取文档内容
                title = doc.get('title', '').lower()
                body = doc.get('body', '').lower()
                content = f"{title} {body}"

                # 简单的关键词匹配评分
                content_words = set(content.split())
                common_words = query_words.intersection(content_words)
                score = len(common_words) / len(query_words) if query_words else 0

                if score > 0:
                    scored_docs.append((score, doc))

            # 按分数排序并取前N个
            scored_docs.sort(key=lambda x: x[0], reverse=True)
            top_docs = [doc for _, doc in scored_docs[:max_results]]

            if not top_docs:
                return ""

            # 格式化输出
            formatted_docs = []
            for doc in top_docs:
                title = doc.get('title', 'Untitled')
                body = doc.get('body', '')
                href = doc.get('href', '')

                formatted_doc = f"Title: {title}\n"
                if href:
                    formatted_doc += f"URL: {href}\n"
                formatted_doc += f"Content: {body}\n"
                formatted_docs.append(formatted_doc)

            return "\n".join(formatted_docs)

        except Exception as e:
            print(f"Error in fallback simple retrieval: {e}")
            return ""


class WrittenContentCompressor:
    def __init__(self, documents, embeddings, similarity_threshold, **kwargs):
        self.documents = documents
        self.kwargs = kwargs
        self.embeddings = embeddings
        self.similarity_threshold = similarity_threshold

    def __get_contextual_retriever(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        relevance_filter = EmbeddingsFilter(embeddings=self.embeddings,
                                            similarity_threshold=self.similarity_threshold)
        pipeline_compressor = DocumentCompressorPipeline(
            transformers=[splitter, relevance_filter]
        )
        base_retriever = SectionRetriever(
            sections=self.documents
        )
        contextual_retriever = ContextualCompressionRetriever(
            base_compressor=pipeline_compressor, base_retriever=base_retriever
        )
        return contextual_retriever

    def __pretty_docs_list(self, docs, top_n):
        return [f"Title: {d.metadata.get('section_title')}\nContent: {d.page_content}\n" for i, d in enumerate(docs) if i < top_n]

    async def async_get_context(self, query, max_results=5, cost_callback=None):
        try:
            compressed_docs = self.__get_contextual_retriever()
            if cost_callback and self.documents:
                cost_callback(estimate_embedding_cost(model=OPENAI_EMBEDDING_MODEL, docs=self.documents))
            relevant_docs = await asyncio.to_thread(compressed_docs.invoke, query, **self.kwargs)
            return self.__pretty_docs_list(relevant_docs, max_results)
        except Exception as e:
            print(f"Error in WrittenContentCompressor.async_get_context: {e}")
            # Return empty list on error to prevent cascading failures
            return []
