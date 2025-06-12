"""
基础信息获取模块
获取产品的基本信息：名称、描述、类型、团队规模等
"""
import json
import re
from typing import Dict, Optional, Any
from urllib.parse import urlparse

from competitive_intelligence.prompts.competitive_prompts import BASIC_INFO_PROMPT
from competitive_intelligence.utils.llm_helper import get_llm_response


class BasicInfoExtractor:
    """基础信息提取器"""
    
    def __init__(self, llm_provider: str = None, model: str = None):
        self.llm_provider = llm_provider
        self.model = model
    
    async def extract_from_content(self, content: str, url: str = None) -> Dict[str, Any]:
        """
        从网页内容中提取基础信息
        
        Args:
            content: 网页内容
            url: 网页URL（可选）
            
        Returns:
            包含基础信息的字典
        """
        # 使用LLM提取信息
        prompt = BASIC_INFO_PROMPT.format(content=content[:8000])  # 限制内容长度
        
        try:
            response = await get_llm_response(
                prompt, 
                self.llm_provider, 
                self.model
            )
            
            # 尝试解析JSON响应
            try:
                # 提取JSON部分（如果响应包含其他文本）
                json_match = re.search(r'\{[\s\S]*\}', response)
                if json_match:
                    info = json.loads(json_match.group())
                else:
                    info = json.loads(response)
            except json.JSONDecodeError:
                # 如果JSON解析失败，返回原始响应
                info = {"raw_response": response}
            
            # 添加URL信息
            if url and "url" not in info:
                info["url"] = url
            
            # 尝试推断团队规模
            if "team_size" not in info:
                info["team_size"] = self._infer_team_size(content)
            
            return info
            
        except Exception as e:
            return {
                "error": str(e),
                "url": url
            }
    
    def _infer_team_size(self, content: str) -> str:
        """
        从内容中推断团队规模
        
        Args:
            content: 网页内容
            
        Returns:
            团队规模分类
        """
        content_lower = content.lower()
        
        # 独立开发者的信号
        solo_signals = [
            "solo developer", "indie developer", "built by", "created by",
            "i built", "i created", "个人开发", "独立开发"
        ]
        
        # 小团队的信号
        small_team_signals = [
            "our small team", "we are a team of", "team of 2", "team of 3",
            "team of 4", "team of 5", "co-founder"
        ]
        
        # 大团队的信号
        large_team_signals = [
            "join our team", "we're hiring", "careers", "20+ employees",
            "50+ employees", "100+ employees"
        ]
        
        # 检查信号
        if any(signal in content_lower for signal in solo_signals):
            return "独立开发者"
        elif any(signal in content_lower for signal in large_team_signals):
            return "大团队(20+人)"
        elif any(signal in content_lower for signal in small_team_signals):
            return "小团队(2-5人)"
        else:
            # 默认返回中型团队
            return "中型团队(6-20人)"
    
    
    def validate_info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证和清理提取的信息
        
        Args:
            info: 提取的信息字典
            
        Returns:
            验证后的信息字典
        """
        required_fields = ["name", "one_liner", "type"]
        validated = {}
        
        for field in required_fields:
            if field in info and info[field]:
                validated[field] = info[field]
            else:
                validated[field] = f"⚠︎ {field} not found"
        
        # 复制其他字段
        optional_fields = ["url", "launch_status", "founded", "team_size"]
        for field in optional_fields:
            if field in info:
                validated[field] = info[field]
        
        return validated