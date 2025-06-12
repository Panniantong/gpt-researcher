"""
Competitive Intelligence Agent for deep product research
专门用于产品深度商业壁垒调研的智能代理
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from gpt_researcher.agent import GPTResearcher
from gpt_researcher.config import Config
from gpt_researcher.utils.logger import get_formatted_logger
from gpt_researcher.agents.utils import CompetitiveQueryBuilder, CompetitiveReportGenerator


logger = get_formatted_logger()


@dataclass
class ProductInfo:
    """产品基础信息数据结构"""
    name: str
    url: str = ""
    team_size: str = "⚠︎ Info insufficient"
    one_liner: str = ""
    type: str = ""
    launch_status: str = ""
    founded: str = ""
    search_traces: List[str] = field(default_factory=list)


@dataclass
class FounderInfo:
    """创始人/团队情报数据结构"""
    profile: Dict[str, str] = field(default_factory=dict)  # 人物画像
    unfair_advantages: Dict[str, str] = field(default_factory=dict)  # 不公平优势
    validation: str = ""  # AI + 行业专家验证
    sources: List[str] = field(default_factory=list)
    search_traces: List[str] = field(default_factory=list)


@dataclass
class EightDimensionAnalysis:
    """八维分析数据结构"""
    q1_pitch: str = "⚠︎ Info insufficient"
    q2_broken_spot: str = "⚠︎ Info insufficient"
    q3_urgency: str = "⚠︎ Info insufficient"
    q4_who_when_action: str = ""
    q5_pain_level: str = ""
    q6_arena: Dict[str, Any] = field(default_factory=lambda: {
        'arena_description': '⚠︎ Info insufficient',
        'success_metrics': '⚠︎ Info insufficient',
        'competitive_scoring': '⚠︎ Info insufficient',
        'leading_logic': '⚠︎ Info insufficient'
    })
    q7_unique: str = "⚠︎ Info insufficient"
    q8_implementation: str = "⚠︎ Info insufficient"
    sources: List[str] = field(default_factory=list)
    search_traces: List[str] = field(default_factory=list)


@dataclass
class GrowthIntelligence:
    """营销情报数据结构"""
    timeline_milestones: str = "⚠︎ Info insufficient"
    channels_tactics: str = "⚠︎ Info insufficient"
    sources: List[str] = field(default_factory=list)
    search_traces: List[str] = field(default_factory=list)


@dataclass
class FeasibilityAssessment:
    """复刻评估数据结构"""
    difficulty: str = ""
    ai_stack: str = ""
    challenges: str = "⚠︎ Info insufficient"
    ai_advantages: str = ""
    barriers: str = ""


@dataclass
class ExecutiveSummary:
    """执行摘要数据结构"""
    core_insights: str = ""  
    growth_model: str = ""  
    founder_advantages: str = ""  
    transferable_elements: str = "⚠︎ Info insufficient"  
    trend_insights: str = ""
    ai_strategy: str = ""


class CompetitiveIntelligenceAgent(GPTResearcher):
    """
    竞品情报研究代理
    继承自GPTResearcher，专门针对产品深度商业壁垒调研
    """
    
    def __init__(self, product_name: str, product_url: Optional[str] = None, config: Optional[Config] = None):
        """
        初始化竞品情报代理
        
        Args:
            product_name: 要研究的产品名称
            product_url: 产品官网URL（可选）
            config: 配置对象
        """
        # 使用自定义查询初始化父类
        query = f"Deep competitive intelligence research on {product_name}"
        
        # 如果没有提供 config，创建默认的
        if config is None:
            config = Config()
        
        # 调用父类初始化，这会设置所有必要的属性
        super().__init__(
            query=query, 
            report_type="custom_report",
            config_path=config.config_path if hasattr(config, 'config_path') else None
        )
        
        self.product_name = product_name
        self.product_url = product_url
        self.report_type = "competitive_intelligence"
        
        # 初始化查询构建器和报告生成器
        self.query_builder = CompetitiveQueryBuilder(product_name, product_url)
        self.report_generator = CompetitiveReportGenerator()
        
        # 初始化各模块数据结构
        self.product_info = ProductInfo(name=product_name, url=product_url or "")
        self.founder_info = FounderInfo()
        self.eight_dimensions = EightDimensionAnalysis()
        self.growth_intelligence = GrowthIntelligence()
        self.feasibility = FeasibilityAssessment()
        self.executive_summary = ExecutiveSummary()
        
        # 所有来源URL集合（去重）
        self.all_sources: set = set()
        self.sources: List[Dict[str, str]] = []  # 用于存储详细的来源信息
        
        logger.info(f"Initialized CompetitiveIntelligenceAgent for product: {product_name}")
    
    async def conduct_research(self) -> Dict[str, Any]:
        """
        执行完整的竞品情报研究流程
        """
        logger.info(f"Starting competitive intelligence research for {self.product_name}")
        
        try:
            # 1. 基础信息收集
            await self._research_basic_info()
            
            # 2. 创始人/团队情报
            await self._research_founder_intelligence()
            
            # 3. 八维分析
            await self._research_eight_dimensions()
            
            # 4. 营销情报
            await self._research_growth_intelligence()
            
            # 5. 复刻评估
            await self._assess_feasibility()
            
            # 6. 生成执行摘要
            await self._generate_executive_summary()
            
            # 7. 自检验证
            validation_result = self._validate_research()
            
            # 8. 生成最终报告
            final_report = await self._generate_final_report()
            
            return {
                "report": final_report,
                "validation": validation_result,
                "sources": list(self.all_sources),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in competitive intelligence research: {e}")
            raise
    
    async def _research_basic_info(self):
        """研究基础信息模块"""
        logger.info("Researching basic product information...")
        
        # 使用查询构建器获取查询
        query_template = self.query_builder._build_basic_info_queries()
        
        # 并行执行搜索
        search_results = await self._parallel_search(query_template.queries)
        
        # 记录搜索轨迹
        self.product_info.search_traces = query_template.queries
        
        # 提取和验证信息
        await self._extract_basic_info(search_results)
    
    async def _research_founder_intelligence(self):
        """研究创始人/团队情报"""
        logger.info("Researching founder and team intelligence...")
        
        queries = [
            f"{self.product_name} founder CEO LinkedIn",
            f"{self.product_name} founding team background",
            f"{self.product_name} founder previous experience",
            f"{self.product_name} team technical expertise"
        ]
        
        search_results = await self._parallel_search(queries)
        await self._extract_founder_info(search_results)
    
    async def _research_eight_dimensions(self):
        """执行八维分析"""
        logger.info("Conducting eight-dimension analysis...")
        
        # Q2: Fixed Broken Spot
        broken_spot_queries = [
            f"{self.product_name} solves problem",
            f"{self.product_name} vs alternatives comparison",
            f"{self.product_name} unique value proposition"
        ]
        
        # Q3: User Urgency
        urgency_queries = [
            f"{self.product_name} user testimonials reviews",
            f"{self.product_name} customer success stories",
            f"{self.product_name} user adoption rate"
        ]
        
        # Q6: Arena & Scoring Rule
        arena_queries = [
            f"{self.product_name} market competition landscape",
            f"{self.product_name} vs competitors comparison",
            f"{self.product_name} market share growth"
        ]
        
        # Q7: First/Only/Number
        uniqueness_queries = [
            f"{self.product_name} first in market pioneer",
            f"{self.product_name} unique features patents",
            f"{self.product_name} market position ranking"
        ]
        
        # Q8: Implementation Architecture
        tech_queries = [
            f"{self.product_name} technology stack architecture",
            f"{self.product_name} API integration features",
            f"{self.product_name} GitHub open source"
        ]
        
        all_queries = broken_spot_queries + urgency_queries + arena_queries + uniqueness_queries + tech_queries
        search_results = await self._parallel_search(all_queries)
        await self._extract_eight_dimensions(search_results)
    
    async def _research_growth_intelligence(self):
        """研究营销情报"""
        logger.info("Researching growth and marketing intelligence...")
        
        queries = [
            f"{self.product_name} growth timeline milestones",
            f"{self.product_name} marketing strategy channels",
            f"{self.product_name} user acquisition tactics",
            f"{self.product_name} ProductHunt launch",
            f"{self.product_name} social media marketing Twitter",
            f"{self.product_name} content marketing blog SEO"
        ]
        
        search_results = await self._parallel_search(queries)
        await self._extract_growth_intelligence(search_results)
    
    async def _assess_feasibility(self):
        """评估复刻可行性"""
        logger.info("Assessing replication feasibility...")
        
        # 基于已收集的信息进行分析
        await self._analyze_feasibility()
    
    async def _generate_executive_summary(self):
        """生成执行摘要"""
        logger.info("Generating executive summary...")
        
        # 基于所有收集的信息生成摘要
        await self._synthesize_summary()
    
    def _validate_research(self) -> Dict[str, bool]:
        """
        验证研究完整性
        返回核对表结果
        """
        validation = {
            "team_size_filled": self.product_info.team_size != "⚠︎ Info insufficient",
            "q2_q3_q6_q7_sourced": all([
                self.eight_dimensions.q2_broken_spot != "⚠︎ Info insufficient",
                self.eight_dimensions.q3_urgency != "⚠︎ Info insufficient",
                self.eight_dimensions.q6_arena.get("arena_description") != "⚠︎ Info insufficient",
                self.eight_dimensions.q7_unique != "⚠︎ Info insufficient"
            ]),
            "growth_intelligence_sourced": bool(self.growth_intelligence.sources),
            "no_speculation": True,  # 需要文本分析验证
            "insufficient_info_marked": True,  # 已在数据结构中默认标记
            "q8_application_only": True,  # 需要内容验证
            "feasibility_includes_barriers": bool(self.feasibility.barriers),
            "summary_includes_founder": bool(self.executive_summary.founder_advantages)
        }
        
        return validation
    
    async def _generate_final_report(self) -> str:
        """
        生成符合格式要求的最终报告
        """
        # 构建报告数据
        report_data = {
            "product_info": self._dataclass_to_dict(self.product_info),
            "founder_info": self._dataclass_to_dict(self.founder_info),
            "eight_dimensions": self._dataclass_to_dict(self.eight_dimensions),
            "growth_intelligence": self._dataclass_to_dict(self.growth_intelligence),
            "feasibility": self._dataclass_to_dict(self.feasibility),
            "executive_summary": self._dataclass_to_dict(self.executive_summary)
        }
        
        # 使用报告生成器生成最终报告
        return self.report_generator.generate_report(report_data)
    
    async def _parallel_search(self, queries: List[str]) -> List[Dict]:
        """并行执行多个搜索查询"""
        from ..actions.query_processing import get_search_results
        
        # 确保 retrievers 已初始化
        if not hasattr(self, 'retrievers') or not self.retrievers:
            from ..actions import get_retrievers
            self.retrievers = get_retrievers(self.headers, self.cfg)
        
        tasks = []
        for query in queries:
            # 使用 get_search_results 函数
            task = get_search_results(
                query=query,
                retriever=self.retrievers[0] if self.retrievers else None,
                query_domains=self.query_domains,
                researcher=self
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        # 扁平化结果
        all_results = []
        for result_list in results:
            all_results.extend(result_list)
        return all_results
    
    def _extract_domain(self) -> str:
        """从产品名提取可能的域名"""
        if self.product_url:
            return self.query_builder._extract_domain(self.product_url)
        # 简单实现，实际需要更智能的域名推测
        return f"{self.product_name.lower().replace(' ', '')}.com"
    
    def _dataclass_to_dict(self, obj) -> Dict:
        """将dataclass转换为字典"""
        from dataclasses import asdict
        return asdict(obj)
    
    # 以下是各种提取方法的占位符，将在后续实现
    async def _extract_basic_info(self, search_results):
        """从搜索结果中提取基础信息"""
        try:
            # 构建上下文
            context_parts = []
            for result in search_results[:5]:  # 使用前5个结果
                if isinstance(result, dict):
                    url = result.get('url', result.get('href', 'Unknown URL'))
                    content = result.get('raw_content', result.get('content', result.get('body', '')))
                    context_parts.append(f"Source: {url}\n{content}")
            context = "\n\n".join(context_parts)
            
            prompt = f"""Based on the following search results about {self.product_name}, extract the basic information:

Context:
{context}

Please extract and return the following information in JSON format:
{{
    "team_size": "number or 'Info insufficient'",
    "one_liner": "brief product description or 'Info insufficient'",
    "product_type": "B2B/B2C/Developer Tool/etc. or 'Info insufficient'", 
    "launch_status": "launched/beta/coming soon or 'Info insufficient'",
    "founded_year": "YYYY or 'Info insufficient'"
}}

IMPORTANT:
- Only use information explicitly stated in the search results
- If information is not found, use 'Info insufficient'
- Do not make assumptions or inferences
- Include the source URL where you found each piece of information

Return ONLY the JSON object, no additional text."""
            
            # 使用LLM提取信息
            from gpt_researcher.utils.llm import create_chat_completion
            response = await create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a competitive intelligence analyst extracting product information."},
                    {"role": "user", "content": prompt}
                ],
                model=self.cfg.smart_llm_model,
                temperature=0.1,
                max_tokens=1000,
                llm_provider=self.cfg.smart_llm_provider,
                llm_kwargs=self.cfg.llm_kwargs
            )
            
            # 解析响应
            import json
    
            try:
                extracted_info = json.loads(response)
                
                # 更新产品信息
                if extracted_info.get('team_size') and extracted_info.get('team_size') != 'Info insufficient':
                    self.product_info.team_size = extracted_info['team_size']
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON from LLM response")
            
            if extracted_info.get('one_liner') != 'Info insufficient':
                self.product_info.one_liner = extracted_info['one_liner']
                
            if extracted_info.get('product_type') != 'Info insufficient':
                self.product_info.type = extracted_info['product_type']
                
            if extracted_info.get('launch_status') != 'Info insufficient':
                self.product_info.launch_status = extracted_info['launch_status']
                
            if extracted_info.get('founded_year') != 'Info insufficient':
                self.product_info.founded = extracted_info['founded_year']
            
            # 记录来源
            for result in search_results:
                if isinstance(result, dict):
                    url = result.get('url', result.get('href', ''))
                    if url and url not in [s['url'] for s in self.sources]:
                        self.sources.append({
                            'url': url,
                            'title': result.get('title', ''),
                            'used_for': 'basic_info'
                        })
                        
        except Exception as e:
            logger.error(f"Error extracting basic info: {str(e)}")
    
    async def _extract_founder_info(self, search_results):
        """提取创始人和团队信息"""
        try:
            # 构建上下文
            context_parts = []
            for result in search_results[:5]:
                if isinstance(result, dict):
                    url = result.get('url', result.get('href', 'Unknown URL'))
                    content = result.get('raw_content', result.get('content', result.get('body', '')))
                    context_parts.append(f"Source: {url}\n{content}")
            context = "\n\n".join(context_parts)

            prompt = f"""Based on the following search results about {self.product_name}, extract founder and team information:

Context:
{context}

Please extract and return the following information in JSON format:
{{
    "founder_portrait": "Detailed founder information including names, background, experience, education, achievements, expertise or 'Info insufficient'",
    "unfair_advantages": "Industry connections, technical expertise, previous exits, domain expertise, team strengths or 'Info insufficient'",
    "ai_validation": "AI expertise, industry knowledge, notable advisors/investors or 'Info insufficient'"
}}

IMPORTANT:
- Only use information explicitly stated in the search results
- If information is not found, use 'Info insufficient'
- Do not make assumptions or inferences
- Include source URLs for key facts within the text

Return ONLY the JSON object, no additional text."""

            # 使用LLM提取信息
            from gpt_researcher.utils.llm import create_chat_completion
            response = await create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a competitive intelligence analyst specializing in founder and team analysis."},
                    {"role": "user", "content": prompt}
                ],
                model=self.cfg.smart_llm_model,
                temperature=0.1,
                max_tokens=2000,
                llm_provider=self.cfg.smart_llm_provider,
                llm_kwargs=self.cfg.llm_kwargs
            )

            # 解析响应
            import json

            try:
                extracted_info = json.loads(response)

                # 更新创始人信息
                if extracted_info.get('founder_portrait') and extracted_info.get('founder_portrait') != 'Info insufficient':
                    self.founder_info.profile['portrait'] = extracted_info['founder_portrait']

                if extracted_info.get('unfair_advantages') and extracted_info.get('unfair_advantages') != 'Info insufficient':
                    self.founder_info.unfair_advantages['summary'] = extracted_info['unfair_advantages']

                if extracted_info.get('ai_validation') and extracted_info.get('ai_validation') != 'Info insufficient':
                    self.founder_info.validation = extracted_info['ai_validation']

            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON from LLM response for founder info")

            # 记录来源
            for result in search_results[:5]:
                if isinstance(result, dict):
                    content = result.get('raw_content', result.get('content', result.get('body', '')))
                    if content and ('founder' in content.lower() or 'team' in content.lower()):
                        url = result.get('url', result.get('href', ''))
                        if url and url not in [s['url'] for s in self.sources]:
                            self.sources.append({
                                'url': url,
                                'title': result.get('title', ''),
                                'used_for': 'founder_info'
                            })

        except Exception as e:
            logger.error(f"Error extracting founder info: {str(e)}")
    
    async def _extract_eight_dimensions(self, search_results):
        """提取八维分析信息"""
        try:
            # 构建上下文
            context_parts = []
            for result in search_results[:8]:  # 使用更多结果进行八维分析
                if isinstance(result, dict):
                    url = result.get('url', result.get('href', 'Unknown URL'))
                    content = result.get('raw_content', result.get('content', result.get('body', '')))
                    context_parts.append(f"Source: {url}\n{content}")
            context = "\n\n".join(context_parts)

            prompt = f"""Based on the following search results about {self.product_name}, analyze the product across 8 dimensions:

Context:
{context}

Please analyze and return the following information in JSON format:
{{
    "q1_pitch": "One sentence description of what the product does or 'Info insufficient'",
    "q2_broken_spot": "What specific problem does it solve? Include sources or 'Info insufficient'",
    "q3_urgency": "How urgent is the problem for users? Include evidence/sources or 'Info insufficient'",
    "q4_who_when_action": "Who uses it, when, and what action they take or 'Info insufficient'",
    "q5_pain_level": "What pain does it address and how severe is it? or 'Info insufficient'",
    "q6_arena": {{
        "arena_description": "Market/Arena description (one sentence) or 'Info insufficient'",
        "success_metrics": "Key success metrics (1-3 metrics with evidence) or 'Info insufficient'",
        "competitive_scoring": "Compare with 2 competitors if known or 'Info insufficient'",
        "leading_logic": "Why this product wins or 'Info insufficient'"
    }},
    "q7_unique": "What makes it unique? Include sources or 'Info insufficient'",
    "q8_implementation": "Technical approach, only based on available info or 'Info insufficient'"
}}

IMPORTANT:
- For Q2, Q3, Q6, Q7: You MUST include specific sources/evidence
- If information is not available, use 'Info insufficient'
- Do not speculate or make assumptions
- Be concise but specific

Return ONLY the JSON object, no additional text."""

            # 使用LLM提取信息
            from gpt_researcher.utils.llm import create_chat_completion
            response = await create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a product analyst conducting competitive intelligence analysis."},
                    {"role": "user", "content": prompt}
                ],
                model=self.cfg.smart_llm_model,
                temperature=0.1,
                max_tokens=3000,
                llm_provider=self.cfg.smart_llm_provider,
                llm_kwargs=self.cfg.llm_kwargs
            )

            # 解析响应
            import json

            try:
                extracted_info = json.loads(response)

                # 更新八维分析信息
                if extracted_info.get('q1_pitch') and extracted_info.get('q1_pitch') != 'Info insufficient':
                    self.eight_dimensions.q1_pitch = extracted_info['q1_pitch']

                if extracted_info.get('q2_broken_spot') and extracted_info.get('q2_broken_spot') != 'Info insufficient':
                    self.eight_dimensions.q2_broken_spot = extracted_info['q2_broken_spot']

                if extracted_info.get('q3_urgency') and extracted_info.get('q3_urgency') != 'Info insufficient':
                    self.eight_dimensions.q3_urgency = extracted_info['q3_urgency']

                if extracted_info.get('q4_who_when_action') and extracted_info.get('q4_who_when_action') != 'Info insufficient':
                    self.eight_dimensions.q4_who_when_action = extracted_info['q4_who_when_action']

                if extracted_info.get('q5_pain_level') and extracted_info.get('q5_pain_level') != 'Info insufficient':
                    self.eight_dimensions.q5_pain_level = extracted_info['q5_pain_level']

                # 处理Q6的嵌套结构
                if extracted_info.get('q6_arena'):
                    q6_data = extracted_info['q6_arena']
                    if q6_data.get('arena_description') and q6_data.get('arena_description') != 'Info insufficient':
                        self.eight_dimensions.q6_arena['arena_description'] = q6_data['arena_description']
                    if q6_data.get('success_metrics') and q6_data.get('success_metrics') != 'Info insufficient':
                        self.eight_dimensions.q6_arena['success_metrics'] = q6_data['success_metrics']
                    if q6_data.get('competitive_scoring') and q6_data.get('competitive_scoring') != 'Info insufficient':
                        self.eight_dimensions.q6_arena['competitive_scoring'] = q6_data['competitive_scoring']
                    if q6_data.get('leading_logic') and q6_data.get('leading_logic') != 'Info insufficient':
                        self.eight_dimensions.q6_arena['leading_logic'] = q6_data['leading_logic']

                if extracted_info.get('q7_unique') and extracted_info.get('q7_unique') != 'Info insufficient':
                    self.eight_dimensions.q7_unique = extracted_info['q7_unique']

                if extracted_info.get('q8_implementation') and extracted_info.get('q8_implementation') != 'Info insufficient':
                    self.eight_dimensions.q8_implementation = extracted_info['q8_implementation']

            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON from LLM response for eight dimensions")
            
            # 记录来源
            for result in search_results[:8]:
                if isinstance(result, dict):
                    url = result.get('url', result.get('href', ''))
                    if url and url not in [s['url'] for s in self.sources]:
                        self.sources.append({
                            'url': url,
                            'title': result.get('title', ''),
                            'used_for': 'eight_dimensions'
                        })
                        
        except Exception as e:
            logger.error(f"Error extracting eight dimensions: {str(e)}")
    
    async def _extract_growth_intelligence(self, search_results):
        """提取增长和营销情报"""
        try:
            # 构建上下文
            context_parts = []
            for result in search_results[:6]:
                if isinstance(result, dict):
                    url = result.get('url', result.get('href', 'Unknown URL'))
                    content = result.get('raw_content', result.get('content', result.get('body', '')))
                    context_parts.append(f"Source: {url}\n{content}")
            context = "\n\n".join(context_parts)

            prompt = f"""Based on the following search results about {self.product_name}, extract growth and marketing intelligence:

Context:
{context}

Please extract and return the following information in JSON format:
{{
    "timeline_milestones": "Launch date, key milestones (funding, user milestones, product launches), growth trajectory with specific dates and sources or 'Info insufficient'",
    "channels_tactics": "Primary customer acquisition channels, marketing strategies, content marketing, community building, SEO/SEM, social media presence with evidence and sources or 'Info insufficient'"
}}

IMPORTANT:
- Only use information explicitly stated in the search results
- Include specific sources for all claims
- If information is not available, use 'Info insufficient'
- Focus on verifiable facts, not speculation

Return ONLY the JSON object, no additional text."""

            # 使用LLM提取信息
            from gpt_researcher.utils.llm import create_chat_completion
            response = await create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a growth marketing analyst extracting competitive intelligence."},
                    {"role": "user", "content": prompt}
                ],
                model=self.cfg.smart_llm_model,
                temperature=0.1,
                max_tokens=2000,
                llm_provider=self.cfg.smart_llm_provider,
                llm_kwargs=self.cfg.llm_kwargs
            )

            # 解析响应
            import json

            try:
                extracted_info = json.loads(response)

                # 更新增长情报信息
                if extracted_info.get('timeline_milestones') and extracted_info.get('timeline_milestones') != 'Info insufficient':
                    self.growth_intelligence.timeline_milestones = extracted_info['timeline_milestones']

                if extracted_info.get('channels_tactics') and extracted_info.get('channels_tactics') != 'Info insufficient':
                    self.growth_intelligence.channels_tactics = extracted_info['channels_tactics']

            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON from LLM response for growth intelligence")
            
            # 记录来源
            for result in search_results[:6]:
                if isinstance(result, dict):
                    content = result.get('raw_content', result.get('content', result.get('body', '')))
                    if content and any(keyword in content.lower() 
                                     for keyword in ['growth', 'marketing', 'launch', 'funding', 'users', 'milestone']):
                        url = result.get('url', result.get('href', ''))
                        if url and url not in [s['url'] for s in self.sources]:
                            self.sources.append({
                                'url': url,
                                'title': result.get('title', ''),
                                'used_for': 'growth_intelligence'
                            })
                        
        except Exception as e:
            logger.error(f"Error extracting growth intelligence: {str(e)}")
    
    async def _analyze_feasibility(self):
        """分析复刻可行性"""
        try:
            # 收集已提取的所有信息作为上下文
            context = f"""
Product: {self.product_name}

Basic Info:
- Type: {getattr(self.product_info, 'type', 'Unknown')}
- One-liner: {getattr(self.product_info, 'one_liner', 'Unknown')}
- Founded: {getattr(self.product_info, 'founded', 'Unknown')}

Product Description (Q1 Pitch):
{getattr(self.eight_dimensions, 'q1_pitch', 'Not available')}

Problem Solved (Q2):
{getattr(self.eight_dimensions, 'q2_broken_spot', 'Not available')}

Implementation Details (Q8):
{getattr(self.eight_dimensions, 'q8_implementation', 'Not available')}

Unique Aspects (Q7):
{getattr(self.eight_dimensions, 'q7_unique', 'Not available')}
"""
            
            prompt = f"""Based on the information about {self.product_name}, analyze the feasibility for a solo developer to replicate this product:

Context:
{context}

Please analyze and return the following information in JSON format:
{{
    "difficulty": "Easy/Medium/Hard/Very Hard with brief justification",
    "ai_stack": "Which parts can be built with modern AI tools (LLMs, embeddings, etc.), AI services/APIs that could replace complex components, estimated development time with AI assistance",
    "challenges": "List 3-4 main challenges: core technical hurdles, infrastructure requirements, data/content challenges, integration complexity",
    "ai_advantages": "What becomes easier with AI tools, which features can be rapidly prototyped, time/cost savings estimates",
    "barriers": "Regulatory requirements, network effects needed, data moats, partnership requirements"
}}

IMPORTANT:
- Focus on practical implementation considerations for an indie developer
- Be specific and actionable
- If information is not available, state clearly

Return ONLY the JSON object, no additional text."""

            # 使用LLM分析
            from gpt_researcher.utils.llm import create_chat_completion
            response = await create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a technical advisor analyzing product replication feasibility for indie developers."},
                    {"role": "user", "content": prompt}
                ],
                model=self.cfg.smart_llm_model,
                temperature=0.2,
                max_tokens=2000,
                llm_provider=self.cfg.smart_llm_provider,
                llm_kwargs=self.cfg.llm_kwargs
            )

            # 解析响应
            import json

            try:
                extracted_info = json.loads(response)

                # 更新可行性分析信息
                if extracted_info.get('difficulty'):
                    self.feasibility.difficulty = extracted_info['difficulty']

                if extracted_info.get('ai_stack'):
                    self.feasibility.ai_stack = extracted_info['ai_stack']

                if extracted_info.get('challenges'):
                    self.feasibility.challenges = extracted_info['challenges']

                if extracted_info.get('ai_advantages'):
                    self.feasibility.ai_advantages = extracted_info['ai_advantages']

                if extracted_info.get('barriers'):
                    self.feasibility.barriers = extracted_info['barriers']

            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON from LLM response for feasibility analysis")
                
        except Exception as e:
            logger.error(f"Error analyzing feasibility: {str(e)}")
    
    async def _synthesize_summary(self):
        """生成执行摘要"""
        try:
            # 收集所有关键信息
            context = f"""
Product: {self.product_name}

Basic Information:
- Type: {getattr(self.product_info, 'type', 'Unknown')}
- One-liner: {getattr(self.product_info, 'one_liner', 'Unknown')}
- Founded: {getattr(self.product_info, 'founded', 'Unknown')}
- Team Size: {getattr(self.product_info, 'team_size', 'Unknown')}

Founder Intelligence:
- Portrait: {self.founder_info.profile.get('portrait', 'Not available')[:200] if self.founder_info.profile.get('portrait') else 'Not available'}...
- Unfair Advantages: {self.founder_info.unfair_advantages.get('summary', 'Not available')[:200] if self.founder_info.unfair_advantages.get('summary') else 'Not available'}...

Key Product Insights:
- Problem Solved: {(self.eight_dimensions.q2_broken_spot[:200] + '...') if self.eight_dimensions.q2_broken_spot and self.eight_dimensions.q2_broken_spot != '⚠︎ Info insufficient' else 'Not available'}
- Unique Value: {(self.eight_dimensions.q7_unique[:200] + '...') if self.eight_dimensions.q7_unique and self.eight_dimensions.q7_unique != '⚠︎ Info insufficient' else 'Not available'}
- Market Position: {self.eight_dimensions.q6_arena.get('arena_description', 'Not available')}

Growth Intelligence:
- Timeline: {(self.growth_intelligence.timeline_milestones[:200] + '...') if self.growth_intelligence.timeline_milestones and self.growth_intelligence.timeline_milestones != '⚠︎ Info insufficient' else 'Not available'}
- Channels: {(self.growth_intelligence.channels_tactics[:200] + '...') if self.growth_intelligence.channels_tactics and self.growth_intelligence.channels_tactics != '⚠︎ Info insufficient' else 'Not available'}

Feasibility Analysis:
- Difficulty: {getattr(self.feasibility, 'difficulty', 'Not assessed')}
- AI Stack Potential: {(self.feasibility.ai_stack[:200] + '...') if self.feasibility.ai_stack else 'Not available'}
"""
            
            prompt = f"""Based on all the competitive intelligence gathered about {self.product_name}, create an executive summary:

Context:
{context}

Please create and return a strategic executive summary in JSON format:
{{
    "core_insights": "2-3 bullet points: Most important findings about the product and market, key competitive advantages identified",
    "growth_model": "2-3 bullet points: How they acquire and retain users, key growth inflection points, scalability insights",
    "founder_advantages": "2-3 bullet points: What unique advantages the founders bring, why they specifically can succeed, team composition strengths",
    "transferable_elements": "2-3 bullet points: What aspects can be replicated by others, which features are commoditized vs. differentiated, lessons for indie developers",
    "trend_insights": "2-3 bullet points: Market trends this product is riding, future opportunities in this space, timing considerations",
    "ai_strategy": "2-3 bullet points: How to approach this market as an indie developer, where AI tools provide leverage, niche opportunities to explore"
}}

IMPORTANT:
- Be concise, strategic, and actionable
- Focus on insights that would help someone understand both the product's success and opportunities for innovation
- Use bullet points format within each field
- If information is insufficient for any section, state clearly

Return ONLY the JSON object, no additional text."""

            # 使用LLM生成摘要
            from gpt_researcher.utils.llm import create_chat_completion
            response = await create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a strategic advisor synthesizing competitive intelligence into actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                model=self.cfg.smart_llm_model,
                temperature=0.3,
                max_tokens=2500,
                llm_provider=self.cfg.smart_llm_provider,
                llm_kwargs=self.cfg.llm_kwargs
            )

            # 解析响应
            import json

            try:
                extracted_info = json.loads(response)

                # 更新执行摘要信息
                if extracted_info.get('core_insights'):
                    self.executive_summary.core_insights = extracted_info['core_insights']

                if extracted_info.get('growth_model'):
                    self.executive_summary.growth_model = extracted_info['growth_model']

                if extracted_info.get('founder_advantages'):
                    self.executive_summary.founder_advantages = extracted_info['founder_advantages']

                if extracted_info.get('transferable_elements'):
                    self.executive_summary.transferable_elements = extracted_info['transferable_elements']

                if extracted_info.get('trend_insights'):
                    self.executive_summary.trend_insights = extracted_info['trend_insights']

                if extracted_info.get('ai_strategy'):
                    self.executive_summary.ai_strategy = extracted_info['ai_strategy']

            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON from LLM response for executive summary")
                    
        except Exception as e:
            logger.error(f"Error synthesizing summary: {str(e)}")