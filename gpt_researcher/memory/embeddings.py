import os
from typing import Any
import logging
from .robust_embeddings import create_robust_embeddings

logger = logging.getLogger(__name__)

OPENAI_EMBEDDING_MODEL = os.environ.get(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)

_SUPPORTED_PROVIDERS = {
    "openai",
    "azure_openai",
    "cohere",
    "gigachat",
    "google_vertexai",
    "google_genai",
    "fireworks",
    "ollama",
    "together",
    "mistralai",
    "huggingface",
    "nomic",
    "voyageai",
    "dashscope",
    "custom",
    "bedrock",
    "aimlapi",
}


class Memory:
    def __init__(self, embedding_provider: str, model: str, **embdding_kwargs: Any):
        _embeddings = None
        match embedding_provider:
            case "custom":
                # 使用自定义embedding客户端处理非标准API响应
                from .custom_embeddings import create_custom_embeddings

                _embeddings = create_custom_embeddings(
                    model=model,
                    api_key=os.getenv("OPENAI_API_KEY", "custom"),
                    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1")
                )
            case "openai":
                # Use official OpenAI API for embeddings
                # 优先使用专门的embedding API配置，如果没有则使用默认配置
                openai_api_key = os.getenv("OPENAI_EMBEDDING_API_KEY") or os.getenv("OPENAI_API_KEY")
                openai_base_url = os.getenv("OPENAI_EMBEDDING_BASE_URL") or os.getenv("OPENAI_BASE_URL")
                
                # 如果有专门的embedding配置，直接使用官方API
                if os.getenv("OPENAI_EMBEDDING_API_KEY"):
                    from langchain_openai import OpenAIEmbeddings
                    _embeddings = OpenAIEmbeddings(
                        model=model,
                        openai_api_key=openai_api_key,
                        openai_api_base=openai_base_url,
                        **embdding_kwargs
                    )
                else:
                    # 否则使用robust wrapper（适用于逆向API）
                    robust_embeddings = create_robust_embeddings("openai", model, **embdding_kwargs)
                    if robust_embeddings:
                        _embeddings = robust_embeddings
                    else:
                        from langchain_openai import OpenAIEmbeddings
                        _embeddings = OpenAIEmbeddings(model=model, **embdding_kwargs)
            case "azure_openai":
                # Use robust embeddings wrapper to handle None responses
                robust_embeddings = create_robust_embeddings("azure_openai", model, **embdding_kwargs)
                if robust_embeddings:
                    _embeddings = robust_embeddings
                else:
                    from langchain_openai import AzureOpenAIEmbeddings
                    _embeddings = AzureOpenAIEmbeddings(
                        model=model,
                        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
                        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
                        **embdding_kwargs,
                    )
            case "cohere":
                from langchain_cohere import CohereEmbeddings

                _embeddings = CohereEmbeddings(model=model, **embdding_kwargs)
            case "google_vertexai":
                from langchain_google_vertexai import VertexAIEmbeddings

                _embeddings = VertexAIEmbeddings(model=model, **embdding_kwargs)
            case "google_genai":
                from langchain_google_genai import GoogleGenerativeAIEmbeddings

                _embeddings = GoogleGenerativeAIEmbeddings(
                    model=model, **embdding_kwargs
                )
            case "fireworks":
                from langchain_fireworks import FireworksEmbeddings

                _embeddings = FireworksEmbeddings(model=model, **embdding_kwargs)
            case "gigachat":
                from langchain_gigachat import GigaChatEmbeddings

                _embeddings = GigaChatEmbeddings(model=model, **embdding_kwargs)
            case "ollama":
                from langchain_ollama import OllamaEmbeddings

                _embeddings = OllamaEmbeddings(
                    model=model,
                    base_url=os.environ["OLLAMA_BASE_URL"],
                    **embdding_kwargs,
                )
            case "together":
                from langchain_together import TogetherEmbeddings

                _embeddings = TogetherEmbeddings(model=model, **embdding_kwargs)
            case "mistralai":
                from langchain_mistralai import MistralAIEmbeddings

                _embeddings = MistralAIEmbeddings(model=model, **embdding_kwargs)
            case "huggingface":
                from langchain_huggingface import HuggingFaceEmbeddings

                _embeddings = HuggingFaceEmbeddings(model_name=model, **embdding_kwargs)
            case "nomic":
                from langchain_nomic import NomicEmbeddings

                _embeddings = NomicEmbeddings(model=model, **embdding_kwargs)
            case "voyageai":
                from langchain_voyageai import VoyageAIEmbeddings

                _embeddings = VoyageAIEmbeddings(
                    voyage_api_key=os.environ["VOYAGE_API_KEY"],
                    model=model,
                    **embdding_kwargs,
                )
            case "dashscope":
                from langchain_community.embeddings import DashScopeEmbeddings

                _embeddings = DashScopeEmbeddings(model=model, **embdding_kwargs)
            case "bedrock":
                from langchain_aws.embeddings import BedrockEmbeddings

                _embeddings = BedrockEmbeddings(model_id=model, **embdding_kwargs)
            case "aimlapi":
                from langchain_openai import OpenAIEmbeddings

                _embeddings = OpenAIEmbeddings(
                    model=model,
                    openai_api_key=os.getenv("AIMLAPI_API_KEY"),
                    openai_api_base=os.getenv("AIMLAPI_BASE_URL", "https://api.aimlapi.com/v1"),
                    **embdding_kwargs,
                )
            case _:
                raise Exception("Embedding not found.")

        self._embeddings = _embeddings

    def get_embeddings(self):
        if self._embeddings is None:
            raise ValueError("Embeddings not initialized. Please check your embedding provider configuration.")
        return self._embeddings
