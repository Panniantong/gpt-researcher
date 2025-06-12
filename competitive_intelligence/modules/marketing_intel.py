"""
营销情报分析模块
分析产品的增长策略和营销手法
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

from competitive_intelligence.utils.llm_helper import get_llm_response
from competitive_intelligence.prompts.competitive_prompts import MARKETING_INTEL_PROMPT


class MarketingIntelAnalyzer:
    """营销情报分析器"""
    
    def __init__(self, llm_provider: str = None, model: str = None):
        self.llm_provider = llm_provider
        self.model = model
    
    async def analyze_marketing_strategy(
        self,
        product_name: str,
        search_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        分析营销策略
        
        Args:
            product_name: 产品名称
            search_results: 营销相关的搜索结果
            
        Returns:
            营销情报分析结果
        """
        
        
        # 格式化搜索结果
        formatted_results = self._format_search_results(search_results)
        
        prompt = MARKETING_INTEL_PROMPT.format(
            product_name=product_name,
            search_results=formatted_results
        )
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        
        # 解析分析结果
        analysis = self._parse_marketing_analysis(response)
        
        # 添加额外的分析
        analysis["growth_metrics"] = self._extract_growth_metrics(search_results)
        analysis["viral_factors"] = self._identify_viral_factors(search_results)
        analysis["sources"] = self._extract_sources(search_results)
        
        return analysis
    
    def _parse_marketing_analysis(self, response: str) -> Dict[str, Any]:
        """解析营销分析响应"""
        analysis = {
            "growth_timeline": {
                "launch_phase": "",
                "growth_phase": "",
                "scale_phase": ""
            },
            "growth_channels": {
                "primary_channels": [],
                "signature_tactics": [],
                "content_strategy": ""
            },
            "key_milestones": []
        }
        
        sections = response.split('\n\n')
        
        for section in sections:
            section_lower = section.lower()
            
            if "launch phase" in section_lower or "发布阶段" in section:
                analysis["growth_timeline"]["launch_phase"] = section
            elif "growth phase" in section_lower or "增长阶段" in section:
                analysis["growth_timeline"]["growth_phase"] = section
            elif "scale phase" in section_lower or "规模化阶段" in section:
                analysis["growth_timeline"]["scale_phase"] = section
            elif "primary channels" in section_lower or "主要.*渠道" in section:
                # 提取渠道列表
                channels = [line.strip() for line in section.split('\n') 
                           if line.strip() and not line.startswith('#')]
                analysis["growth_channels"]["primary_channels"] = channels
            elif "signature tactics" in section_lower or "独特.*手法" in section:
                tactics = [line.strip() for line in section.split('\n') 
                          if line.strip() and not line.startswith('#')]
                analysis["growth_channels"]["signature_tactics"] = tactics
            elif "content strategy" in section_lower or "内容.*策略" in section:
                analysis["growth_channels"]["content_strategy"] = section
        
        # 如果没有解析到结构化内容，保存原始响应
        if not any([analysis["growth_timeline"]["launch_phase"],
                   analysis["growth_timeline"]["growth_phase"],
                   analysis["growth_channels"]["primary_channels"]]):
            analysis["raw_analysis"] = response
        
        return analysis
    
    def _format_search_results(self, search_results: List[Dict[str, Any]]) -> str:
        """格式化搜索结果为字符串"""
        if not search_results:
            return "No search results available"
        
        formatted = []
        for i, result in enumerate(search_results[:10], 1):  # 限制前10个结果
            title = result.get("title", "No title")
            content = result.get("content", "No content")[:500]  # 限制内容长度
            url = result.get("url", "")
            
            formatted.append(f"""
Result {i}:
Title: {title}
URL: {url}
Content: {content}...
""")
        
        return "\n".join(formatted)
    
    def _extract_growth_metrics(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """从搜索结果中提取增长指标"""
        metrics = {
            "user_numbers": [],
            "revenue_data": [],
            "growth_rates": [],
            "funding_info": []
        }
        
        for result in search_results:
            content = result.get("content", "")
            
            # 提取用户数量
            user_patterns = [
                r'(\d+[KMB]?)\s*users',
                r'用户.*?(\d+[万亿]?)',
                r'(\d+[,\d]*)\s*customers'
            ]
            for pattern in user_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                metrics["user_numbers"].extend(matches)
            
            # 提取收入数据
            revenue_patterns = [
                r'\$(\d+[KMB]?)\s*(?:revenue|ARR|MRR)',
                r'revenue.*?\$(\d+[,\d]*)',
                r'营收.*?(\d+[万亿]?)'
            ]
            for pattern in revenue_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                metrics["revenue_data"].extend(matches)
            
            # 提取增长率
            growth_patterns = [
                r'(\d+)%\s*growth',
                r'增长.*?(\d+)%',
                r'grew\s*(\d+)%'
            ]
            for pattern in growth_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                metrics["growth_rates"].extend(matches)
            
            # 提取融资信息
            funding_patterns = [
                r'raised\s*\$(\d+[KMB]?)',
                r'funding.*?\$(\d+[KMB]?)',
                r'融资.*?(\d+[万亿]?)'
            ]
            for pattern in funding_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                metrics["funding_info"].extend(matches)
        
        # 去重
        for key in metrics:
            metrics[key] = list(set(metrics[key]))[:5]  # 限制数量
        
        return metrics
    
    def _identify_viral_factors(self, search_results: List[Dict[str, Any]]) -> List[str]:
        """识别病毒式传播因素"""
        viral_factors = []
        
        viral_keywords = [
            "viral", "word of mouth", "referral", "social sharing",
            "community", "user generated", "network effect",
            "病毒", "口碑", "推荐", "社交分享", "社区", "网络效应"
        ]
        
        for result in search_results:
            content = result.get("content", "").lower()
            title = result.get("title", "").lower()
            
            for keyword in viral_keywords:
                if keyword in content or keyword in title:
                    # 提取相关句子作为病毒因素
                    sentences = content.split('.')
                    for sentence in sentences:
                        if keyword in sentence and len(sentence) < 200:
                            viral_factors.append(sentence.strip())
                            break
        
        return list(set(viral_factors))[:5]  # 去重并限制数量
    
    def _extract_sources(self, results: List[Dict[str, Any]]) -> List[str]:
        """提取信息源"""
        sources = []
        for result in results:
            url = result.get("url", "")
            if url and url not in sources:
                sources.append(url)
        return sources[:10]
    
    async def generate_marketing_research_queries(
        self,
        product_name: str,
        product_url: str = None
    ) -> List[str]:
        """
        生成营销研究相关的搜索查询
        
        Args:
            product_name: 产品名称
            product_url: 产品网址（可选）
            
        Returns:
            搜索查询列表
        """
        queries = [
            # 增长相关
            f"{product_name} growth story",
            f"{product_name} user growth",
            f"{product_name} launch strategy",
            f"how {product_name} acquired first users",
            
            # 营销策略
            f"{product_name} marketing strategy",
            f"{product_name} content marketing",
            f"{product_name} SEO strategy",
            f"{product_name} social media",
            
            # 病毒传播
            f"{product_name} viral growth",
            f"{product_name} referral program",
            f"{product_name} community building",
            
            # 里程碑事件
            f"{product_name} funding announcement",
            f"{product_name} product hunt launch",
            f"{product_name} press coverage",
            
            # 竞争对比
            f"{product_name} market share",
            f"{product_name} competitive advantage"
        ]
        
        # 如果有网址，添加domain相关查询
        if product_url:
            domain = product_url.replace("https://", "").replace("http://", "").split('/')[0]
            queries.extend([
                f"site:{domain} growth",
                f"site:{domain} about us"
            ])
        
        return queries[:12]  # 限制查询数量
    
    def analyze_content_strategy(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析内容营销策略
        
        Args:
            search_results: 搜索结果
            
        Returns:
            内容策略分析
        """
        content_analysis = {
            "content_types": [],
            "publishing_frequency": "Unknown",
            "key_topics": [],
            "platforms": []
        }
        
        # 内容类型关键词
        content_type_keywords = {
            "blog": ["blog", "article", "post", "博客", "文章"],
            "video": ["video", "youtube", "视频"],
            "podcast": ["podcast", "播客"],
            "newsletter": ["newsletter", "email", "订阅"],
            "social": ["twitter", "linkedin", "facebook", "社交媒体"],
            "webinar": ["webinar", "workshop", "在线研讨会"],
            "ebook": ["ebook", "guide", "whitepaper", "电子书", "白皮书"]
        }
        
        # 平台关键词
        platform_keywords = {
            "YouTube": ["youtube.com", "youtube channel"],
            "Twitter": ["twitter.com", "@"],
            "LinkedIn": ["linkedin.com", "linkedin post"],
            "Medium": ["medium.com"],
            "Blog": ["blog.", "/blog/"],
            "Newsletter": ["substack", "convertkit", "mailchimp"]
        }
        
        for result in search_results:
            content = result.get("content", "").lower()
            url = result.get("url", "").lower()
            
            # 识别内容类型
            for content_type, keywords in content_type_keywords.items():
                if any(keyword in content or keyword in url for keyword in keywords):
                    if content_type not in content_analysis["content_types"]:
                        content_analysis["content_types"].append(content_type)
            
            # 识别平台
            for platform, keywords in platform_keywords.items():
                if any(keyword in url for keyword in keywords):
                    if platform not in content_analysis["platforms"]:
                        content_analysis["platforms"].append(platform)
        
        return content_analysis