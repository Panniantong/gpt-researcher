"""
Competitor identification and analysis module
竞品识别和分析模块
"""

from typing import List, Dict, Tuple, Optional, Any
import re
from dataclasses import dataclass


@dataclass 
class Competitor:
    """竞品信息数据结构"""
    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    key_features: List[str] = None
    pricing: Optional[str] = None
    market_position: Optional[str] = None
    strengths: List[str] = None
    weaknesses: List[str] = None


class CompetitorAnalyzer:
    """
    竞品分析器
    负责识别竞品、提取对比信息、生成评分矩阵
    """
    
    def __init__(self):
        self.competitors: List[Competitor] = []
        self.scoring_metrics: List[str] = []
        self.scoring_matrix: Dict[str, Dict[str, float]] = {}
    
    async def identify_competitors(self, product_name: str, search_results: List[Dict]) -> List[str]:
        """
        从搜索结果中识别主要竞品
        
        Args:
            product_name: 目标产品名称
            search_results: 搜索结果列表
            
        Returns:
            竞品名称列表
        """
        competitor_names = set()
        
        # 常见的竞品识别模式
        patterns = [
            rf"{product_name}\s+vs\s+(\w+)",
            rf"{product_name}\s+alternatives?\s+like\s+(\w+)",
            rf"competitors?\s+(?:of|to)\s+{product_name}.*?(\w+)",
            rf"(\w+)\s+vs\s+{product_name}",
            rf"similar\s+to\s+{product_name}.*?(\w+)",
            rf"better\s+than\s+{product_name}.*?(\w+)"
        ]
        
        # 从搜索结果中提取竞品名称
        for result in search_results:
            text = result.get("content", "") + " " + result.get("title", "")
            text = text.lower()
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                competitor_names.update(matches)
        
        # 过滤掉常见的非产品词汇
        exclude_words = {"the", "and", "or", "for", "with", "best", "top", "free", "paid"}
        competitor_names = {name for name in competitor_names if name.lower() not in exclude_words}
        
        # 返回前5个最相关的竞品
        return list(competitor_names)[:5]
    
    def extract_competitor_features(self, competitor_name: str, search_results: List[Dict]) -> Competitor:
        """
        提取竞品的详细特征信息
        
        Args:
            competitor_name: 竞品名称
            search_results: 关于该竞品的搜索结果
            
        Returns:
            竞品信息对象
        """
        competitor = Competitor(name=competitor_name)
        
        # TODO: 实现特征提取逻辑
        # 1. 提取产品描述
        # 2. 识别关键功能
        # 3. 获取定价信息
        # 4. 分析市场定位
        # 5. 总结优劣势
        
        return competitor
    
    def define_scoring_metrics(self, product_category: str) -> List[str]:
        """
        根据产品类别定义评分指标
        
        Args:
            product_category: 产品类别
            
        Returns:
            评分指标列表
        """
        # 通用评分指标
        base_metrics = ["用户体验", "功能完整性", "性价比", "技术创新"]
        
        # 根据类别添加特定指标
        category_metrics = {
            "saas": ["集成能力", "扩展性", "安全性"],
            "ai_tool": ["模型质量", "响应速度", "准确率"],
            "developer_tool": ["API友好度", "文档质量", "社区活跃度"],
            "productivity": ["易用性", "协作功能", "移动支持"],
            "marketing": ["分析能力", "自动化程度", "ROI"]
        }
        
        # 合并指标
        specific_metrics = category_metrics.get(product_category.lower(), [])
        self.scoring_metrics = base_metrics + specific_metrics
        
        return self.scoring_metrics[:6]  # 最多返回6个指标
    
    def generate_scoring_matrix(self, target_product: str, competitors: List[str], 
                              scores: Optional[Dict[str, Dict[str, float]]] = None) -> Dict[str, Any]:
        """
        生成竞品评分矩阵
        
        Args:
            target_product: 目标产品名称
            competitors: 竞品列表（最多2个）
            scores: 预设的评分数据（可选）
            
        Returns:
            评分矩阵数据
        """
        # 确保只比较2个竞品
        competitors = competitors[:2]
        all_products = [target_product] + competitors
        
        if not scores:
            # 如果没有提供评分，生成占位符
            scores = {}
            for product in all_products:
                scores[product] = {metric: 0.0 for metric in self.scoring_metrics}
        
        self.scoring_matrix = scores
        
        return {
            "metrics": self.scoring_metrics,
            "scores": self.scoring_matrix
        }
    
    def analyze_competitive_advantage(self, target_product: str) -> str:
        """
        分析目标产品的竞争优势
        
        Args:
            target_product: 目标产品名称
            
        Returns:
            竞争优势分析文本
        """
        if not self.scoring_matrix or target_product not in self.scoring_matrix:
            return "⚠︎ Info insufficient - 需要先生成评分矩阵"
        
        # 分析每个指标上的表现
        advantages = []
        target_scores = self.scoring_matrix[target_product]
        
        for metric, score in target_scores.items():
            # 比较与竞品的得分
            is_leading = True
            for competitor, comp_scores in self.scoring_matrix.items():
                if competitor != target_product and comp_scores.get(metric, 0) >= score:
                    is_leading = False
                    break
            
            if is_leading and score > 0:
                advantages.append(metric)
        
        if advantages:
            return f"{target_product}在{', '.join(advantages)}等方面领先竞品，形成差异化竞争优势"
        else:
            return f"{target_product}需要在核心指标上进一步提升以建立竞争优势"
    
    def get_market_position_analysis(self, target_product: str, market_data: Dict) -> Dict[str, str]:
        """
        分析市场定位
        
        Args:
            target_product: 目标产品
            market_data: 市场数据
            
        Returns:
            市场定位分析
        """
        return {
            "arena_description": market_data.get("market_overview", "⚠︎ Info insufficient"),
            "leading_logic": self.analyze_competitive_advantage(target_product)
        }