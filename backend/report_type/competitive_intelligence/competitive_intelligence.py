from fastapi import WebSocket
from typing import Any, List, Optional, Dict

from gpt_researcher import GPTResearcher


class CompetitiveIntelligenceReport:
    def __init__(
        self,
        query: str,
        query_domains: list = [],
        report_type: str = "competitive_intelligence",
        report_source: str = "web",
        source_urls: List[str] = [],
        document_urls: List[str] = [],
        tone: Any = "",
        config_path: str = None,
        websocket: WebSocket = None,
        headers: Optional[Dict] = None,
        mcp_configs=None,
        mcp_strategy=None,
    ):
        """
        Initialize Competitive Intelligence Report
        
        Args:
            query (str): Product name or URL to research
            query_domains (list): Domains to search within
            report_type (str): Type of competitive intelligence report
            report_source (str): Source of research data
            source_urls (List[str]): Specific URLs to include
            document_urls (List[str]): Document URLs to analyze
            tone: Writing tone for the report
            config_path (str): Path to configuration file
            websocket (WebSocket): WebSocket connection for real-time updates
            headers (Optional[Dict]): HTTP headers
            mcp_configs: MCP configurations
            mcp_strategy: MCP strategy
        """
        self.query = query
        self.query_domains = query_domains
        self.report_type = report_type
        self.report_source = report_source
        self.source_urls = source_urls
        self.document_urls = document_urls
        self.tone = tone
        self.config_path = config_path
        self.websocket = websocket
        self.headers = headers or {}

        # Initialize researcher with optional MCP parameters
        gpt_researcher_params = {
            "query": self.query,
            "query_domains": self.query_domains,
            "report_type": self.report_type,
            "report_source": self.report_source,
            "source_urls": self.source_urls,
            "document_urls": self.document_urls,
            "tone": self.tone,
            "config_path": self.config_path,
            "websocket": self.websocket,
            "headers": self.headers,
        }
        
        # Add MCP parameters if provided
        if mcp_configs is not None:
            gpt_researcher_params["mcp_configs"] = mcp_configs
        if mcp_strategy is not None:
            gpt_researcher_params["mcp_strategy"] = mcp_strategy
            
        self.gpt_researcher = GPTResearcher(**gpt_researcher_params)

    async def run(self):
        """
        Execute competitive intelligence research and generate report
        
        Returns:
            str: The generated competitive intelligence report
        """
        # Conduct research phase
        await self.gpt_researcher.conduct_research()
        
        # Generate competitive intelligence report
        report = await self.gpt_researcher.write_report()
        
        return report

    def _process_product_input(self, query: str) -> str:
        """
        Process product input (name or URL) and prepare for research
        
        Args:
            query (str): Product name or URL
            
        Returns:
            str: Processed query for research
        """
        # If query looks like a URL, extract additional context
        if query.startswith(("http://", "https://", "www.")):
            # For URL inputs, we might want to add the URL to source_urls
            if query not in self.source_urls:
                self.source_urls.append(query)
            
            # Extract product name from URL if possible
            try:
                from urllib.parse import urlparse
                parsed = urlparse(query)
                domain = parsed.netloc.replace("www.", "")
                product_name = domain.split(".")[0].title()
                return f"{product_name} (product intelligence research for {query})"
            except:
                return f"Product intelligence research for {query}"
        else:
            # For product names, enhance the query for better research
            return f"{query} (competitive intelligence analysis)"

    def _enhance_query_for_competitive_research(self, query: str) -> str:
        """
        Enhance query specifically for competitive intelligence research
        
        Args:
            query (str): Original query
            
        Returns:
            str: Enhanced query with competitive intelligence focus
        """
        enhanced_query = self._process_product_input(query)
        
        # Add competitive intelligence specific research angles
        research_angles = [
            "founder background",
            "business model",
            "market position",
            "competitive advantages",
            "growth strategy", 
            "funding history",
            "team information",
            "product features",
            "user reviews",
            "market share",
            "technical architecture"
        ]
        
        return f"{enhanced_query}. Research focus areas: {', '.join(research_angles)}"


class CompetitiveIntelligenceDetailedReport(CompetitiveIntelligenceReport):
    """
    Detailed version of Competitive Intelligence Report with more comprehensive analysis
    """
    
    def __init__(self, *args, **kwargs):
        # Set default report type to detailed version
        kwargs["report_type"] = kwargs.get("report_type", "competitive_intelligence_detailed")
        super().__init__(*args, **kwargs)

    async def run(self):
        """
        Execute detailed competitive intelligence research and generate comprehensive report
        
        Returns:
            str: The generated detailed competitive intelligence report
        """
        # Enhance query for detailed research
        original_query = self.gpt_researcher.query
        self.gpt_researcher.query = self._enhance_query_for_detailed_research(original_query)
        
        # Conduct more thorough research phase
        await self.gpt_researcher.conduct_research()
        
        # Generate detailed competitive intelligence report
        report = await self.gpt_researcher.write_report()
        
        return report

    def _enhance_query_for_detailed_research(self, query: str) -> str:
        """
        Enhance query for detailed competitive intelligence research
        
        Args:
            query (str): Original query
            
        Returns:
            str: Enhanced query for detailed analysis
        """
        enhanced_query = self._enhance_query_for_competitive_research(query)
        
        # Add detailed analysis specific research angles
        detailed_angles = [
            "financial metrics",
            "revenue model details",
            "user acquisition costs",
            "retention rates",
            "market size analysis",
            "competitive landscape",
            "technology stack",
            "intellectual property",
            "partnerships",
            "regulatory considerations",
            "scalability factors",
            "risk assessment"
        ]
        
        return f"{enhanced_query}. Additional detailed research areas: {', '.join(detailed_angles)}"