"""
竞品调研 Agent
基于 gpt-researcher 的专门用于产品竞品调研的智能代理
"""
import asyncio
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
import json

from gpt_researcher import GPTResearcher
from gpt_researcher.config import Config
from gpt_researcher.utils.llm import get_llm
from gpt_researcher.scraper import Scraper
from gpt_researcher.utils.workers import WorkerPool

from .modules.basic_info import BasicInfoExtractor
from .modules.founder_analysis import FounderAnalyzer
from .modules.eight_dimensions import EightDimensionsAnalyzer
from .modules.marketing_intel import MarketingIntelAnalyzer
from .modules.replication_eval import ReplicationEvaluator
from .modules.executive_summary import ExecutiveSummaryGenerator


class CompetitiveIntelligenceAgent:
    """竞品调研智能代理"""
    
    def __init__(
        self,
        query: str = None,
        product_url: str = None,
        llm_provider: str = None,
        model: str = None,
        report_type: str = "competitive_analysis",
        config_path: str = None,
        websocket = None
    ):
        """
        初始化竞品调研Agent
        
        Args:
            query: 产品名称或查询
            product_url: 产品网址
            llm_provider: LLM提供商
            model: 模型名称
            report_type: 报告类型
            config_path: 配置文件路径
            websocket: WebSocket连接（用于实时更新）
        """
        self.query = query
        self.product_url = product_url
        self.websocket = websocket
        
        # 配置
        self.config = Config(config_path)
        self.llm_provider = llm_provider or self.config.fast_llm_provider
        self.model = model or self.config.fast_llm_model
        
        # 初始化各个分析模块
        self.basic_info_extractor = BasicInfoExtractor(self.llm_provider, self.model)
        self.founder_analyzer = FounderAnalyzer(self.llm_provider, self.model)
        self.eight_dimensions_analyzer = EightDimensionsAnalyzer(self.llm_provider, self.model)
        self.marketing_analyzer = MarketingIntelAnalyzer(self.llm_provider, self.model)
        self.replication_evaluator = ReplicationEvaluator(self.llm_provider, self.model)
        self.summary_generator = ExecutiveSummaryGenerator(self.llm_provider, self.model)
        
        # 初始化工作池
        self.worker_pool = WorkerPool(max_workers=5)
        
        # 初始化检索器
        from gpt_researcher.actions.retriever import get_retrievers
        self.retrievers = get_retrievers({}, self.config)
        self._retriever = self.retrievers[0] if self.retrievers else None
        
        # 存储分析结果
        self.results = {
            "basic_info": {},
            "founder_analysis": {},
            "eight_dimensions": {},
            "marketing_intel": {},
            "replication_eval": {},
            "executive_summary": {},
            "sources": []
        }
    
    async def run_research(self) -> str:
        """
        运行完整的竞品调研流程
        
        Returns:
            格式化的调研报告
        """
        try:
            # 1. 获取基础信息
            await self._update_status("🔍 正在获取产品基础信息...")
            await self._extract_basic_info()
            
            # 2. 创始人背景调研
            await self._update_status("👤 正在调研创始人/团队背景...")
            await self._research_founder_background()
            
            # 3. 八维分析
            await self._update_status("📊 正在进行八维深度分析...")
            await self._analyze_eight_dimensions()
            
            # 4. 营销情报分析
            await self._update_status("📈 正在分析营销策略...")
            await self._analyze_marketing_strategy()
            
            # 5. 复刻难度评估
            await self._update_status("🔧 正在评估复刻难度...")
            await self._evaluate_replication_difficulty()
            
            # 6. 生成执行摘要
            await self._update_status("📝 正在生成执行摘要...")
            await self._generate_executive_summary()
            
            # 7. 生成最终报告
            await self._update_status("✅ 正在生成最终报告...")
            report = self._format_final_report()
            
            return report
            
        except Exception as e:
            await self._update_status(f"❌ 调研过程中出现错误：{str(e)}")
            raise
    
    async def _extract_basic_info(self):
        """提取基础信息"""
        if self.product_url:
            # 从URL获取信息
            content = await self._scrape_url(self.product_url)
            self.results["basic_info"] = await self.basic_info_extractor.extract_from_content(
                content, 
                self.product_url
            )
        else:
            # 使用搜索获取产品主页
            from gpt_researcher.actions.query_processing import get_search_results
            
            # 搜索产品官网
            search_query = f"{self.query} official website"
            if self._retriever:
                search_results = await get_search_results(
                    search_query,
                    self._retriever,
                    researcher=None
                )
                
                if search_results and len(search_results) > 0:
                    # 获取第一个搜索结果的URL
                    self.product_url = search_results[0].get("href", search_results[0].get("url", ""))
                    if self.product_url:
                        content = await self._scrape_url(self.product_url)
                        self.results["basic_info"] = await self.basic_info_extractor.extract_from_content(
                            content,
                            self.product_url
                        )
                    else:
                        # 使用默认信息
                        self.results["basic_info"] = {
                            "name": self.query,
                            "one_liner": "产品描述未找到",
                            "type": "未知",
                            "team_size": "未知"
                        }
                else:
                    # 如果找不到搜索结果，使用基本信息
                    self.results["basic_info"] = {
                        "name": self.query,
                        "one_liner": "产品描述未找到",
                        "type": "未知",
                        "team_size": "未知"
                    }
            else:
                # 没有检索器可用
                self.results["basic_info"] = {
                    "name": self.query,
                    "one_liner": "产品描述未找到（无搜索API）",
                    "type": "未知",
                    "team_size": "未知"
                }
        
        # 验证基础信息
        self.results["basic_info"] = self.basic_info_extractor.validate_info(
            self.results["basic_info"]
        )
    
    async def _research_founder_background(self):
        """调研创始人背景"""
        product_name = self.results["basic_info"].get("name", self.query)
        
        # 验证产品名称是否有效
        if not product_name or "not found" in product_name.lower() or "⚠" in product_name:
            # 使用原始查询词
            product_name = self.query
        
        # 生成搜索查询
        queries = await self.founder_analyzer.generate_search_queries(
            product_name,
            self.product_url
        )
        
        # 执行搜索
        search_results = await self._perform_searches(queries)
        
        # 分析创始人背景
        self.results["founder_analysis"] = await self.founder_analyzer.analyze_founder_background(
            product_name,
            search_results
        )
        
        # 识别竞争优势
        advantages = self.founder_analyzer.identify_competitive_advantages(
            self.results["founder_analysis"]
        )
        self.results["founder_analysis"]["competitive_advantages"] = advantages
    
    async def _analyze_eight_dimensions(self):
        """进行八维分析"""
        product_info = self.results["basic_info"]
        
        # 生成需要研究的维度的查询
        dimension_queries = await self.eight_dimensions_analyzer.generate_research_queries(
            product_info
        )
        
        # 对每个需要研究的维度执行搜索
        research_results = {}
        for dimension, queries in dimension_queries.items():
            search_results = await self._perform_searches(queries)
            research_results[dimension] = search_results
        
        # 执行八维分析
        self.results["eight_dimensions"] = await self.eight_dimensions_analyzer.analyze_all_dimensions(
            product_info,
            research_results
        )
    
    async def _analyze_marketing_strategy(self):
        """分析营销策略"""
        product_name = self.results["basic_info"].get("name", self.query)
        
        # 验证产品名称是否有效
        if not product_name or "not found" in product_name.lower() or "⚠" in product_name:
            # 使用原始查询词
            product_name = self.query
        
        # 生成营销相关查询
        queries = await self.marketing_analyzer.generate_marketing_research_queries(
            product_name,
            self.product_url
        )
        
        # 执行搜索
        search_results = await self._perform_searches(queries)
        
        # 分析营销策略
        self.results["marketing_intel"] = await self.marketing_analyzer.analyze_marketing_strategy(
            product_name,
            search_results
        )
        
        # 分析内容策略
        content_strategy = self.marketing_analyzer.analyze_content_strategy(search_results)
        self.results["marketing_intel"]["content_strategy_analysis"] = content_strategy
    
    async def _evaluate_replication_difficulty(self):
        """评估复刻难度"""
        product_info = self.results["basic_info"]
        
        # 获取技术架构信息（从Q8）
        tech_architecture = ""
        if "Q8" in self.results["eight_dimensions"]:
            q8_result = self.results["eight_dimensions"]["Q8"]
            if hasattr(q8_result, 'answer'):
                tech_architecture = q8_result.answer
        
        # 获取创始人优势
        founder_advantages = self.results["founder_analysis"].get("unfair_advantages", [])
        
        # 评估复刻难度
        self.results["replication_eval"] = await self.replication_evaluator.evaluate_replication_difficulty(
            product_info,
            tech_architecture,
            founder_advantages
        )
        
        # 生成复刻策略
        strategy = self.replication_evaluator.generate_replication_strategy(
            self.results["replication_eval"],
            product_info
        )
        self.results["replication_eval"]["strategy"] = strategy
    
    async def _generate_executive_summary(self):
        """生成执行摘要"""
        summary = await self.summary_generator.generate_summary(
            self.results["basic_info"],
            self.results["founder_analysis"],
            self.results["eight_dimensions"],
            self.results["marketing_intel"],
            self.results["replication_eval"]
        )
        
        # 生成可执行洞察
        insights = self.summary_generator.generate_actionable_insights(
            summary,
            self.results["replication_eval"]
        )
        summary["actionable_insights"] = insights
        
        self.results["executive_summary"] = summary
    
    async def _perform_searches(self, queries: List[str]) -> List[Dict[str, Any]]:
        """执行搜索查询"""
        from gpt_researcher.actions.query_processing import get_search_results
        
        all_results = []
        
        # 使用检索器进行搜索
        if not self._retriever:
            print("Warning: No retriever available, skipping search")
            return []
        
        for query in queries[:5]:  # 限制查询数量
            try:
                # 获取搜索结果
                search_results = await get_search_results(
                    query, 
                    self._retriever,
                    researcher=None
                )
                
                # 处理搜索结果
                for result in search_results[:3]:  # 每个查询限制3个结果
                    url = result.get("href", result.get("url", ""))
                    if url:
                        try:
                            content = await self._scrape_url(url)
                            
                            all_results.append({
                                "query": query,
                                "url": url,
                                "title": result.get("title", self._extract_title(content)),
                                "content": content[:1000]  # 限制内容长度
                            })
                            
                            # 添加到源列表
                            if url not in self.results["sources"]:
                                self.results["sources"].append(url)
                                
                        except Exception as e:
                            print(f"Error scraping {url}: {e}")
                            # 即使抓取失败，也保存搜索结果
                            all_results.append({
                                "query": query,
                                "url": url,
                                "title": result.get("title", ""),
                                "content": result.get("body", "")[:1000]
                            })
                            
            except Exception as e:
                print(f"Error searching for '{query}': {e}")
                continue
        
        return all_results
    
    def _extract_title(self, html_content: str) -> str:
        """从HTML中提取标题"""
        import re
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
        return title_match.group(1) if title_match else "无标题"
    
    async def _scrape_url(self, url: str, timeout: int = 10) -> str:
        """抓取单个URL的内容"""
        try:
            # 使用超时控制
            scraper = Scraper(
                [url], 
                user_agent=self.config.user_agent,
                scraper=self.config.scraper,
                worker_pool=self.worker_pool
            )
            
            # 设置超时
            results = await asyncio.wait_for(
                scraper.run(),
                timeout=timeout
            )
            
            if results and len(results) > 0:
                content = results[0].get('raw_content', '')
                # 如果内容太短，可能是抓取失败
                if len(content) < 100:
                    print(f"Warning: Content too short for {url}")
                return content
            return ""
        except asyncio.TimeoutError:
            print(f"Timeout scraping {url} after {timeout}s")
            return ""
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""
    
    async def _update_status(self, message: str):
        """更新状态（通过WebSocket或打印）"""
        if self.websocket:
            await self.websocket.send_json({
                "type": "status",
                "message": message
            })
        else:
            print(message)
    
    def _format_final_report(self) -> str:
        """格式化最终报告"""
        report = []
        
        # 标题
        product_name = self.results["basic_info"].get("name", self.query)
        report.append(f"# 竞品调研报告：{product_name}")
        report.append("")
        
        # 基础信息
        report.append("## 【基础信息 | Facts】")
        info = self.results["basic_info"]
        report.append(f"**Team Size**: {info.get('team_size', 'N/A')}")
        report.append(f"**Name**: {info.get('name', 'N/A')}")
        report.append(f"**One-liner**: {info.get('one_liner', 'N/A')}")
        report.append(f"**Type**: {info.get('type', 'N/A')}")
        report.append(f"**URL**: {info.get('url', 'N/A')}")
        report.append(f"**Launch Status**: {info.get('launch_status', 'N/A')}")
        report.append(f"**Founded**: {info.get('founded', 'N/A')}")
        report.append("")
        
        # 创始人/团队背景分析
        report.append("## 【创始人/团队背景分析 | Founder Intelligence】")
        founder = self.results["founder_analysis"]
        
        report.append("### 👤 核心人物画像")
        profile = founder.get("profile", {})
        report.append(f"- **身份背景**：{profile.get('background', 'N/A')}")
        report.append(f"- **技术能力**：{profile.get('technical_skills', 'N/A')}")
        report.append(f"- **行业深度**：{profile.get('industry_depth', 'N/A')}")
        report.append("")
        
        report.append("### 🎯 不公平优势识别")
        advantages = founder.get("unfair_advantages", [])
        for advantage in advantages[:5]:
            report.append(f"- {advantage}")
        report.append("")
        
        report.append("### 💡 'AI + 行业专家' 模式验证")
        ai_expert = founder.get("ai_expert_model", {})
        report.append(f"- 符合模式：{'是' if ai_expert.get('fits_pattern') else '否'}")
        if ai_expert.get("explanation"):
            report.append(f"- 说明：{ai_expert['explanation']}")
        report.append("")
        
        sources = founder.get("sources", [])
        if sources:
            report.append(f"**信息来源**：{' | '.join(sources[:5])}")
        report.append("")
        
        # 八维分析
        report.append("## 【八维分析 | 8 Questions】")
        dimensions = self.results["eight_dimensions"]
        
        for key in sorted(dimensions.keys()):
            analysis = dimensions[key]
            if hasattr(analysis, 'question') and hasattr(analysis, 'answer'):
                report.append(f"### {key} · {analysis.question}")
                report.append(analysis.answer)
                if analysis.sources:
                    report.append(f"来源：{' | '.join(analysis.sources[:3])}")
                report.append("")
        
        # 营销情报
        report.append("## 【营销情报 | Growth Intelligence】")
        marketing = self.results["marketing_intel"]
        
        report.append("### G1 · Growth Timeline & Milestones")
        timeline = marketing.get("growth_timeline", {})
        if timeline.get("launch_phase"):
            report.append(f"- **Launch Phase**: {timeline['launch_phase']}")
        if timeline.get("growth_phase"):
            report.append(f"- **Growth Phase**: {timeline['growth_phase']}")
        report.append("")
        
        report.append("### G2 · Growth Channels & Tactics")
        channels = marketing.get("growth_channels", {})
        if channels.get("primary_channels"):
            report.append(f"- **Primary Channels**: {', '.join(channels['primary_channels'][:3])}")
        if channels.get("signature_tactics"):
            report.append(f"- **Signature Tactics**: {', '.join(channels['signature_tactics'][:3])}")
        report.append("")
        
        # 复刻难度评估
        report.append("## 【复刻难度评估 | Solo Developer Feasibility】")
        replication = self.results["replication_eval"]
        
        report.append(f"### 💻 AI时代技术复刻评估")
        report.append(f"**难度等级**：{replication.get('difficulty_level', 'N/A')}")
        report.append("")
        
        report.append("### ⚡ 核心技术挑战")
        challenges = replication.get("core_challenges", [])
        for i, challenge in enumerate(challenges[:4], 1):
            report.append(f"{i}. {challenge}")
        report.append("")
        
        # 执行摘要
        report.append("## 【Executive Summary】")
        summary = self.results["executive_summary"]
        
        report.append(f"### 🎯 核心洞察")
        report.append(summary.get("core_insights", "N/A"))
        report.append("")
        
        report.append(f"### 🚀 增长模式")
        report.append(summary.get("growth_model", "N/A"))
        report.append("")
        
        report.append(f"### 👑 创始人优势")
        report.append(summary.get("founder_advantages", "N/A"))
        report.append("")
        
        report.append("### 🧩 可迁移要素")
        elements = summary.get("transferable_elements", {})
        for category, items in elements.items():
            if items:
                report.append(f"- **{category.capitalize()}**: {items[0] if items else 'N/A'}")
        report.append("")
        
        report.append("### ⭐ AI时代独立开发者策略")
        report.append(summary.get("indie_developer_strategy", "N/A"))
        report.append("")
        
        # 信息来源
        if self.results["sources"]:
            report.append("## 【信息来源】")
            report.append(f"**Sources**: {' | '.join(self.results['sources'][:10])}")
        
        return "\n".join(report)
    
    async def save_results(self, filepath: str = None):
        """保存调研结果"""
        if not filepath:
            product_name = self.results["basic_info"].get("name", self.query)
            filepath = f"competitive_intel_{product_name.replace(' ', '_')}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        await self._update_status(f"💾 结果已保存到：{filepath}")


# 便捷函数
async def analyze_competitor(
    query: str,
    product_url: str = None,
    llm_provider: str = None,
    model: str = None
) -> str:
    """
    便捷函数：分析竞品
    
    Args:
        query: 产品名称或查询
        product_url: 产品网址（可选）
        llm_provider: LLM提供商
        model: 模型名称
        
    Returns:
        格式化的调研报告
    """
    agent = CompetitiveIntelligenceAgent(
        query=query,
        product_url=product_url,
        llm_provider=llm_provider,
        model=model
    )
    
    return await agent.run_research()