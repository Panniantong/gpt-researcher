"""
八维分析模块
实现产品竞品调研的八个分析维度
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from competitive_intelligence.utils.llm_helper import get_llm_response
from competitive_intelligence.prompts.competitive_prompts import (
    Q2_BROKEN_SPOT_PROMPT,
    Q3_USER_URGENCY_PROMPT,
    Q6_ARENA_SCORING_PROMPT,
    Q7_POSITIONING_PROMPT,
    Q8_ARCHITECTURE_PROMPT,
    SEARCH_QUERY_GENERATOR
)


@dataclass
class DimensionAnalysis:
    """单个维度的分析结果"""
    dimension: str
    question: str
    answer: str
    sources: List[str] = None
    requires_research: bool = False


class EightDimensionsAnalyzer:
    """八维分析器"""
    
    def __init__(self, llm_provider: str = None, model: str = None):
        self.llm_provider = llm_provider
        self.model = model
        
        # 定义八个维度
        self.dimensions = {
            "Q1": {
                "name": "One-sentence Pitch",
                "requires_research": False
            },
            "Q2": {
                "name": "Fixed 'Broken' Spot",
                "requires_research": True
            },
            "Q3": {
                "name": "User Urgency",
                "requires_research": True
            },
            "Q4": {
                "name": "Who-When-Action",
                "requires_research": False
            },
            "Q5": {
                "name": "Pain & Pain-level",
                "requires_research": False
            },
            "Q6": {
                "name": "Arena & Scoring Rule",
                "requires_research": True
            },
            "Q7": {
                "name": "First / Only / Number",
                "requires_research": True
            },
            "Q8": {
                "name": "Implementation Architecture",
                "requires_research": True
            }
        }
    
    async def analyze_all_dimensions(
        self,
        product_info: Dict[str, Any],
        research_results: Dict[str, List[Dict[str, Any]]] = None
    ) -> Dict[str, DimensionAnalysis]:
        """
        分析所有八个维度
        
        Args:
            product_info: 产品基础信息
            research_results: 各维度的研究结果（可选）
            
        Returns:
            八维分析结果字典
        """
        results = {}
        
        # Q1: One-sentence Pitch
        results["Q1"] = await self._analyze_q1(product_info)
        
        # Q2: Fixed "Broken" Spot
        if research_results and "Q2" in research_results:
            results["Q2"] = await self._analyze_q2(product_info, research_results["Q2"])
        else:
            results["Q2"] = self._create_placeholder("Q2", "需要搜索相关信息")
        
        # Q3: User Urgency
        if research_results and "Q3" in research_results:
            results["Q3"] = await self._analyze_q3(product_info, research_results["Q3"])
        else:
            results["Q3"] = self._create_placeholder("Q3", "需要搜索用户反馈")
        
        # Q4: Who-When-Action
        results["Q4"] = await self._analyze_q4(product_info)
        
        # Q5: Pain & Pain-level
        results["Q5"] = await self._analyze_q5(product_info)
        
        # Q6: Arena & Scoring Rule
        if research_results and "Q6" in research_results:
            results["Q6"] = await self._analyze_q6(product_info, research_results["Q6"])
        else:
            results["Q6"] = self._create_placeholder("Q6", "需要竞品分析")
        
        # Q7: First / Only / Number
        if research_results and "Q7" in research_results:
            results["Q7"] = await self._analyze_q7(product_info, research_results["Q7"])
        else:
            results["Q7"] = self._create_placeholder("Q7", "需要市场定位研究")
        
        # Q8: Implementation Architecture
        if research_results and "Q8" in research_results:
            results["Q8"] = await self._analyze_q8(product_info, research_results["Q8"])
        else:
            results["Q8"] = self._create_placeholder("Q8", "需要技术架构分析")
        
        # 将所有 DimensionAnalysis 对象转换为字典
        return {key: asdict(value) for key, value in results.items()}
    
    async def _analyze_q1(self, product_info: Dict[str, Any]) -> DimensionAnalysis:
        """Q1: One-sentence Pitch"""
        
        
        prompt = f"""
基于以下产品信息，用≤20字中文或≤140字英文写出核心价值主张：

产品名称：{product_info.get('name', '')}
产品描述：{product_info.get('one_liner', '')}
产品类型：{product_info.get('type', '')}

请直接输出一句话pitch，不要其他解释。
"""
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        
        return DimensionAnalysis(
            dimension="Q1",
            question="One-sentence Pitch",
            answer=response.strip(),
            requires_research=False
        )
    
    async def _analyze_q2(
        self, 
        product_info: Dict[str, Any],
        search_results: List[Dict[str, Any]]
    ) -> DimensionAnalysis:
        """Q2: Fixed 'Broken' Spot"""
        
        
        formatted_results = self._format_search_results(search_results)
        
        prompt = Q2_BROKEN_SPOT_PROMPT.format(
            product_name=product_info.get('name', ''),
            product_description=product_info.get('one_liner', ''),
            search_results=formatted_results
        )
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        sources = self._extract_sources(search_results)
        
        return DimensionAnalysis(
            dimension="Q2",
            question="Fixed 'Broken' Spot",
            answer=response,
            sources=sources,
            requires_research=True
        )
    
    async def _analyze_q3(
        self,
        product_info: Dict[str, Any],
        search_results: List[Dict[str, Any]]
    ) -> DimensionAnalysis:
        """Q3: User Urgency"""
        
        
        formatted_results = self._format_search_results(search_results)
        
        prompt = Q3_USER_URGENCY_PROMPT.format(
            product_name=product_info.get('name', ''),
            product_description=product_info.get('one_liner', ''),
            search_results=formatted_results
        )
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        sources = self._extract_sources(search_results)
        
        return DimensionAnalysis(
            dimension="Q3",
            question="User Urgency (Skin-in-the-Game)",
            answer=response,
            sources=sources,
            requires_research=True
        )
    
    async def _analyze_q4(self, product_info: Dict[str, Any]) -> DimensionAnalysis:
        """Q4: Who-When-Action"""
        
        
        prompt = f"""
基于以下产品信息，精准描述「谁-在什么场景-做什么动作」时会使用它：

产品名称：{product_info.get('name', '')}
产品描述：{product_info.get('one_liner', '')}
产品类型：{product_info.get('type', '')}

请用一句话回答，格式：[目标用户]在[具体场景]时[执行动作]
"""
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        
        return DimensionAnalysis(
            dimension="Q4",
            question="Who-When-Action",
            answer=response.strip(),
            requires_research=False
        )
    
    async def _analyze_q5(self, product_info: Dict[str, Any]) -> DimensionAnalysis:
        """Q5: Pain & Pain-level"""
        
        
        prompt = f"""
基于以下产品信息，分析用户痛点：

产品名称：{product_info.get('name', '')}
产品描述：{product_info.get('one_liner', '')}
产品类型：{product_info.get('type', '')}

请回答：
1. 一句话描述痛点
2. 用5-10字标记痛感等级（例：刚需/高频痛/偶发痒）

格式：
痛点：[描述]
等级：[等级]
"""
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        
        return DimensionAnalysis(
            dimension="Q5",
            question="Pain & Pain-level",
            answer=response.strip(),
            requires_research=False
        )
    
    async def _analyze_q6(
        self,
        product_info: Dict[str, Any],
        search_results: List[Dict[str, Any]]
    ) -> DimensionAnalysis:
        """Q6: Arena & Scoring Rule"""
        
        
        formatted_results = self._format_search_results(search_results)
        
        prompt = Q6_ARENA_SCORING_PROMPT.format(
            product_name=product_info.get('name', ''),
            product_type=product_info.get('type', ''),
            search_results=formatted_results
        )
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        sources = self._extract_sources(search_results)
        
        return DimensionAnalysis(
            dimension="Q6",
            question="Arena & Scoring Rule",
            answer=response,
            sources=sources,
            requires_research=True
        )
    
    async def _analyze_q7(
        self,
        product_info: Dict[str, Any],
        search_results: List[Dict[str, Any]]
    ) -> DimensionAnalysis:
        """Q7: First / Only / Number"""
        
        
        formatted_results = self._format_search_results(search_results)
        
        prompt = Q7_POSITIONING_PROMPT.format(
            product_name=product_info.get('name', ''),
            product_description=product_info.get('one_liner', ''),
            search_results=formatted_results
        )
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        sources = self._extract_sources(search_results)
        
        return DimensionAnalysis(
            dimension="Q7",
            question="First / Only / Number",
            answer=response,
            sources=sources,
            requires_research=True
        )
    
    async def _analyze_q8(
        self,
        product_info: Dict[str, Any],
        search_results: List[Dict[str, Any]]
    ) -> DimensionAnalysis:
        """Q8: Implementation Architecture"""
        
        
        # 从搜索结果中提取技术相关信息
        tech_info = self._extract_tech_info(search_results)
        
        prompt = Q8_ARCHITECTURE_PROMPT.format(
            product_name=product_info.get('name', ''),
            product_features=product_info.get('one_liner', ''),
            tech_info=tech_info
        )
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        sources = self._extract_sources(search_results)
        
        return DimensionAnalysis(
            dimension="Q8",
            question="Implementation Architecture",
            answer=response,
            sources=sources,
            requires_research=True
        )
    
    def _create_placeholder(self, dimension: str, message: str) -> DimensionAnalysis:
        """创建占位符分析结果"""
        return DimensionAnalysis(
            dimension=dimension,
            question=self.dimensions[dimension]["name"],
            answer=f"⚠︎ Info insufficient - {message}",
            requires_research=self.dimensions[dimension]["requires_research"]
        )
    
    def _format_search_results(self, results: List[Dict[str, Any]]) -> str:
        """格式化搜索结果"""
        formatted = []
        
        for i, result in enumerate(results[:10]):
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")
            
            formatted.append(f"""
Result {i+1}:
Title: {title}
URL: {url}
Content: {content[:300]}...
""")
        
        return "\n".join(formatted)
    
    def _extract_sources(self, results: List[Dict[str, Any]]) -> List[str]:
        """提取信息源"""
        return [r.get("url", "") for r in results if r.get("url")][:5]
    
    def _extract_tech_info(self, results: List[Dict[str, Any]]) -> str:
        """从搜索结果中提取技术信息"""
        tech_keywords = [
            "api", "technology", "built with", "tech stack", "architecture",
            "openai", "anthropic", "llm", "framework", "integration"
        ]
        
        tech_info = []
        
        for result in results:
            content = result.get("content", "").lower()
            if any(keyword in content for keyword in tech_keywords):
                tech_info.append(f"Source: {result.get('url', '')}\n{result.get('content', '')[:200]}")
        
        return "\n\n".join(tech_info) if tech_info else "No technical information found"
    
    async def generate_research_queries(
        self,
        product_info: Dict[str, Any],
        dimensions: List[str] = None
    ) -> Dict[str, List[str]]:
        """
        为需要研究的维度生成搜索查询
        
        Args:
            product_info: 产品信息
            dimensions: 要研究的维度列表（默认所有需要研究的维度）
            
        Returns:
            各维度的搜索查询字典
        """
        if dimensions is None:
            dimensions = [d for d, info in self.dimensions.items() if info["requires_research"]]
        
        queries = {}
        
        
        for dimension in dimensions:
            if dimension == "Q2":
                # Fixed "Broken" Spot 查询
                queries["Q2"] = [
                    f"{product_info['name']} solves problem",
                    f"{product_info['name']} vs traditional",
                    f"before {product_info['name']} pain point",
                    f"{product_info['name']} use case"
                ]
            
            elif dimension == "Q3":
                # User Urgency 查询
                queries["Q3"] = [
                    f"{product_info['name']} review",
                    f"{product_info['name']} testimonial",
                    f"{product_info['name']} user feedback",
                    f"{product_info['name']} pricing willing to pay"
                ]
            
            elif dimension == "Q6":
                # Arena & Scoring Rule 查询
                queries["Q6"] = [
                    f"{product_info['name']} competitors",
                    f"{product_info['name']} vs alternative",
                    f"{product_info['name']} comparison",
                    f"best {product_info.get('type', 'tool')} features"
                ]
            
            elif dimension == "Q7":
                # Positioning 查询
                queries["Q7"] = [
                    f"{product_info['name']} first market",
                    f"{product_info['name']} unique feature",
                    f"{product_info['name']} market leader",
                    f"{product_info['name']} innovation"
                ]
            
            elif dimension == "Q8":
                # Technical Architecture 查询
                queries["Q8"] = [
                    f"{product_info['name']} technology stack",
                    f"{product_info['name']} API",
                    f"{product_info['name']} architecture",
                    f"how {product_info['name']} works"
                ]
        
        return queries