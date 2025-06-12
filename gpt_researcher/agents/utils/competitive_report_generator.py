"""
Report generator for competitive intelligence
竞品情报报告生成器，严格遵循7大模块格式
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class CompetitiveReportGenerator:
    """
    竞品情报报告生成器
    严格按照预定义的7大模块格式生成报告
    """
    
    def __init__(self):
        self.report_sections = []
        self.all_sources = set()
    
    def generate_report(self, data: Dict[str, Any]) -> str:
        """
        生成完整的竞品情报报告
        
        Args:
            data: 包含所有研究数据的字典
        
        Returns:
            格式化的Markdown报告
        """
        self.report_sections = []
        
        # 1. 基础信息
        self._add_basic_info_section(data.get("product_info", {}))
        
        # 2. 创始人/团队
        self._add_founder_section(data.get("founder_info", {}))
        
        # 3. 八维分析
        self._add_eight_dimensions_section(data.get("eight_dimensions", {}))
        
        # 4. 营销情报
        self._add_growth_intelligence_section(data.get("growth_intelligence", {}))
        
        # 5. 复刻评估
        self._add_feasibility_section(data.get("feasibility", {}))
        
        # 6. Executive Summary
        self._add_executive_summary(data.get("executive_summary", {}))
        
        # 7. 信息来源
        self._add_sources_section()
        
        return "\n\n".join(self.report_sections)
    
    def _add_basic_info_section(self, info: Dict):
        """添加基础信息部分"""
        section = "### 【基础信息 | Facts】\n"
        
        fields = [
            ("Team Size", info.get("team_size", "⚠︎ Info insufficient")),
            ("Name", info.get("name", "")),
            ("One-liner", info.get("one_liner", "")),
            ("Type", info.get("type", "")),
            ("URL", info.get("url", "")),
            ("Launch Status", info.get("launch_status", "")),
            ("Founded", info.get("founded", ""))
        ]
        
        for field_name, value in fields:
            if not value or value == "":
                value = "⚠︎ Info insufficient"
                if search_trace := info.get(f"{field_name.lower()}_search_trace"):
                    value += f" (Searched: {search_trace})"
            
            section += f"**{field_name}**: {value}\n"
        
        self.report_sections.append(section.strip())
    
    def _add_founder_section(self, info: Dict):
        """添加创始人/团队部分"""
        section = "### 【创始人/团队 | Founder Intelligence】\n"
        
        # a. 人物画像
        section += "**a. 👤 人物画像**\n"
        profile = info.get("profile", {})
        if profile:
            if identity := profile.get("identity_background"):
                section += f"- 身份背景: {identity}\n"
            if tech := profile.get("technical_ability"):
                section += f"- 技术能力: {tech}\n"
            if industry := profile.get("industry_depth"):
                section += f"- 行业深度: {industry}\n"
        else:
            section += "⚠︎ Info insufficient (Searched: LinkedIn, company about page, founder interviews)\n"
        
        # b. 不公平优势
        section += "\n**b. 🎯 不公平优势**\n"
        advantages = info.get("unfair_advantages", {})
        if advantages:
            if insight := advantages.get("industry_insight"):
                section += f"- 行业洞察: {insight}\n"
            if tech_impl := advantages.get("technical_implementation"):
                section += f"- 技术实现: {tech_impl}\n"
            if network := advantages.get("resource_network"):
                section += f"- 资源网络: {network}\n"
            if timing := advantages.get("timing_judgment"):
                section += f"- 时机判断: {timing}\n"
        else:
            section += "⚠︎ Info insufficient\n"
        
        # c. AI + 行业专家验证
        section += "\n**c. 💡 AI + 行业专家验证**\n"
        validation = info.get("validation", "⚠︎ Info insufficient")
        section += f"{validation}\n"
        
        # 信息来源
        if sources := info.get("sources", []):
            section += "\n**信息来源**:\n"
            for i, source in enumerate(sources, 1):
                section += f"[▲{i}] {source}\n"
                self.all_sources.add(source)
        
        self.report_sections.append(section.strip())
    
    def _add_eight_dimensions_section(self, dimensions: Dict):
        """添加八维分析部分"""
        section = "### 【八维分析 | 8 Questions】\n"
        
        # Q1 Pitch
        pitch = dimensions.get("pitch", "")
        if pitch:
            # 确保符合长度限制
            if self._is_chinese(pitch):
                pitch = pitch[:20] if len(pitch) > 20 else pitch
            else:
                pitch = pitch[:140] if len(pitch) > 140 else pitch
        else:
            pitch = "⚠︎ Info insufficient"
        section += f"**Q1 Pitch**: {pitch}\n"
        
        # Q2 Fixed Broken Spot
        section += "\n**Q2 Fixed Broken Spot**【需调研 + 来源】\n"
        broken_spot = dimensions.get("fixed_broken_spot", {})
        if broken_spot.get("description"):
            section += f"{broken_spot['description']}\n"
            if sources := broken_spot.get("sources", []):
                for i, source in enumerate(sources, 1):
                    section += f"[■{i}] {source}\n"
                    self.all_sources.add(source)
        else:
            section += "⚠︎ Info insufficient (Searched: product value proposition, problem solved)\n"
        
        # Q3 User Urgency
        section += "\n**Q3 User Urgency**【需调研 + 来源】\n"
        urgency = dimensions.get("user_urgency", {})
        if urgency.get("description"):
            section += f"{urgency['description']}\n"
            if sources := urgency.get("sources", []):
                for i, source in enumerate(sources, 1):
                    section += f"[◆{i}] {source}\n"
                    self.all_sources.add(source)
        else:
            section += "⚠︎ Info insufficient (Searched: user testimonials, reviews, case studies)\n"
        
        # Q4 Who-When-Action
        section += "\n**Q4 Who-When-Action**\n"
        who_when = dimensions.get("who_when_action", "⚠︎ Info insufficient")
        section += f"{who_when}\n"
        
        # Q5 Pain & Pain-level
        section += "\n**Q5 Pain & Pain-level**\n"
        pain = dimensions.get("pain_and_level", "⚠︎ Info insufficient")
        section += f"{pain}\n"
        
        # Q6 Arena & Scoring Rule
        section += "\n**Q6 Arena & Scoring Rule**【需调研】\n"
        arena = dimensions.get("arena_and_scoring", {})
        
        # 赛道一句话
        section += f"**1. 赛道一句话**: {arena.get('arena_description', '⚠︎ Info insufficient')}\n"
        
        # 胜负指标
        section += "\n**2. 胜负指标** (1-3条 + 证据句 + 来源)\n"
        if metrics := arena.get("scoring_metrics", []):
            for metric in metrics[:3]:  # 最多3条
                section += f"- {metric['metric']}: {metric['evidence']}"
                if source := metric.get("source"):
                    section += f" [{source}]"
                    self.all_sources.add(source)
                section += "\n"
        else:
            section += "⚠︎ Info insufficient\n"
        
        # 竞品得分表
        section += "\n**3. 竞品得分表** (目标 + 2竞品)\n"
        if scoring_table := arena.get("competitor_scoring"):
            section += self._format_competitor_table(scoring_table)
        else:
            section += "⚠︎ Info insufficient\n"
        
        # 领先逻辑
        section += "\n**4. 领先逻辑** (≤2句)\n"
        leading_logic = arena.get("leading_logic", "⚠︎ Info insufficient")
        section += f"{leading_logic}\n"
        
        # Q7 First/Only/Number
        section += "\n**Q7 First/Only/Number**【需调研 + 来源】\n"
        uniqueness = dimensions.get("first_only_number", {})
        if uniqueness.get("description"):
            section += f"{uniqueness['description']}\n"
            if sources := uniqueness.get("sources", []):
                for i, source in enumerate(sources, 1):
                    section += f"[●{i}] {source}\n"
                    self.all_sources.add(source)
        else:
            section += "⚠︎ Info insufficient (Searched: market position, unique features, patents)\n"
        
        # Q8 Implementation Architecture
        section += "\n**Q8 Implementation Architecture**【需调研】\n"
        implementation = dimensions.get("implementation_architecture", {})
        if implementation:
            if features := implementation.get("feature_breakdown"):
                section += f"- 功能拆解: {features}\n"
            if apis := implementation.get("api_composition"):
                section += f"- API组合: {apis}\n"
            if innovation := implementation.get("innovation_points"):
                section += f"- 创新点: {innovation}\n"
        else:
            section += "⚠︎ Info insufficient (Searched: technical architecture, API docs, GitHub)\n"
        
        self.report_sections.append(section.strip())
    
    def _add_growth_intelligence_section(self, growth: Dict):
        """添加营销情报部分"""
        section = "### 【营销情报 | Growth Intelligence】【需调研】\n"
        
        # G1 Growth Timeline & Milestones
        section += "**G1 Growth Timeline & Milestones**\n"
        if milestones := growth.get("timeline_milestones", []):
            for milestone in milestones[:7]:  # 列表不超过7条
                section += f"- {milestone.get('date', '')}: {milestone.get('event', '')}\n"
        else:
            section += "⚠︎ Info insufficient (Searched: company history, milestones, growth timeline)\n"
        
        # G2 Growth Channels & Tactics
        section += "\n**G2 Growth Channels & Tactics**\n"
        if channels := growth.get("channels_tactics", []):
            for channel in channels[:7]:  # 列表不超过7条
                section += f"- {channel.get('channel', '')}: {channel.get('tactic', '')}\n"
        else:
            section += "⚠︎ Info insufficient (Searched: marketing strategy, growth channels, acquisition tactics)\n"
        
        # 添加来源
        if sources := growth.get("sources", []):
            section += "\n**信息来源**:\n"
            for i, source in enumerate(sources, 1):
                section += f"[△{i}] {source}\n"
                self.all_sources.add(source)
        
        self.report_sections.append(section.strip())
    
    def _add_feasibility_section(self, feasibility: Dict):
        """添加复刻评估部分"""
        section = "### 【复刻评估 | Solo-Dev Feasibility】\n"
        
        # 难度等级
        difficulty = feasibility.get("difficulty_level", "⚠︎ Info insufficient")
        section += f"**难度等级**: {difficulty}\n"
        
        # 现代AI栈分析
        section += f"\n**现代AI栈分析**:\n{feasibility.get('ai_stack_analysis', '⚠︎ Info insufficient')}\n"
        
        # 技术挑战
        section += "\n**技术挑战** (3-4项):\n"
        if challenges := feasibility.get("technical_challenges", []):
            for challenge in challenges[:4]:  # 最多4项
                section += f"- {challenge}\n"
        else:
            section += "⚠︎ Info insufficient\n"
        
        # AI辅助优势
        section += f"\n**AI辅助优势**:\n{feasibility.get('ai_advantages', '⚠︎ Info insufficient')}\n"
        
        # 行业壁垒
        section += f"\n**行业壁垒**:\n{feasibility.get('industry_barriers', '⚠︎ Info insufficient')}\n"
        
        self.report_sections.append(section.strip())
    
    def _add_executive_summary(self, summary: Dict):
        """添加Executive Summary部分"""
        section = "### 【Executive Summary】\n"
        
        # 核心洞察（≤100字）
        core_insight = summary.get("core_insight", "⚠︎ Info insufficient")
        core_insight = self._limit_text(core_insight, 100)
        section += f"**🎯 核心洞察**:\n{core_insight}\n"
        
        # 增长模式（≤80字）
        growth_model = summary.get("growth_model", "⚠︎ Info insufficient")
        growth_model = self._limit_text(growth_model, 80)
        section += f"\n**🚀 增长模式**:\n{growth_model}\n"
        
        # 创始人优势（≤60字）
        founder_advantage = summary.get("founder_advantage", "⚠︎ Info insufficient")
        founder_advantage = self._limit_text(founder_advantage, 60)
        section += f"\n**👑 创始人优势**:\n{founder_advantage}\n"
        
        # 可迁移要素（3-4项）
        section += "\n**🧩 可迁移要素**:\n"
        if elements := summary.get("transferable_elements", []):
            categories = ["技术", "产品", "营销", "运营"]
            for i, element in enumerate(elements[:4]):
                category = categories[i] if i < len(categories) else "其他"
                section += f"- {category}: {element}\n"
        else:
            section += "⚠︎ Info insufficient\n"
        
        # 趋势判断
        section += f"\n**💡 趋势判断**:\n{summary.get('trend_judgment', '⚠︎ Info insufficient')}\n"
        
        # AI时代独立开发者策略（≤100字）
        indie_strategy = summary.get("indie_developer_strategy", "⚠︎ Info insufficient")
        indie_strategy = self._limit_text(indie_strategy, 100)
        section += f"\n**⭐ AI时代独立开发者策略**:\n{indie_strategy}\n"
        
        self.report_sections.append(section.strip())
    
    def _add_sources_section(self):
        """添加信息来源部分"""
        section = "### 【信息来源 | Sources】\n"
        
        if self.all_sources:
            # 去重并排序
            unique_sources = sorted(list(self.all_sources))
            for i, source in enumerate(unique_sources, 1):
                section += f"{i}. {source}\n"
        else:
            section += "No sources collected.\n"
        
        self.report_sections.append(section.strip())
    
    def _format_competitor_table(self, scoring_data: Dict) -> str:
        """格式化竞品得分表"""
        if not scoring_data:
            return "⚠︎ Info insufficient"
        
        # 获取评分指标
        metrics = scoring_data.get("metrics", [])
        if isinstance(metrics, dict):
            metrics = list(metrics.keys())
        elif not isinstance(metrics, list):
            metrics = []
        
        if not metrics:
            return "⚠︎ Info insufficient - No metrics defined"
        
        # 简单的文本表格格式
        table = "| 产品 | "
        table += " | ".join(metrics) + " |\n"
        table += "|------|" + "|------" * len(metrics) + "|\n"
        
        # 添加每个产品的得分
        for product, scores in scoring_data.get("scores", {}).items():
            table += f"| {product} | "
            table += " | ".join(str(scores.get(metric, "-")) for metric in metrics)
            table += " |\n"
        
        return table
    
    def _is_chinese(self, text: str) -> bool:
        """检测文本是否包含中文"""
        return bool(re.search(r'[\u4e00-\u9fff]', text))
    
    def _limit_text(self, text: str, max_chars: int) -> str:
        """限制文本长度"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars-3] + "..."