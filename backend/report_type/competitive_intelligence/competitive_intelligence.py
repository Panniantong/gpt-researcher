from fastapi import WebSocket
from typing import Any, List, Optional, Dict
from urllib.parse import urlparse

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

        # 为竞品调研配置多搜索引擎：tavily + google
        # 这样可以获得更全面的搜索覆盖，特别是Google对某些平台的索引可能更好
        competitive_headers = self.headers.copy()
        if "retrievers" not in competitive_headers:
            competitive_headers["retrievers"] = "tavily,google"

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
            "headers": competitive_headers,  # 使用包含多搜索引擎配置的headers
        }
        
        # Add MCP parameters if provided
        if mcp_configs is not None:
            gpt_researcher_params["mcp_configs"] = mcp_configs
        if mcp_strategy is not None:
            gpt_researcher_params["mcp_strategy"] = mcp_strategy
            
        self.gpt_researcher = GPTResearcher(**gpt_researcher_params)

        # 定义关键平台优先级（用于结果过滤优化）
        # 针对tavily+google双搜索引擎，扩展平台覆盖范围
        self.priority_platforms = [
            # 核心创始人和团队信息平台
            "linkedin.com",
            "crunchbase.com",
            "angel.co",
            "angellist.com",

            # 用户反馈和社区讨论平台
            "reddit.com",
            "producthunt.com",
            "news.ycombinator.com",  # Hacker News
            "hackernews.com",

            # 创业和增长故事平台
            "indiehackers.com",
            "medium.com",
            "substack.com",

            # 技术和开发平台
            "github.com",
            "stackoverflow.com",
            "dev.to",

            # 专业评价和比较平台
            "g2.com",
            "capterra.com",
            "trustpilot.com",
            "getapp.com",

            # 新闻和媒体平台
            "techcrunch.com",
            "venturebeat.com",
            "theverge.com",
            "wired.com",

            # 视频和演示平台
            "youtube.com",
            "vimeo.com",

            # 其他有价值的平台
            "twitter.com",
            "x.com",
            "facebook.com",
            "blog.com",
            "wordpress.com"
        ]

    async def run(self):
        """
        Execute competitive intelligence research and generate report with platform optimization

        Returns:
            str: The generated competitive intelligence report
        """
        # Conduct research phase
        await self.gpt_researcher.conduct_research()

        # 第2步：结果过滤优化 - 重新排序研究上下文，优先展示关键平台信息
        if hasattr(self.gpt_researcher, 'context') and self.gpt_researcher.context:
            self.gpt_researcher.context = self._prioritize_platform_results(self.gpt_researcher.context)

        # 第3步：上下文增强 - 添加平台指导信息
        if hasattr(self.gpt_researcher, 'context') and self.gpt_researcher.context:
            enhanced_context = self._enhance_context_with_platform_guidance(self.gpt_researcher.context)
            self.gpt_researcher.context = enhanced_context

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
        Enhance query specifically for competitive intelligence research with platform-optimized queries

        Args:
            query (str): Original query

        Returns:
            str: Enhanced query with competitive intelligence focus and platform guidance
        """
        # 生成平台优化的查询，引导搜索引擎返回关键平台的结果
        platform_optimized_query = self._generate_platform_optimized_query(query)

        return platform_optimized_query

    def _generate_platform_optimized_query(self, product_name: str) -> str:
        """
        生成平台优化的查询，针对tavily+google双搜索引擎优化

        Args:
            product_name (str): 产品名称

        Returns:
            str: 优化后的查询，同时适配Tavily和Google搜索特性
        """
        # 提取纯产品名（去除URL等）
        clean_product_name = self._extract_clean_product_name(product_name)

        # 针对双搜索引擎的优化策略：
        # 1. Tavily: 使用关键词引导，提高相关平台内容返回概率
        # 2. Google: 支持site:语法，可以更精确地搜索特定平台

        # 基础查询：产品名 + 竞品分析
        base_query = f"{clean_product_name} competitive intelligence analysis"

        # 平台关键词（适用于Tavily和Google的通用搜索）
        platform_keywords = [
            "LinkedIn founder CEO team background",  # 创始人信息
            "Reddit review discussion user experience",  # 用户反馈
            "ProductHunt launch feedback community",  # 产品评价
            "IndieHackers growth story revenue model",  # 增长故事
            "Crunchbase funding investment valuation",  # 投资信息
            "GitHub repository code open source",  # 技术实现
            "startup company business model strategy"  # 商业模式
        ]

        # 组合优化查询
        # 这个查询既能让Tavily理解我们想要的内容类型，
        # 也能让Google通过关键词匹配找到相关平台的内容
        optimized_query = f"{base_query} {' '.join(platform_keywords)}"

        return optimized_query

    def _extract_clean_product_name(self, query: str) -> str:
        """
        从查询中提取干净的产品名称

        Args:
            query (str): 原始查询

        Returns:
            str: 清理后的产品名称
        """
        # 如果是URL，提取域名作为产品名
        if query.startswith(("http://", "https://", "www.")):
            try:
                parsed = urlparse(query if query.startswith("http") else f"https://{query}")
                domain = parsed.netloc.replace("www.", "")
                product_name = domain.split(".")[0].title()
                return product_name
            except:
                return query

        # 移除常见的后缀词
        clean_name = query.replace("(competitive intelligence analysis)", "").strip()
        clean_name = clean_name.replace("(product intelligence research for", "").strip()
        clean_name = clean_name.replace(")", "").strip()

        return clean_name

    def _prioritize_platform_results(self, context_data):
        """
        第2步：结果过滤优化 - 对研究上下文按平台重要性重新排序

        Args:
            context_data: 研究上下文数据

        Returns:
            重新排序后的上下文数据，关键平台信息优先
        """
        if not context_data:
            return context_data

        # 如果context是字符串，直接返回（某些情况下context可能是字符串格式）
        if isinstance(context_data, str):
            return context_data

        # 如果context是列表，按平台优先级排序
        if isinstance(context_data, list):
            priority_items = []
            other_items = []

            for item in context_data:
                # 检查item是否包含URL信息
                item_text = str(item)
                is_priority = False

                # 检查是否来自关键平台
                for platform in self.priority_platforms:
                    if platform in item_text.lower():
                        priority_items.append(item)
                        is_priority = True
                        break

                if not is_priority:
                    other_items.append(item)

            # 返回重新排序的结果：关键平台信息在前
            return priority_items + other_items

        # 其他情况直接返回原数据
        return context_data

    def _enhance_context_with_platform_guidance(self, context_data):
        """
        第3步：上下文增强 - 在研究上下文中添加平台分析指导

        Args:
            context_data: 原始研究上下文

        Returns:
            增强后的上下文，包含平台分析指导
        """
        if not context_data:
            return context_data

        # 平台分析指导文本（针对tavily+google双搜索引擎优化）
        platform_guidance = """

=== 多搜索引擎平台信息分析指导 ===

本次研究使用了Tavily + Google双搜索引擎，请特别关注并优先分析来自以下关键平台的信息：

🔍 **创始人和团队信息**：
- LinkedIn: 创始人背景、工作经历、教育背景、团队构成、职业网络
- Crunchbase: 公司团队信息、投资人关系、顾问团队、管理层变动
- AngelList: 早期团队构成、股权分配、招聘信息

👥 **用户反馈和市场认知**：
- Reddit: 真实用户讨论、使用体验、产品对比、问题反馈、社区口碑
- Product Hunt: 产品发布反馈、社区评价、功能讨论、竞品对比
- Hacker News: 技术社区讨论、开发者观点、行业趋势

📈 **增长和商业模式**：
- Indie Hackers: 增长故事、收入数据、营销策略、创业经验分享
- Medium/Substack: 创始人分享、增长复盘、行业洞察、战略思考

💻 **技术实现**：
- GitHub: 开源代码、技术栈、架构设计、开发活跃度、贡献者
- Stack Overflow: 技术问题、实现难点、开发者讨论
- Dev.to: 技术博客、开发经验、架构分享

💰 **投资和估值**：
- Crunchbase: 融资历史、投资轮次、估值信息、投资人背景
- AngelList: 早期投资、股权信息、投资条件

📊 **专业评价和比较**：
- G2/Capterra/GetApp: 专业用户评分、功能对比、竞品分析
- Trustpilot: 用户满意度、服务质量评价

📰 **媒体报道和行业分析**：
- TechCrunch/VentureBeat: 行业新闻、融资报道、产品发布
- The Verge/Wired: 深度分析、行业趋势、技术评测

🎥 **产品演示和教程**：
- YouTube: 产品演示、用户教程、评测视频、创始人访谈

**双搜索引擎优势分析**：
1. **Tavily优势**: 实时信息、AI优化的内容提取、相关性排序
2. **Google优势**: 全面的索引覆盖、精确的site:搜索、历史信息

**分析要求**：
1. 优先分析来自关键平台的信息，并明确标注信息来源和搜索引擎
2. 对比不同平台的信息，识别一致性和差异性
3. 重点关注时效性：标注信息获取时间，区分最新动态和历史信息
4. 如果某个重要维度缺少关键平台信息，请标注"⚠️ 信息不足，建议补充调研"

"""

        # 根据context_data的类型进行不同处理
        if isinstance(context_data, str):
            return context_data + platform_guidance
        elif isinstance(context_data, list):
            # 将指导信息作为第一个元素添加到列表中
            enhanced_context = [platform_guidance] + context_data
            return enhanced_context
        else:
            # 其他类型，尝试转换为字符串后添加指导
            return str(context_data) + platform_guidance


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
        Execute detailed competitive intelligence research and generate comprehensive report with platform optimization

        Returns:
            str: The generated detailed competitive intelligence report
        """
        # Enhance query for detailed research
        original_query = self.gpt_researcher.query
        self.gpt_researcher.query = self._enhance_query_for_detailed_research(original_query)

        # Conduct more thorough research phase
        await self.gpt_researcher.conduct_research()

        # 第2步：结果过滤优化 - 重新排序研究上下文，优先展示关键平台信息
        if hasattr(self.gpt_researcher, 'context') and self.gpt_researcher.context:
            self.gpt_researcher.context = self._prioritize_platform_results(self.gpt_researcher.context)

        # 第3步：上下文增强 - 添加平台指导信息（详细模式使用更全面的指导）
        if hasattr(self.gpt_researcher, 'context') and self.gpt_researcher.context:
            enhanced_context = self._enhance_context_with_detailed_platform_guidance(self.gpt_researcher.context)
            self.gpt_researcher.context = enhanced_context

        # Generate detailed competitive intelligence report
        report = await self.gpt_researcher.write_report()

        return report

    def _enhance_query_for_detailed_research(self, query: str) -> str:
        """
        Enhance query for detailed competitive intelligence research with deeper platform coverage

        Args:
            query (str): Original query

        Returns:
            str: Enhanced query for detailed analysis with expanded platform keywords
        """
        # 获取基础的平台优化查询
        base_query = self._generate_platform_optimized_query(query)

        # 为详细模式添加更多深度分析关键词
        detailed_keywords = [
            "financial metrics revenue model",
            "user acquisition growth strategy",
            "technology stack architecture",
            "competitive landscape market analysis",
            "investment funding valuation",
            "team background experience",
            "user feedback testimonials",
            "pricing strategy business model"
        ]

        # 组合详细查询
        detailed_query = f"{base_query} {' '.join(detailed_keywords)} deep analysis comprehensive research"

        return detailed_query

    def _enhance_context_with_detailed_platform_guidance(self, context_data):
        """
        为详细模式提供更全面的平台分析指导

        Args:
            context_data: 原始研究上下文

        Returns:
            增强后的上下文，包含详细的平台分析指导
        """
        if not context_data:
            return context_data

        # 详细模式的平台分析指导文本
        detailed_platform_guidance = """

=== 详细竞品情报分析指导 ===

在进行深度竞品分析时，请按照以下框架系统性地分析各平台信息：

🏢 **基础信息收集**：
- LinkedIn: 创始人完整背景、团队规模、关键员工、公司发展历程
- Crunchbase: 成立时间、总部位置、员工数量、业务模式、投资状态

👨‍💼 **创始人/团队深度分析**：
- LinkedIn: 教育背景、工作经历、行业经验、领导风格、网络关系
- Medium/个人博客: 创始人思考、价值观、战略观点
- Twitter: 行业影响力、观点表达、社交网络

📊 **八维商业分析**：
1. 市场定位: Reddit/HackerNews用户讨论、G2/Capterra专业评价
2. 产品功能: ProductHunt功能介绍、GitHub技术实现
3. 用户体验: Reddit真实反馈、App Store/Google Play评价
4. 商业模式: IndieHackers收入分享、公司博客商业策略
5. 技术架构: GitHub代码分析、技术博客架构分享
6. 团队能力: LinkedIn团队背景、Crunchbase团队信息
7. 资金状况: Crunchbase融资历史、新闻报道
8. 增长策略: IndieHackers增长故事、营销案例分析

📈 **营销情报深度挖掘**：
- IndieHackers: 增长时间线、用户获取策略、收入里程碑
- ProductHunt: 发布策略、社区反应、传播效果
- Reddit: 用户自发讨论、口碑传播、病毒式增长
- 社交媒体: 内容营销、社区建设、品牌传播

🔧 **复刻可行性评估**：
- GitHub: 技术复杂度、开源程度、技术栈分析
- 技术博客: 架构设计、技术选型、开发难点
- 招聘信息: 技术要求、团队规模、开发周期

💡 **Executive Summary要素**：
- 核心竞争优势识别
- 可复制的增长策略
- 技术实现的关键要点
- 市场机会和威胁分析

**分析深度要求**：
1. **定量分析**: 尽可能收集具体数字（用户数、收入、融资额、团队规模等）
2. **定性分析**: 深度解读策略思路、执行细节、成功因素
3. **时间维度**: 分析发展历程、关键节点、增长轨迹
4. **对比维度**: 与竞品对比、与行业标准对比
5. **风险评估**: 识别潜在风险、市场威胁、技术挑战

**信息验证要求**：
- 多源验证: 同一信息尽量从多个平台验证
- 时效性检查: 标注信息获取时间，识别过时信息
- 可信度评估: 区分官方信息、第三方评价、用户反馈
- 缺失标注: 明确标注信息不足的领域，建议补充调研方向

"""

        # 根据context_data的类型进行不同处理
        if isinstance(context_data, str):
            return context_data + detailed_platform_guidance
        elif isinstance(context_data, list):
            # 将详细指导信息作为第一个元素添加到列表中
            enhanced_context = [detailed_platform_guidance] + context_data
            return enhanced_context
        else:
            # 其他类型，尝试转换为字符串后添加指导
            return str(context_data) + detailed_platform_guidance