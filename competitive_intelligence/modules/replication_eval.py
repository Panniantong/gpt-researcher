"""
复刻难度评估模块
评估独立开发者复刻产品的技术和商业难度
"""
from typing import Dict, List, Any, Optional
from enum import Enum

from competitive_intelligence.utils.llm_helper import get_llm_response
from competitive_intelligence.prompts.competitive_prompts import REPLICATION_EVAL_PROMPT


class DifficultyLevel(Enum):
    """难度等级"""
    EASY = "🟢 容易"
    MEDIUM = "🟡 中等"
    HARD = "🔴 困难"
    EXTREME = "⚫ 极难"


class ReplicationEvaluator:
    """复刻难度评估器"""
    
    def __init__(self, llm_provider: str = None, model: str = None):
        self.llm_provider = llm_provider
        self.model = model
    
    async def evaluate_replication_difficulty(
        self,
        product_info: Dict[str, Any],
        tech_architecture: str = None,
        founder_advantages: List[str] = None
    ) -> Dict[str, Any]:
        """
        评估产品复刻难度
        
        Args:
            product_info: 产品基础信息
            tech_architecture: 技术架构信息（从Q8获得）
            founder_advantages: 创始人不公平优势列表
            
        Returns:
            复刻难度评估结果
        """
        
        
        # 准备提示词
        prompt = REPLICATION_EVAL_PROMPT.format(
            product_name=product_info.get('name', ''),
            product_features=product_info.get('one_liner', ''),
            tech_architecture=tech_architecture or "技术架构信息不足"
        )
        
        response = await get_llm_response(prompt, self.llm_provider, self.model)
        
        # 解析评估结果
        evaluation = self._parse_evaluation(response)
        
        # 添加额外的分析
        evaluation["ai_tools_advantage"] = self._analyze_ai_tools_advantage(product_info)
        evaluation["industry_barriers"] = self._analyze_industry_barriers(
            product_info, 
            founder_advantages
        )
        evaluation["overall_assessment"] = self._generate_overall_assessment(evaluation)
        
        return evaluation
    
    def _parse_evaluation(self, response: str) -> Dict[str, Any]:
        """解析评估响应"""
        evaluation = {
            "difficulty_level": DifficultyLevel.MEDIUM.value,
            "technical_replication": {
                "frontend": "",
                "api_integration": "",
                "ai_workflow": "",
                "business_logic": ""
            },
            "core_challenges": [],
            "ai_development_advantages": {
                "code_generation": "",
                "api_platforms": "",
                "templates": ""
            },
            "barriers": {
                "industry_knowhow": "",
                "user_acquisition": "",
                "trust_building": "",
                "network_effects": "",
                "data_barriers": ""
            }
        }
        
        sections = response.split('\n\n')
        
        for section in sections:
            section_lower = section.lower()
            
            # 识别难度等级
            if "🟢" in section or "容易" in section or "easy" in section_lower:
                evaluation["difficulty_level"] = DifficultyLevel.EASY.value
            elif "🟡" in section or "中等" in section or "medium" in section_lower:
                evaluation["difficulty_level"] = DifficultyLevel.MEDIUM.value
            elif "🔴" in section or "困难" in section or "hard" in section_lower:
                evaluation["difficulty_level"] = DifficultyLevel.HARD.value
            elif "⚫" in section or "极难" in section or "extreme" in section_lower:
                evaluation["difficulty_level"] = DifficultyLevel.EXTREME.value
            
            # 技术复刻评估
            if "前端" in section or "frontend" in section_lower:
                evaluation["technical_replication"]["frontend"] = section
            elif "api" in section_lower:
                evaluation["technical_replication"]["api_integration"] = section
            elif "workflow" in section_lower:
                evaluation["technical_replication"]["ai_workflow"] = section
            elif "业务逻辑" in section or "business logic" in section_lower:
                evaluation["technical_replication"]["business_logic"] = section
            
            # 核心挑战
            if "核心.*挑战" in section or "core.*challenge" in section_lower:
                challenges = [line.strip() for line in section.split('\n') 
                             if line.strip() and not line.startswith('#')]
                evaluation["core_challenges"] = challenges[:4]  # 限制3-4个
            
            # 行业壁垒
            if "行业.*knowhow" in section or "industry.*knowhow" in section_lower:
                evaluation["barriers"]["industry_knowhow"] = section
            elif "用户获取" in section or "user acquisition" in section_lower:
                evaluation["barriers"]["user_acquisition"] = section
            elif "信任" in section or "trust" in section_lower:
                evaluation["barriers"]["trust_building"] = section
            elif "网络效应" in section or "network effect" in section_lower:
                evaluation["barriers"]["network_effects"] = section
            elif "数据壁垒" in section or "data barrier" in section_lower:
                evaluation["barriers"]["data_barriers"] = section
        
        # 如果没有解析到内容，保存原始响应
        if not evaluation["core_challenges"]:
            evaluation["raw_evaluation"] = response
        
        return evaluation
    
    def _analyze_ai_tools_advantage(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """分析AI工具在复刻中的优势"""
        advantages = {
            "ui_replication": "高",
            "api_integration": "高",
            "basic_features": "高",
            "complex_logic": "中"
        }
        
        # 基于产品类型调整评估
        product_type = product_info.get('type', '').lower()
        
        if any(keyword in product_type for keyword in ['ai', 'ml', 'chat', 'assistant']):
            # AI类产品
            advantages["api_integration"] = "极高 - 可使用OpenRouter等聚合平台"
            advantages["basic_features"] = "极高 - 大量现成的AI组件"
        
        if any(keyword in product_type for keyword in ['data', 'analytics', 'visualization']):
            # 数据类产品
            advantages["complex_logic"] = "低 - 数据处理逻辑通常较复杂"
        
        if any(keyword in product_type for keyword in ['social', 'community', 'marketplace']):
            # 社交/社区类产品
            advantages["ui_replication"] = "中 - 需要复杂的交互设计"
            advantages["complex_logic"] = "低 - 社交逻辑较复杂"
        
        return advantages
    
    def _analyze_industry_barriers(
        self,
        product_info: Dict[str, Any],
        founder_advantages: List[str] = None
    ) -> List[str]:
        """分析行业壁垒"""
        barriers = []
        
        # 基于创始人优势分析
        if founder_advantages:
            for advantage in founder_advantages:
                if "行业" in advantage or "industry" in advantage.lower():
                    barriers.append("创始人深厚的行业背景难以复制")
                if "网络" in advantage or "network" in advantage.lower():
                    barriers.append("创始人的行业人脉和资源网络")
                if "数据" in advantage or "data" in advantage.lower():
                    barriers.append("独特的数据获取渠道")
        
        # 基于产品类型分析
        product_type = product_info.get('type', '').lower()
        
        if any(keyword in product_type for keyword in ['医疗', 'health', 'medical']):
            barriers.append("医疗行业的合规要求和专业知识")
        
        if any(keyword in product_type for keyword in ['金融', 'finance', 'fintech']):
            barriers.append("金融行业的监管要求和信任建立")
        
        if any(keyword in product_type for keyword in ['教育', 'education', 'edtech']):
            barriers.append("教育内容的质量和权威性")
        
        if any(keyword in product_type for keyword in ['b2b', 'enterprise']):
            barriers.append("企业级销售渠道和信任建立")
        
        # 通用壁垒
        barriers.extend([
            "品牌认知度和用户信任",
            "早期用户社区的网络效应",
            "SEO积累和内容营销资产"
        ])
        
        return list(set(barriers))[:5]  # 去重并限制数量
    
    def _generate_overall_assessment(self, evaluation: Dict[str, Any]) -> str:
        """生成总体评估"""
        difficulty = evaluation.get("difficulty_level", "")
        challenges = len(evaluation.get("core_challenges", []))
        barriers = len([b for b in evaluation.get("barriers", {}).values() if b])
        
        # 基于各项指标生成总体评估
        if "🟢" in difficulty and challenges <= 2 and barriers <= 2:
            assessment = """
技术实现相对简单，主要依赖现有AI API的组合。独立开发者可以快速构建MVP，
但需要关注差异化定位和细分市场。建议：
1. 快速验证细分场景
2. 专注特定用户群体
3. 通过内容营销建立权威性
"""
        elif "🟡" in difficulty or (challenges > 2 and challenges <= 3):
            assessment = """
技术实现中等难度，需要一定的领域知识和产品设计能力。独立开发者需要：
1. 深入理解目标用户痛点
2. 利用AI工具加速开发
3. 找到未被满足的细分需求
4. 建立早期用户社区
"""
        elif "🔴" in difficulty or challenges > 3:
            assessment = """
技术和商业壁垒较高，独立开发者面临较大挑战。建议策略：
1. 寻找合作伙伴弥补行业经验
2. 从更细分的利基市场切入
3. 重点突破1-2个核心功能
4. 考虑开源策略建立社区
"""
        else:  # 极难
            assessment = """
极高的技术或行业壁垒，不建议独立开发者直接复刻。可考虑：
1. 作为该产品的补充工具
2. 服务该产品未覆盖的长尾市场
3. 提供集成或增值服务
4. 等待市场成熟后的机会
"""
        
        return assessment.strip()
    
    def generate_replication_strategy(
        self,
        evaluation: Dict[str, Any],
        product_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成复刻策略建议
        
        Args:
            evaluation: 复刻难度评估结果
            product_info: 产品信息
            
        Returns:
            复刻策略建议
        """
        strategy = {
            "mvp_features": [],
            "tech_stack_recommendation": [],
            "differentiation_points": [],
            "go_to_market": [],
            "timeline_estimate": ""
        }
        
        difficulty = evaluation.get("difficulty_level", "")
        
        # MVP功能建议
        if "🟢" in difficulty or "🟡" in difficulty:
            strategy["mvp_features"] = [
                "核心功能的简化版本",
                "基础的用户界面",
                "使用现成的AI API (OpenAI/Anthropic)",
                "简单的用户认证系统"
            ]
            strategy["timeline_estimate"] = "1-2个月构建MVP"
        else:
            strategy["mvp_features"] = [
                "选择一个最核心的使用场景",
                "极简的功能实现",
                "先验证市场需求",
                "逐步增加复杂功能"
            ]
            strategy["timeline_estimate"] = "2-3个月验证可行性"
        
        # 技术栈推荐
        strategy["tech_stack_recommendation"] = [
            "前端：Next.js + Tailwind CSS (快速开发)",
            "后端：Vercel/Railway (简化部署)",
            "数据库：Supabase (开箱即用)",
            "AI集成：OpenRouter (多模型支持)",
            "认证：Clerk/Auth0 (现成方案)"
        ]
        
        # 差异化建议
        strategy["differentiation_points"] = [
            "专注特定行业或用户群体",
            "本地化优势（语言/文化）",
            "更好的用户体验设计",
            "开源社区驱动",
            "价格优势或免费增值模式"
        ]
        
        # 市场策略
        strategy["go_to_market"] = [
            "Product Hunt发布获得初始用户",
            "在相关社区（Reddit/Discord）推广",
            "内容营销建立SEO优势",
            "寻找微影响力KOL合作",
            "提供限时优惠吸引早期用户"
        ]
        
        return strategy