import json_repair

from gpt_researcher.llm_provider.generic.base import ReasoningEfforts
from ..utils.llm import create_chat_completion
from ..prompts import PromptFamily
from typing import Any, List, Dict
from ..config import Config
import logging

logger = logging.getLogger(__name__)

# Maximum query length for Tavily API (400 characters)
MAX_QUERY_LENGTH = 400

def truncate_query(query: str, max_length: int = MAX_QUERY_LENGTH) -> str:
    """
    Truncate query to fit within API character limits.

    Args:
        query (str): The original query
        max_length (int): Maximum allowed length

    Returns:
        str: Truncated query that fits within the limit
    """
    if len(query) <= max_length:
        return query

    # Try to truncate at word boundary to maintain readability
    truncated = query[:max_length]
    last_space = truncated.rfind(' ')

    if last_space > max_length * 0.8:  # If we can find a space in the last 20%
        return truncated[:last_space].strip()
    else:
        # If no good word boundary, just truncate at character limit
        return truncated.strip()

async def get_search_results(query: str, retriever: Any, query_domains: List[str] = None, researcher=None) -> List[Dict[str, Any]]:
    """
    Get web search results for a given query.

    Args:
        query: The search query
        retriever: The retriever instance
        query_domains: Optional list of domains to search
        researcher: The researcher instance (needed for MCP retrievers)

    Returns:
        A list of search results
    """
    # Ensure query is within API limits before passing to retriever
    truncated_query = truncate_query(query, MAX_QUERY_LENGTH)
    if len(query) > MAX_QUERY_LENGTH:
        logger.info(f"Query truncated from {len(query)} to {len(truncated_query)} characters")

    # Check if this is an MCP retriever and pass the researcher instance
    if "mcpretriever" in retriever.__name__.lower():
        search_retriever = retriever(
            truncated_query,
            query_domains=query_domains,
            researcher=researcher  # Pass researcher instance for MCP retrievers
        )
    else:
        search_retriever = retriever(truncated_query, query_domains=query_domains)

    return search_retriever.search()

async def generate_sub_queries(
    query: str,
    parent_query: str,
    report_type: str,
    context: List[Dict[str, Any]],
    cfg: Config,
    cost_callback: callable = None,
    prompt_family: type[PromptFamily] | PromptFamily = PromptFamily,
    **kwargs
) -> List[str]:
    """
    Generate sub-queries using the specified LLM model.

    Args:
        query: The original query
        parent_query: The parent query
        report_type: The type of report
        max_iterations: Maximum number of research iterations
        context: Search results context
        cfg: Configuration object
        cost_callback: Callback for cost calculation
        prompt_family: Family of prompts

    Returns:
        A list of sub-queries
    """
    # First, translate query to English if it's not already
    translation_prompt = f"""If the following query is not in English, translate it to English. 
If it's already in English, return it as is.
Query: {query}

Return ONLY the English query, nothing else."""
    
    try:
        english_query = await create_chat_completion(
            model=cfg.smart_llm_model,
            messages=[{"role": "user", "content": translation_prompt}],
            temperature=0.3,
            max_tokens=500,
            llm_provider=cfg.smart_llm_provider,
            llm_kwargs=cfg.llm_kwargs,
            cost_callback=cost_callback,
        )
        english_query = english_query.strip()
    except Exception as e:
        logger.warning(f"Failed to translate query: {e}. Using original query.")
        english_query = query
    
    gen_queries_prompt = prompt_family.generate_search_queries_prompt(
        english_query,
        parent_query,
        report_type,
        max_iterations=cfg.max_iterations or 3,
        context=context,
    )

    try:
        response = await create_chat_completion(
            model=cfg.strategic_llm_model,
            messages=[{"role": "user", "content": gen_queries_prompt}],
            llm_provider=cfg.strategic_llm_provider,
            max_tokens=None,
            llm_kwargs=cfg.llm_kwargs,
            reasoning_effort=ReasoningEfforts.Medium.value,
            cost_callback=cost_callback,
            **kwargs
        )
    except Exception as e:
        logger.warning(f"Error with strategic LLM: {e}. Retrying with max_tokens={cfg.strategic_token_limit}.")
        logger.warning(f"See https://github.com/assafelovic/gpt-researcher/issues/1022")
        try:
            response = await create_chat_completion(
                model=cfg.strategic_llm_model,
                messages=[{"role": "user", "content": gen_queries_prompt}],
                max_tokens=cfg.strategic_token_limit,
                llm_provider=cfg.strategic_llm_provider,
                llm_kwargs=cfg.llm_kwargs,
                cost_callback=cost_callback,
                **kwargs
            )
            logger.warning(f"Retrying with max_tokens={cfg.strategic_token_limit} successful.")
        except Exception as e:
            logger.warning(f"Retrying with max_tokens={cfg.strategic_token_limit} failed.")
            logger.warning(f"Error with strategic LLM: {e}. Falling back to smart LLM.")
            response = await create_chat_completion(
                model=cfg.smart_llm_model,
                messages=[{"role": "user", "content": gen_queries_prompt}],
                temperature=cfg.temperature,
                max_tokens=cfg.smart_token_limit,
                llm_provider=cfg.smart_llm_provider,
                llm_kwargs=cfg.llm_kwargs,
                cost_callback=cost_callback,
                **kwargs
            )

    # Parse the response and truncate any queries that are too long
    sub_queries = json_repair.loads(response)

    # Ensure all sub-queries are within length limits
    if isinstance(sub_queries, list):
        truncated_queries = []
        for query in sub_queries:
            if isinstance(query, str):
                truncated_query = truncate_query(query, MAX_QUERY_LENGTH)
                if len(query) > MAX_QUERY_LENGTH:
                    logger.info(f"Sub-query truncated from {len(query)} to {len(truncated_query)} characters")
                truncated_queries.append(truncated_query)
            else:
                truncated_queries.append(query)
        return truncated_queries

    return sub_queries

async def plan_research_outline(
    query: str,
    search_results: List[Dict[str, Any]],
    agent_role_prompt: str,
    cfg: Config,
    parent_query: str,
    report_type: str,
    cost_callback: callable = None,
    retriever_names: List[str] = None,
    **kwargs
) -> List[str]:
    """
    Plan the research outline by generating sub-queries.

    Args:
        query: Original query
        search_results: Initial search results
        agent_role_prompt: Agent role prompt
        cfg: Configuration object
        parent_query: Parent query
        report_type: Report type
        cost_callback: Callback for cost calculation
        retriever_names: Names of the retrievers being used

    Returns:
        A list of sub-queries
    """
    # Handle the case where retriever_names is not provided
    if retriever_names is None:
        retriever_names = []
    
    # For MCP retrievers, we may want to skip sub-query generation
    # Check if MCP is the only retriever or one of multiple retrievers
    if retriever_names and ("mcp" in retriever_names or "MCPRetriever" in retriever_names):
        mcp_only = (len(retriever_names) == 1 and 
                   ("mcp" in retriever_names or "MCPRetriever" in retriever_names))
        
        if mcp_only:
            # If MCP is the only retriever, skip sub-query generation
            logger.info("Using MCP retriever only - skipping sub-query generation")
            # Return the original query to prevent additional search iterations
            return [query]
        else:
            # If MCP is one of multiple retrievers, generate sub-queries for the others
            logger.info("Using MCP with other retrievers - generating sub-queries for non-MCP retrievers")

    # Generate sub-queries for research outline
    sub_queries = await generate_sub_queries(
        query,
        parent_query,
        report_type,
        search_results,
        cfg,
        cost_callback,
        **kwargs
    )

    return sub_queries
