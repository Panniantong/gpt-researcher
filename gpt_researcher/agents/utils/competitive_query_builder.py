"""
Query builder for competitive intelligence research
为竞品情报研究构建专门的查询策略
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class QueryTemplate:
    """查询模板数据结构"""
    module: str
    queries: List[str]
    sources: List[str]  # 优先搜索的来源
    required: bool = True  # 是否为必需信息


class CompetitiveQueryBuilder:
    """
    竞品情报查询构建器
    为7大模块生成针对性的搜索查询
    """
    
    def __init__(self, product_name: str, product_url: Optional[str] = None):
        self.product_name = product_name
        self.product_url = product_url
        self.domain = self._extract_domain(product_url) if product_url else None
    
    def build_all_queries(self) -> Dict[str, QueryTemplate]:
        """
        构建所有模块的查询
        返回按模块组织的查询字典
        """
        return {
            "basic_info": self._build_basic_info_queries(),
            "founder_intelligence": self._build_founder_queries(),
            "broken_spot": self._build_broken_spot_queries(),
            "user_urgency": self._build_user_urgency_queries(),
            "arena_scoring": self._build_arena_queries(),
            "uniqueness": self._build_uniqueness_queries(),
            "implementation": self._build_implementation_queries(),
            "growth_intelligence": self._build_growth_queries()
        }
    
    def _build_basic_info_queries(self) -> QueryTemplate:
        """基础信息查询"""
        queries = [
            f'"{self.product_name}" company team size employees number',
            f'"{self.product_name}" founded year when started launch date',
            f'"{self.product_name}" product type category SaaS B2B B2C',
            f'"{self.product_name}" company about us team page',
            f'"{self.product_name}" crunchbase profile'
        ]
        
        if self.domain:
            queries.extend([
                f'site:{self.domain} about team',
                f'site:{self.domain} company founded'
            ])
        
        return QueryTemplate(
            module="基础信息 | Facts",
            queries=queries,
            sources=["crunchbase.com", "linkedin.com/company", self.domain] if self.domain else ["crunchbase.com", "linkedin.com/company"],
            required=True
        )
    
    def _build_founder_queries(self) -> QueryTemplate:
        """创始人/团队情报查询"""
        queries = [
            f'"{self.product_name}" founder CEO CTO LinkedIn profile',
            f'"{self.product_name}" founding team background experience',
            f'"{self.product_name}" founder previous company startup exit',
            f'"{self.product_name}" team technical expertise engineers',
            f'"{self.product_name}" founder Twitter social media',
            f'"{self.product_name}" founder interview podcast blog post'
        ]
        
        return QueryTemplate(
            module="创始人/团队 | Founder Intelligence",
            queries=queries,
            sources=["linkedin.com", "twitter.com", "medium.com", "techcrunch.com"],
            required=True
        )
    
    def _build_broken_spot_queries(self) -> QueryTemplate:
        """Q2: Fixed Broken Spot 查询"""
        queries = [
            f'"{self.product_name}" solves problem pain point solution',
            f'"{self.product_name}" vs alternatives comparison better than',
            f'"{self.product_name}" unique value proposition USP',
            f'"{self.product_name}" why built reason mission',
            f'"{self.product_name}" disrupting industry changing'
        ]
        
        if self.domain:
            queries.append(f'site:{self.domain} why problem solution')
        
        return QueryTemplate(
            module="Q2 Fixed Broken Spot",
            queries=queries,
            sources=[self.domain, "producthunt.com", "g2.com", "capterra.com"] if self.domain else ["producthunt.com", "g2.com"],
            required=True
        )
    
    def _build_user_urgency_queries(self) -> QueryTemplate:
        """Q3: User Urgency 查询"""
        queries = [
            f'"{self.product_name}" customer testimonial review case study',
            f'"{self.product_name}" user feedback satisfaction NPS score',
            f'"{self.product_name}" customer success story ROI results',
            f'"{self.product_name}" user adoption rate growth statistics',
            f'"{self.product_name}" review rating stars G2 Capterra'
        ]
        
        return QueryTemplate(
            module="Q3 User Urgency",
            queries=queries,
            sources=["g2.com", "capterra.com", "trustpilot.com", "producthunt.com"],
            required=True
        )
    
    def _build_arena_queries(self) -> QueryTemplate:
        """Q6: Arena & Scoring Rule 查询"""
        queries = [
            f'"{self.product_name}" market competition landscape analysis',
            f'"{self.product_name}" vs competitors comparison chart table',
            f'"{self.product_name}" market share percentage growth rate',
            f'"{self.product_name}" competitive advantage differentiation',
            f'"{self.product_name}" industry report gartner forrester',
            f'best "{self.product_name}" alternatives competitors similar tools'
        ]
        
        return QueryTemplate(
            module="Q6 Arena & Scoring Rule",
            queries=queries,
            sources=["g2.com/compare", "alternativeto.net", "getapp.com", "gartner.com"],
            required=True
        )
    
    def _build_uniqueness_queries(self) -> QueryTemplate:
        """Q7: First/Only/Number 查询"""
        queries = [
            f'"{self.product_name}" first market pioneer innovative breakthrough',
            f'"{self.product_name}" only unique feature patent proprietary',
            f'"{self.product_name}" market leader position ranking number one',
            f'"{self.product_name}" awards recognition industry accolades',
            f'"{self.product_name}" milestone achievement record breaking'
        ]
        
        return QueryTemplate(
            module="Q7 First/Only/Number",
            queries=queries,
            sources=["techcrunch.com", "venturebeat.com", "forbes.com", "businesswire.com"],
            required=True
        )
    
    def _build_implementation_queries(self) -> QueryTemplate:
        """Q8: Implementation Architecture 查询"""
        queries = [
            f'"{self.product_name}" technology stack tech architecture',
            f'"{self.product_name}" API documentation integration SDK',
            f'"{self.product_name}" GitHub repository open source code',
            f'"{self.product_name}" technical blog engineering how built',
            f'"{self.product_name}" infrastructure scalability performance',
            f'site:github.com "{self.product_name}"'
        ]
        
        if self.domain:
            queries.extend([
                f'site:{self.domain} API docs documentation',
                f'site:{self.domain} developers technical blog'
            ])
        
        return QueryTemplate(
            module="Q8 Implementation Architecture",
            queries=queries,
            sources=["github.com", "stackshare.io", f"{self.domain}/docs" if self.domain else None],
            required=True
        )
    
    def _build_growth_queries(self) -> QueryTemplate:
        """营销情报查询"""
        queries = [
            f'"{self.product_name}" growth timeline history milestones',
            f'"{self.product_name}" marketing strategy channels tactics',
            f'"{self.product_name}" user acquisition customer growth rate',
            f'"{self.product_name}" ProductHunt launch ship page',
            f'"{self.product_name}" content marketing SEO blog strategy',
            f'"{self.product_name}" social media marketing Twitter LinkedIn',
            f'"{self.product_name}" funding investment series revenue ARR'
        ]
        
        return QueryTemplate(
            module="营销情报 | Growth Intelligence",
            queries=queries,
            sources=["producthunt.com", "twitter.com", "linkedin.com", "techcrunch.com", "similarweb.com"],
            required=True
        )
    
    def get_competitor_queries(self, competitors: List[str]) -> Dict[str, List[str]]:
        """
        为竞品分析生成查询
        
        Args:
            competitors: 竞品名称列表
        
        Returns:
            按竞品组织的查询字典
        """
        competitor_queries = {}
        
        for competitor in competitors:
            competitor_queries[competitor] = [
                f'"{competitor}" features pricing plans comparison',
                f'"{competitor}" market share user base statistics',
                f'"{competitor}" strengths weaknesses SWOT analysis',
                f'"{self.product_name}" vs "{competitor}" comparison',
                f'"{competitor}" customer reviews satisfaction rating'
            ]
        
        return competitor_queries
    
    def _extract_domain(self, url: str) -> str:
        """从URL提取域名"""
        if not url:
            return ""
        
        # 移除协议
        domain = url.replace("https://", "").replace("http://", "")
        # 移除路径
        domain = domain.split("/")[0]
        # 移除端口
        domain = domain.split(":")[0]
        
        return domain