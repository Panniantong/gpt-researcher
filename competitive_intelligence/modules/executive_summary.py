"""
执行摘要生成模块
生成竞品调研的执行摘要
"""
from typing import Dict, List, Any, Optional

from competitive_intelligence.utils.llm_helper import get_llm_response
from competitive_intelligence.prompts.competitive_prompts import EXECUTIVE_SUMMARY_PROMPT


class ExecutiveSummaryGenerator:
    """执行摘要生成器"""
    
    def __init__(self, llm_provider: str = None, model: str = None):
        self.llm_provider = llm_provider
        self.model = model
    
    async def generate_summary(
        self,
        basic_info: Dict[str, Any],
        founder_analysis: Dict[str, Any],
        eight_dimensions: Dict[str, Any],
        marketing_intel: Dict[str, Any],
        replication_eval: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成执行摘要
        
        Args:
            basic_info: 基础信息
            founder_analysis: 创始人分析
            eight_dimensions: 八维分析结果
            marketing_intel: 营销情报
            replication_eval: 复刻评估
            
        Returns:
            执行摘要
        """
        
        
        # 格式化各部分信息
        formatted_data = {
            "basic_info": self._format_basic_info(basic_info),
            "founder_analysis": self._format_founder_analysis(founder_analysis),
            "eight_dimensions": self._format_eight_dimensions(eight_dimensions),
            "marketing_intel": self._format_marketing_intel(marketing_intel),
            "replication_eval": self._format_replication_eval(replication_eval)
        }
        
        # 生成摘要
        prompt = EXECUTIVE_SUMMARY_PROMPT.format(**formatted_data)
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        
        # 解析摘要
        summary = self._parse_summary(response)
        
        # 添加额外的洞察
        summary["key_success_factors"] = self._identify_success_factors(
            founder_analysis, 
            marketing_intel,
            eight_dimensions
        )
        summary["risk_factors"] = self._identify_risk_factors(
            replication_eval,
            eight_dimensions
        )
        
        return summary
    
    def _format_basic_info(self, info: Dict[str, Any]) -> str:
        """格式化基础信息"""
        return f"""
产品名称：{info.get('name', 'N/A')}
一句话描述：{info.get('one_liner', 'N/A')}
产品类型：{info.get('type', 'N/A')}
团队规模：{info.get('team_size', 'N/A')}
发布状态：{info.get('launch_status', 'N/A')}
"""
    
    def _format_founder_analysis(self, analysis: Dict[str, Any]) -> str:
        """格式化创始人分析"""
        profile = analysis.get('profile', {})
        advantages = analysis.get('unfair_advantages', [])
        
        return f"""
背景：{profile.get('background', 'N/A')}
技术能力：{profile.get('technical_skills', 'N/A')}
行业经验：{profile.get('industry_depth', 'N/A')}
不公平优势：{', '.join(advantages[:3]) if advantages else 'N/A'}
符合AI+行业专家模式：{'是' if analysis.get('ai_expert_model', {}).get('fits_pattern') else '否'}
"""
    
    def _format_eight_dimensions(self, dimensions: Dict[str, Any]) -> str:
        """格式化八维分析"""
        formatted = []
        
        for key, analysis in dimensions.items():
            if hasattr(analysis, 'answer'):
                formatted.append(f"{key} - {analysis.question}: {analysis.answer[:100]}...")
        
        return '\n'.join(formatted)
    
    def _format_marketing_intel(self, intel: Dict[str, Any]) -> str:
        """格式化营销情报"""
        channels = intel.get('growth_channels', {})
        timeline = intel.get('growth_timeline', {})
        
        return f"""
主要获客渠道：{', '.join(channels.get('primary_channels', [])[:3])}
独特策略：{', '.join(channels.get('signature_tactics', [])[:2])}
增长阶段：{timeline.get('growth_phase', 'N/A')[:100]}...
"""
    
    def _format_replication_eval(self, evaluation: Dict[str, Any]) -> str:
        """格式化复刻评估"""
        return f"""
难度等级：{evaluation.get('difficulty_level', 'N/A')}
核心挑战：{', '.join(evaluation.get('core_challenges', [])[:3])}
主要壁垒：{len([b for b in evaluation.get('barriers', {}).values() if b])}个
"""
    
    def _parse_summary(self, response: str) -> Dict[str, Any]:
        """解析摘要响应"""
        summary = {
            "core_insights": "",
            "growth_model": "",
            "founder_advantages": "",
            "transferable_elements": {
                "technical": [],
                "product": [],
                "marketing": [],
                "operations": []
            },
            "trend_analysis": "",
            "indie_developer_strategy": ""
        }
        
        sections = response.split('\n\n')
        
        for section in sections:
            section_lower = section.lower()
            
            if "核心洞察" in section or "core insight" in section_lower:
                summary["core_insights"] = self._extract_content(section)
            elif "增长模式" in section or "growth model" in section_lower:
                summary["growth_model"] = self._extract_content(section)
            elif "创始人优势" in section or "founder advantage" in section_lower:
                summary["founder_advantages"] = self._extract_content(section)
            elif "可迁移要素" in section or "transferable" in section_lower:
                # 解析可迁移要素
                elements = section.split('\n')
                for element in elements:
                    if "技术" in element or "technical" in element.lower():
                        summary["transferable_elements"]["technical"].append(element.strip())
                    elif "产品" in element or "product" in element.lower():
                        summary["transferable_elements"]["product"].append(element.strip())
                    elif "营销" in element or "marketing" in element.lower():
                        summary["transferable_elements"]["marketing"].append(element.strip())
                    elif "运营" in element or "operation" in element.lower():
                        summary["transferable_elements"]["operations"].append(element.strip())
            elif "趋势" in section or "trend" in section_lower:
                summary["trend_analysis"] = self._extract_content(section)
            elif "独立开发者" in section or "indie developer" in section_lower:
                summary["indie_developer_strategy"] = self._extract_content(section)
        
        # 如果没有解析到内容，保存原始响应
        if not summary["core_insights"]:
            summary["raw_summary"] = response
        
        return summary
    
    def _extract_content(self, section: str) -> str:
        """从章节中提取内容（去除标题）"""
        lines = section.split('\n')
        content_lines = [line for line in lines if line.strip() and not line.startswith('#')]
        return ' '.join(content_lines).strip()
    
    def _identify_success_factors(
        self,
        founder_analysis: Dict[str, Any],
        marketing_intel: Dict[str, Any],
        eight_dimensions: Dict[str, Any]
    ) -> List[str]:
        """识别关键成功因素"""
        factors = []
        
        # 从创始人分析中提取
        if founder_analysis.get('ai_expert_model', {}).get('fits_pattern'):
            factors.append("创始人具备AI+行业专家的完美结合")
        
        advantages = founder_analysis.get('unfair_advantages', [])
        if advantages:
            factors.append(f"创始人不公平优势：{advantages[0]}")
        
        # 从营销情报中提取
        viral_factors = marketing_intel.get('viral_factors', [])
        if viral_factors:
            factors.append("具备病毒式传播特性")
        
        growth_metrics = marketing_intel.get('growth_metrics', {})
        if growth_metrics.get('growth_rates'):
            factors.append("高速增长验证市场需求")
        
        # 从八维分析中提取
        # 这里可以根据具体的分析结果添加更多因素
        
        return factors[:5]  # 限制数量
    
    def _identify_risk_factors(
        self,
        replication_eval: Dict[str, Any],
        eight_dimensions: Dict[str, Any]
    ) -> List[str]:
        """识别风险因素"""
        risks = []
        
        # 从复刻评估中提取
        if "🟢" in replication_eval.get('difficulty_level', ''):
            risks.append("低进入门槛，容易被复制")
        
        barriers = replication_eval.get('barriers', {})
        if not any(barriers.values()):
            risks.append("缺乏明显的护城河")
        
        # 从八维分析中提取
        # 根据Q7的分析判断
        if eight_dimensions.get('Q7'):
            q7_answer = eight_dimensions['Q7'].answer if hasattr(eight_dimensions['Q7'], 'answer') else ""
            if "number one" not in q7_answer.lower() and "第一" not in q7_answer:
                risks.append("非市场领导者，面临激烈竞争")
        
        return risks[:3]  # 限制数量
    
    def generate_actionable_insights(
        self,
        summary: Dict[str, Any],
        replication_eval: Dict[str, Any]
    ) -> List[str]:
        """
        生成可执行的洞察建议
        
        Args:
            summary: 执行摘要
            replication_eval: 复刻评估
            
        Returns:
            可执行建议列表
        """
        insights = []
        
        # 基于难度等级给出建议
        difficulty = replication_eval.get('difficulty_level', '')
        
        if "🟢" in difficulty or "🟡" in difficulty:
            insights.extend([
                "立即开始MVP开发，快速验证市场",
                "专注于某个被忽视的细分市场",
                "通过优秀的用户体验建立差异化"
            ])
        else:
            insights.extend([
                "先深入研究目标用户，找到未被满足的需求",
                "考虑与行业专家合作弥补经验不足",
                "从辅助工具或插件开始，而非直接竞争"
            ])
        
        # 基于可迁移要素给出建议
        transferable = summary.get('transferable_elements', {})
        if transferable.get('marketing'):
            insights.append("复制已验证的营销策略，但需本地化调整")
        
        if transferable.get('technical'):
            insights.append("利用相似的技术栈快速搭建原型")
        
        # 基于成功因素给出建议
        success_factors = summary.get('key_success_factors', [])
        if any("社区" in factor for factor in success_factors):
            insights.append("优先建立用户社区，培养早期拥护者")
        
        return insights[:5]  # 限制数量