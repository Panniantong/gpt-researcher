"""
创始人背景调研模块
分析产品创始人/团队的背景和不公平优势
"""
from typing import Dict, List, Any, Optional

from competitive_intelligence.utils.llm_helper import get_llm_response
from competitive_intelligence.prompts.competitive_prompts import FOUNDER_RESEARCH_PROMPT, SEARCH_QUERY_GENERATOR


class FounderAnalyzer:
    """创始人背景分析器"""
    
    def __init__(self, llm_provider: str = None, model: str = None):
        self.llm_provider = llm_provider
        self.model = model
    
    async def generate_search_queries(self, product_name: str, product_url: str = None) -> List[str]:
        """
        生成创始人相关的搜索查询
        
        Args:
            product_name: 产品名称
            product_url: 产品网址（可选）
            
        Returns:
            搜索查询列表
        """
        # 验证产品名称是否有效
        if not product_name or "not found" in product_name.lower() or "⚠" in product_name:
            # 如果产品名无效，返回空列表或基础查询
            return []
        
        prompt = SEARCH_QUERY_GENERATOR.format(
            product_name=product_name,
            product_url=product_url or "",
            product_type="",
            research_goal="查找创始人/团队背景信息、职业经历、技术能力、行业经验"
        )
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        
        # 解析响应为查询列表
        queries = [q.strip() for q in response.split('\n') if q.strip()]
        
        # 添加一些特定的创始人搜索查询
        founder_queries = [
            f"{product_name} founder",
            f"{product_name} CEO",
            f"{product_name} team",
            f"{product_name} LinkedIn",
            f"{product_name} GitHub",
            f"{product_name} Twitter creator",
            f"who created {product_name}",
            f"{product_name} company about us"
        ]
        
        # 合并查询，去重
        all_queries = list(set(queries + founder_queries))
        
        return all_queries[:10]  # 限制查询数量
    
    async def analyze_founder_background(
        self, 
        product_name: str, 
        search_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        分析创始人背景
        
        Args:
            product_name: 产品名称
            search_results: 搜索结果列表
            
        Returns:
            创始人背景分析结果
        """
        
        
        # 格式化搜索结果
        formatted_results = self._format_search_results(search_results)
        
        prompt = FOUNDER_RESEARCH_PROMPT.format(
            product_name=product_name,
            search_results=formatted_results
        )
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        
        # 解析响应
        analysis = self._parse_founder_analysis(response)
        
        # 添加原始信息源
        analysis["sources"] = self._extract_sources(search_results)
        
        return analysis
    
    def _format_search_results(self, results: List[Dict[str, Any]]) -> str:
        """格式化搜索结果为文本"""
        formatted = []
        
        for i, result in enumerate(results[:15]):  # 限制结果数量
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")
            
            formatted.append(f"""
Result {i+1}:
Title: {title}
URL: {url}
Content: {content[:500]}...
---
""")
        
        return "\n".join(formatted)
    
    def _parse_founder_analysis(self, response: str) -> Dict[str, Any]:
        """解析创始人分析响应"""
        analysis = {
            "profile": {
                "background": "",
                "technical_skills": "",
                "industry_depth": ""
            },
            "unfair_advantages": [],
            "ai_expert_model": {
                "fits_pattern": False,
                "explanation": ""
            },
            "key_insights": []
        }
        
        # 简单的解析逻辑（实际使用时可以更复杂）
        sections = response.split('\n\n')
        
        for section in sections:
            section_lower = section.lower()
            
            if "身份背景" in section or "background" in section_lower:
                analysis["profile"]["background"] = section
            elif "技术能力" in section or "technical" in section_lower:
                analysis["profile"]["technical_skills"] = section
            elif "行业深度" in section or "industry" in section_lower:
                analysis["profile"]["industry_depth"] = section
            elif "不公平优势" in section or "unfair advantage" in section_lower:
                # 提取优势列表
                advantages = [line.strip() for line in section.split('\n') if line.strip() and not line.startswith('#')]
                analysis["unfair_advantages"] = advantages
            elif "ai + 行业专家" in section_lower or "ai expert" in section_lower:
                analysis["ai_expert_model"]["explanation"] = section
                analysis["ai_expert_model"]["fits_pattern"] = "是" in section or "yes" in section_lower
        
        # 如果没有解析到结构化内容，将整个响应作为原始分析
        if not any(analysis["profile"].values()):
            analysis["raw_analysis"] = response
        
        return analysis
    
    def _extract_sources(self, results: List[Dict[str, Any]]) -> List[str]:
        """提取信息源URL"""
        sources = []
        
        for result in results:
            url = result.get("url", "")
            if url and url not in sources:
                sources.append(url)
        
        return sources[:10]  # 限制源数量
    
    def identify_competitive_advantages(self, founder_analysis: Dict[str, Any]) -> List[str]:
        """
        识别竞争优势
        
        Args:
            founder_analysis: 创始人分析结果
            
        Returns:
            竞争优势列表
        """
        advantages = []
        
        # 从分析中提取优势
        if "unfair_advantages" in founder_analysis:
            advantages.extend(founder_analysis["unfair_advantages"])
        
        # 基于背景识别额外优势
        profile = founder_analysis.get("profile", {})
        
        # 检查技术背景
        tech_skills = profile.get("technical_skills", "").lower()
        if any(skill in tech_skills for skill in ["ai", "machine learning", "深度学习", "nlp"]):
            advantages.append("AI/ML技术背景优势")
        
        # 检查行业经验
        industry_depth = profile.get("industry_depth", "").lower()
        if "年" in industry_depth or "years" in industry_depth:
            advantages.append("深厚的行业经验优势")
        
        # 检查是否符合"AI + 行业专家"模式
        ai_expert = founder_analysis.get("ai_expert_model", {})
        if ai_expert.get("fits_pattern"):
            advantages.append("符合'AI + 行业专家'成功模式")
        
        return list(set(advantages))  # 去重