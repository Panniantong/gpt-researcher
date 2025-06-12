# Tavily API Retriever

# libraries
import os
from typing import Literal, Sequence, Optional
import requests
import json


class TavilySearch:
    """
    Tavily API Retriever
    """

    def __init__(self, query, headers=None, topic="general", query_domains=None):
        """
        Initializes the TavilySearch object.

        Args:
            query (str): The search query string.
            headers (dict, optional): Additional headers to include in the request. Defaults to None.
            topic (str, optional): The topic for the search. Defaults to "general".
            query_domains (list, optional): List of domains to include in the search. Defaults to None.
        """
        # Tavily API has a 400 character limit for queries
        self.query = query[:400] if len(query) > 400 else query
        self.headers = headers or {}
        self.topic = topic
        self.base_url = "https://api.tavily.com/search"
        self.api_key = self.get_api_key()
        self.headers = {
            "Content-Type": "application/json",
        }
        self.query_domains = query_domains or None

    def _truncate_query(self, query: str, max_length: int = 400) -> str:
        """
        Truncate query to fit within Tavily API's character limit.

        Args:
            query (str): The original query
            max_length (int): Maximum allowed length (default: 400 for Tavily API)

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

    def get_api_key(self):
        """
        Gets the Tavily API key
        Returns:

        """
        api_key = self.headers.get("tavily_api_key")
        if not api_key:
            try:
                api_key = os.environ["TAVILY_API_KEY"]
            except KeyError:
                print(
                    "Tavily API key not found, set to blank. If you need a retriver, please set the TAVILY_API_KEY environment variable."
                )
                return ""
        return api_key


    def _search(
        self,
        query: str,
        search_depth: Literal["basic", "advanced"] = "basic",
        topic: str = "general",
        days: int = 2,
        max_results: int = 10,
        include_domains: Sequence[str] = None,
        exclude_domains: Sequence[str] = None,
        include_answer: bool = False,
        include_raw_content: bool = False,
        include_images: bool = False,
        use_cache: bool = True,
    ) -> dict:
        """
        Internal search method to send the request to the API.
        """

        # Ensure query is within Tavily API limits
        truncated_query = self._truncate_query(query, max_length=400)
        if len(query) > 400:
            print(f"Query truncated from {len(query)} to {len(truncated_query)} characters for Tavily API")

        data = {
            "query": truncated_query,
            "search_depth": search_depth,
            "topic": topic,
            "days": days,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content,
            "max_results": max_results,
            "include_images": include_images,
            "api_key": self.api_key,
            "use_cache": use_cache,
        }
        
        # Only add domains if they are not None and not empty
        if include_domains is not None and include_domains:
            # Convert to list and filter out empty strings
            data["include_domains"] = [d for d in list(include_domains) if d]
        
        if exclude_domains is not None and exclude_domains:
            # Convert to list and filter out empty strings
            data["exclude_domains"] = [d for d in list(exclude_domains) if d]

        # Log the request for debugging
        if not self.api_key:
            raise ValueError("Tavily API key is not set. Please set TAVILY_API_KEY environment variable.")
        
        # Clean up the data dictionary to remove None values
        cleaned_data = {k: v for k, v in data.items() if v is not None}
        
        try:
            response = requests.post(
                self.base_url, 
                data=json.dumps(cleaned_data), 
                headers=self.headers, 
                timeout=150  # Increased timeout from 100 to 150 seconds
            )
        except requests.exceptions.Timeout:
            print(f"Tavily API timeout for query: {query}")
            raise Exception("Tavily API request timed out after 150 seconds")
        except requests.exceptions.RequestException as e:
            print(f"Tavily API request error: {e}")
            raise

        if response.status_code == 200:
            return response.json()
        else:
            # Log detailed error information
            error_msg = f"Tavily API error {response.status_code}: "
            try:
                error_detail = response.json()
                error_msg += json.dumps(error_detail)
            except:
                error_msg += response.text
            
            print(error_msg)
            
            # Raise specific errors for common issues
            if response.status_code == 422:
                raise ValueError(f"Invalid request parameters: {error_msg}")
            elif response.status_code == 400:
                raise ValueError(f"Bad request: {error_msg}")
            elif response.status_code == 401:
                raise ValueError("Invalid API key")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded")
            else:
                response.raise_for_status()

    def search(self, max_results=10):
        """
        Searches the query
        Returns:

        """
        try:
            # Search the query
            results = self._search(
                self.query,
                search_depth="basic",
                max_results=max_results,
                topic=self.topic,
                include_domains=self.query_domains,
            )
            sources = results.get("results", [])
            if not sources:
                raise Exception("No results found with Tavily API search.")
            # Return the results
            search_response = [
                {"href": obj["url"], "body": obj["content"]} for obj in sources
            ]
        except Exception as e:
            print(f"Error: {e}. Failed fetching sources. Resulting in empty response.")
            search_response = []
        return search_response
