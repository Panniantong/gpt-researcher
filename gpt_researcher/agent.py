# -*- coding: utf-8 -*-
"""
GPT Researcher 核心代理模块

这个模块包含了 GPTResearcher 类，它是整个研究系统的核心控制器。
GPTResearcher 负责协调所有的研究活动，包括：
- 选择合适的AI代理
- 执行研究任务
- 生成研究报告
- 管理研究上下文和成本

作者: GPT Researcher Team
版本: 最新版本
"""

from typing import Any, Optional
import json
import os

# 核心配置和内存模块
from .config import Config  # 配置管理器
from .memory import Memory  # 记忆和嵌入系统
from .utils.enum import ReportSource, ReportType, Tone  # 枚举类型定义
from .llm_provider import GenericLLMProvider  # 通用LLM提供商
from .prompts import get_prompt_family  # 提示词系列获取
from .vector_store import VectorStoreWrapper  # 向量存储包装器

# 研究技能模块 - 各种专业技能的实现
from .skills.researcher import ResearchConductor  # 研究执行器
from .skills.writer import ReportGenerator  # 报告生成器
from .skills.context_manager import ContextManager  # 上下文管理器
from .skills.browser import BrowserManager  # 浏览器管理器
from .skills.curator import SourceCurator  # 来源策展器
from .skills.deep_research import DeepResearchSkill  # 深度研究技能

# 行动模块 - 具体的操作功能
from .actions import (
    add_references,      # 添加引用
    extract_headers,     # 提取标题
    extract_sections,    # 提取章节
    table_of_contents,   # 生成目录
    get_search_results,  # 获取搜索结果
    get_retrievers,      # 获取检索器
    choose_agent         # 选择代理
)


class GPTResearcher:
    """
    GPT研究员 - 智能研究助手的核心类

    这个类是整个GPT Researcher系统的核心控制器，负责：
    1. 协调各种研究技能和工具
    2. 管理研究流程和状态
    3. 生成高质量的研究报告
    4. 处理多种数据源和格式
    5. 提供成本跟踪和日志记录

    主要特性：
    - 支持多种报告类型（研究报告、深度研究、竞争情报等）
    - 集成多个搜索引擎和数据源
    - 智能代理选择和角色分配
    - 向量化存储和语义搜索
    - 实时流式输出和进度跟踪
    """

    def __init__(
        self,
        query: str,                                          # 研究查询问题
        report_type: str = ReportType.ResearchReport.value, # 报告类型
        report_format: str = "markdown",                     # 报告格式
        report_source: str = ReportSource.Web.value,        # 数据源类型
        tone: Tone = Tone.Objective,                         # 报告语调
        source_urls: list[str] | None = None,               # 指定的源URL列表
        document_urls: list[str] | None = None,             # 文档URL列表
        complement_source_urls: bool = False,                # 是否补充源URL
        query_domains: list[str] | None = None,             # 查询域名限制
        documents=None,                                      # LangChain文档对象
        vector_store=None,                                   # 向量存储
        vector_store_filter=None,                           # 向量存储过滤器
        config_path=None,                                   # 配置文件路径
        websocket=None,                                     # WebSocket连接
        agent=None,                                         # 预定义代理
        role=None,                                          # 预定义角色
        parent_query: str = "",                             # 父查询（用于子主题）
        subtopics: list | None = None,                      # 子主题列表
        visited_urls: set | None = None,                    # 已访问URL集合
        verbose: bool = True,                               # 详细输出模式
        context=None,                                       # 预加载上下文
        headers: dict | None = None,                        # HTTP请求头
        max_subtopics: int = 5,                            # 最大子主题数
        log_handler=None,                                   # 日志处理器
        prompt_family: str | None = None,                   # 提示词系列
        mcp_configs: list[dict] | None = None,              # MCP配置列表
        mcp_max_iterations: int | None = None,              # MCP最大迭代次数（已弃用）
        mcp_strategy: str | None = None,                    # MCP执行策略
        **kwargs                                            # 其他关键字参数
    ):
        """
        初始化GPT研究员实例

        这个方法设置了研究员的所有配置和组件，包括：
        - 基础配置（查询、报告类型、格式等）
        - 数据源配置（URL、域名、文档等）
        - 技能组件（研究员、写作者、策展人等）
        - 高级功能（MCP协议、深度研究、向量存储等）

        参数说明:
            query (str): 研究查询或问题 - 这是研究的核心问题
            report_type (str): 要生成的报告类型
                - ResearchReport: 标准研究报告
                - DeepResearch: 深度递归研究
                - DetailedReport: 详细报告
                - SubtopicReport: 子主题报告
                - CompetitiveIntelligence: 竞争情报
            report_format (str): 报告的格式（markdown、pdf、docx等）
            report_source (str): 报告信息的来源（web、local、hybrid等）
            tone (Tone): 报告的语调（客观、正式、友好等）
            source_urls (list[str], optional): 用作来源的特定URL列表
            document_urls (list[str], optional): 用作来源的文档URL列表
            complement_source_urls (bool): 是否用网络搜索补充来源URL
            query_domains (list[str], optional): 限制搜索范围的域名列表
            documents: 用于LangChain集成的文档对象
            vector_store: 用于文档检索的向量存储
            vector_store_filter: 向量存储查询的过滤器
            config_path: 配置文件的路径
            websocket: 用于流式输出的WebSocket连接
            agent: 预定义的代理类型（如果不指定会自动选择）
            role: 预定义的代理角色（如果不指定会自动选择）
            parent_query: 子主题报告的父查询
            subtopics: 要研究的子主题列表
            visited_urls: 已访问URL的集合（用于避免重复访问）
            verbose (bool): 是否输出详细日志
            context: 预加载的研究上下文
            headers (dict, optional): HTTP请求和配置的附加头信息
            max_subtopics (int): 生成的最大子主题数量
            log_handler: 日志事件处理器（用于自定义日志处理）
            prompt_family: 要使用的提示词系列
            mcp_configs (list[dict], optional): MCP（模型上下文协议）服务器配置列表
                每个配置字典可以包含：
                - name (str): MCP服务器名称
                - command (str): 启动服务器的命令
                - args (list[str]): 服务器命令的参数
                - tool_name (str): 在MCP服务器上使用的特定工具
                - env (dict): 服务器的环境变量
                - connection_url (str): WebSocket或HTTP连接的URL
                - connection_type (str): 连接类型（stdio, websocket, http）
                - connection_token (str): 远程连接的认证令牌

                配置示例：
                ```python
                mcp_configs=[{
                    "command": "python",
                    "args": ["my_mcp_server.py"],
                    "name": "search"
                }]
                ```
            mcp_strategy (str, optional): MCP执行策略，控制MCP工具的使用方式：
                - "fast" (默认): 使用原始查询运行一次MCP，性能最佳
                - "deep": 为所有子查询运行MCP，覆盖最全面
                - "disabled": 完全跳过MCP，仅使用传统网络检索器
            **kwargs: 其他关键字参数，用于扩展功能
        """
        # === 基础配置设置 ===
        self.kwargs = kwargs                    # 保存额外的关键字参数
        self.query = query                      # 研究查询问题
        self.report_type = report_type          # 报告类型
        self.cfg = Config(config_path)          # 加载配置文件
        self.cfg.set_verbose(verbose)           # 设置详细输出模式

        # 报告相关配置
        self.report_source = report_source if report_source else getattr(self.cfg, 'report_source', None)
        self.report_format = report_format      # 报告格式（markdown, pdf等）
        self.max_subtopics = max_subtopics      # 最大子主题数量
        self.tone = tone if isinstance(tone, Tone) else Tone.Objective  # 报告语调

        # === 数据源配置 ===
        self.source_urls = source_urls                      # 指定的源URL列表
        self.document_urls = document_urls                  # 文档URL列表
        self.complement_source_urls = complement_source_urls # 是否补充源URL
        self.query_domains = query_domains or []            # 查询域名限制

        # === 研究数据存储 ===
        self.research_sources = []              # 抓取的源列表（包含标题、内容和图片）
        self.research_images = []               # 选中的研究图片列表
        self.documents = documents              # LangChain文档对象

        # === 向量存储配置 ===
        self.vector_store = VectorStoreWrapper(vector_store) if vector_store else None
        self.vector_store_filter = vector_store_filter  # 向量存储过滤器

        # === 通信和界面配置 ===
        self.websocket = websocket              # WebSocket连接（用于实时通信）

        # === 代理和角色配置 ===
        self.agent = agent                      # 预定义的代理类型
        self.role = role                        # 预定义的代理角色

        # === 研究层次结构配置 ===
        self.parent_query = parent_query        # 父查询（用于子主题研究）
        self.subtopics = subtopics or []        # 子主题列表

        # === 状态管理 ===
        self.visited_urls = visited_urls or set()  # 已访问URL集合（避免重复访问）
        self.verbose = verbose                     # 详细输出模式
        self.context = context or []               # 研究上下文数据
        self.headers = headers or {}               # HTTP请求头
        self.research_costs = 0.0                  # 研究成本跟踪

        # === 日志和提示词配置 ===
        self.log_handler = log_handler             # 自定义日志处理器
        self.prompt_family = get_prompt_family(    # 获取提示词系列
            prompt_family or self.cfg.prompt_family, self.cfg
        )

        # === MCP（模型上下文协议）配置处理 ===
        self.mcp_configs = mcp_configs          # 保存MCP配置
        if mcp_configs:
            self._process_mcp_configs(mcp_configs)  # 处理MCP配置

        # === 核心组件初始化 ===
        # 获取所有可用的检索器（搜索引擎、API等）
        self.retrievers = get_retrievers(self.headers, self.cfg)

        # 初始化记忆系统（用于向量化存储和语义搜索）
        self.memory = Memory(
            self.cfg.embedding_provider,    # 嵌入提供商（OpenAI、Azure等）
            self.cfg.embedding_model,       # 嵌入模型名称
            **self.cfg.embedding_kwargs     # 嵌入模型的额外参数
        )

        # === 技能组件初始化 ===
        # 每个组件都是一个专门的技能模块，负责特定的功能
        self.research_conductor: ResearchConductor = ResearchConductor(self)  # 研究执行器
        self.report_generator: ReportGenerator = ReportGenerator(self)        # 报告生成器
        self.context_manager: ContextManager = ContextManager(self)           # 上下文管理器
        self.scraper_manager: BrowserManager = BrowserManager(self)           # 浏览器管理器
        self.source_curator: SourceCurator = SourceCurator(self)             # 来源策展器

        # === 深度研究技能（可选） ===
        # 只有在报告类型为深度研究时才初始化深度研究技能
        self.deep_researcher: Optional[DeepResearchSkill] = None
        if report_type == ReportType.DeepResearch.value:
            self.deep_researcher = DeepResearchSkill(self)  # 深度研究技能

        # === MCP策略配置（向后兼容） ===
        # 解析MCP执行策略，支持新旧参数格式
        self.mcp_strategy = self._resolve_mcp_strategy(mcp_strategy, mcp_max_iterations)

    def _resolve_mcp_strategy(self, mcp_strategy: str | None, mcp_max_iterations: int | None) -> str:
        """
        解析MCP执行策略，支持多种配置源和向后兼容性

        MCP（模型上下文协议）策略决定了如何使用MCP工具：
        - "fast": 快速模式，只对原始查询运行一次MCP，性能最佳
        - "deep": 深度模式，对所有子查询都运行MCP，覆盖最全面
        - "disabled": 禁用模式，完全跳过MCP，只使用传统检索器

        解析优先级：
        1. 参数 mcp_strategy（新方法，优先级最高）
        2. 参数 mcp_max_iterations（旧方法，向后兼容）
        3. 配置文件中的 MCP_STRATEGY
        4. 默认值 "fast"

        参数:
            mcp_strategy: 新的策略参数
            mcp_max_iterations: 旧的迭代次数参数（向后兼容）

        返回:
            str: 解析后的策略 ("fast", "deep", 或 "disabled")
        """
        # 优先级1: 如果提供了mcp_strategy参数，优先使用
        if mcp_strategy is not None:
            # 支持新的策略名称
            if mcp_strategy in ["fast", "deep", "disabled"]:
                return mcp_strategy
            # 支持旧的策略名称（向后兼容）
            elif mcp_strategy == "optimized":
                import logging
                logging.getLogger(__name__).warning("mcp_strategy 'optimized' 已弃用，请使用 'fast' 代替")
                return "fast"
            elif mcp_strategy == "comprehensive":
                import logging
                logging.getLogger(__name__).warning("mcp_strategy 'comprehensive' 已弃用，请使用 'deep' 代替")
                return "deep"
            else:
                import logging
                logging.getLogger(__name__).warning(f"无效的 mcp_strategy '{mcp_strategy}'，使用默认值 'fast'")
                return "fast"

        # 优先级2: 转换mcp_max_iterations参数（向后兼容）
        if mcp_max_iterations is not None:
            import logging
            logging.getLogger(__name__).warning("mcp_max_iterations 已弃用，请使用 mcp_strategy 代替")

            # 根据迭代次数映射到新的策略
            if mcp_max_iterations == 0:
                return "disabled"    # 0次迭代 = 禁用MCP
            elif mcp_max_iterations == 1:
                return "fast"        # 1次迭代 = 快速模式
            elif mcp_max_iterations == -1:
                return "deep"        # -1表示无限制 = 深度模式
            else:
                # 其他任何数字都视为快速模式
                return "fast"

        # 优先级3: 使用配置文件设置
        if hasattr(self.cfg, 'mcp_strategy'):
            config_strategy = self.cfg.mcp_strategy
            # 支持新的策略名称
            if config_strategy in ["fast", "deep", "disabled"]:
                return config_strategy
            # 支持旧的策略名称（向后兼容）
            elif config_strategy == "optimized":
                return "fast"
            elif config_strategy == "comprehensive":
                return "deep"

        # 优先级4: 默认使用快速模式
        return "fast"

    def _process_mcp_configs(self, mcp_configs: list[dict]) -> None:
        """
        处理MCP配置列表，验证配置并自动添加MCP检索器

        这个方法负责：
        1. 验证MCP服务器配置的有效性
        2. 智能地将MCP添加到检索器列表中
        3. 尊重用户的显式配置选择

        MCP（模型上下文协议）允许AI模型与外部工具和数据源进行交互，
        扩展了研究员的能力范围。

        参数:
            mcp_configs (list[dict]): MCP服务器配置字典列表
        """
        # 检查用户是否通过环境变量显式设置了RETRIEVER
        user_set_retriever = os.getenv("RETRIEVER") is not None

        if not user_set_retriever:
            # 只有在用户没有显式设置检索器时才自动添加MCP
            if hasattr(self.cfg, 'retrievers') and self.cfg.retrievers:
                # 如果配置中设置了检索器（但不是通过环境变量）
                if isinstance(self.cfg.retrievers, str):
                    current_retrievers = set(self.cfg.retrievers.split(","))
                else:
                    current_retrievers = set(self.cfg.retrievers)

                # 如果MCP不在当前检索器列表中，则添加它
                if "mcp" not in current_retrievers:
                    current_retrievers.add("mcp")
                    self.cfg.retrievers = ",".join(filter(None, current_retrievers))
            else:
                # 没有配置检索器，使用MCP作为默认检索器
                self.cfg.retrievers = "mcp"
        # 如果用户显式设置了RETRIEVER环境变量，尊重他们的选择，不自动添加MCP

        # 保存MCP配置供MCP检索器使用
        self.mcp_configs = mcp_configs

    async def _log_event(self, event_type: str, **kwargs):
        """
        日志事件处理辅助方法

        这个方法负责处理研究过程中的各种日志事件，包括：
        - 工具使用事件
        - 代理行动事件
        - 研究步骤事件

        支持自定义日志处理器和标准日志记录的双重机制，
        确保重要事件不会丢失。

        参数:
            event_type (str): 事件类型 ("tool", "action", "research")
            **kwargs: 事件的详细信息
        """
        if self.log_handler:
            try:
                # 根据事件类型调用相应的日志处理方法
                if event_type == "tool":
                    # 工具启动事件
                    await self.log_handler.on_tool_start(kwargs.get('tool_name', ''), **kwargs)
                elif event_type == "action":
                    # 代理行动事件
                    await self.log_handler.on_agent_action(kwargs.get('action', ''), **kwargs)
                elif event_type == "research":
                    # 研究步骤事件
                    await self.log_handler.on_research_step(kwargs.get('step', ''), kwargs.get('details', {}))

                # 添加直接日志记录作为备份
                import logging
                research_logger = logging.getLogger('research')
                research_logger.info(f"{event_type}: {json.dumps(kwargs, default=str)}")

            except Exception as e:
                # 如果日志处理出错，记录错误信息
                import logging
                logging.getLogger('research').error(f"日志事件处理错误: {e}", exc_info=True)

    async def conduct_research(self, on_progress=None):
        """
        执行研究任务的核心方法

        这是GPT研究员的主要工作流程，包括：
        1. 记录研究开始事件
        2. 处理特殊研究类型（如深度研究）
        3. 选择合适的AI代理和角色
        4. 执行实际的研究工作
        5. 返回研究上下文

        参数:
            on_progress: 进度回调函数，用于实时更新研究进度

        返回:
            研究上下文数据，包含所有收集到的信息
        """
        # 记录研究开始事件
        await self._log_event("research", step="start", details={
            "query": self.query,           # 研究查询
            "report_type": self.report_type, # 报告类型
            "agent": self.agent,           # 当前代理
            "role": self.role              # 当前角色
        })

        # 特殊处理：深度研究有独立的处理流程
        if self.report_type == ReportType.DeepResearch.value and self.deep_researcher:
            return await self._handle_deep_research(on_progress)

        # 如果没有预设代理和角色，则自动选择最合适的
        if not (self.agent and self.role):
            await self._log_event("action", action="choose_agent")

            # 使用AI智能选择最适合当前查询的代理和角色
            self.agent, self.role = await choose_agent(
                query=self.query,              # 研究查询
                cfg=self.cfg,                  # 配置对象
                parent_query=self.parent_query, # 父查询（如果有）
                cost_callback=self.add_costs,   # 成本回调函数
                headers=self.headers,           # HTTP头信息
                prompt_family=self.prompt_family, # 提示词系列
                **self.kwargs                   # 其他参数
            )

            # 记录代理选择结果
            await self._log_event("action", action="agent_selected", details={
                "agent": self.agent,
                "role": self.role
            })

        # 开始执行研究
        await self._log_event("research", step="conducting_research", details={
            "agent": self.agent,
            "role": self.role
        })

        # 委托给研究执行器进行实际的研究工作
        self.context = await self.research_conductor.conduct_research()

        # 记录研究完成事件
        await self._log_event("research", step="research_completed", details={
            "context_length": len(self.context)  # 上下文数据长度
        })

        return self.context

    async def _handle_deep_research(self, on_progress=None):
        """
        处理深度研究的执行和日志记录

        深度研究是一种高级研究模式，具有以下特点：
        1. 递归式研究：从初始查询开始，逐层深入
        2. 多维度探索：在广度和深度两个维度上扩展研究
        3. 并发处理：支持多个研究任务同时进行
        4. 智能去重：避免重复访问相同的信息源

        参数:
            on_progress: 进度回调函数，用于实时更新研究进度

        返回:
            深度研究的上下文数据
        """
        # 记录深度研究配置初始化
        await self._log_event("research", step="deep_research_initialize", details={
            "type": "deep_research",                           # 研究类型
            "breadth": self.deep_researcher.breadth,           # 广度参数（每层查询数量）
            "depth": self.deep_researcher.depth,               # 深度参数（递归层数）
            "concurrency": self.deep_researcher.concurrency_limit  # 并发限制
        })

        # 记录深度研究开始
        await self._log_event("research", step="deep_research_start", details={
            "query": self.query,                               # 初始查询
            "breadth": self.deep_researcher.breadth,           # 广度配置
            "depth": self.deep_researcher.depth,               # 深度配置
            "concurrency": self.deep_researcher.concurrency_limit  # 并发配置
        })

        # 运行深度研究并获取上下文
        self.context = await self.deep_researcher.run(on_progress=on_progress)

        # 获取总研究成本
        total_costs = self.get_costs()

        # 记录深度研究完成，包含成本信息
        await self._log_event("research", step="deep_research_complete", details={
            "context_length": len(self.context),      # 上下文数据长度
            "visited_urls": len(self.visited_urls),   # 访问的URL数量
            "total_costs": total_costs                # 总成本
        })

        # 记录最终成本更新
        await self._log_event("research", step="cost_update", details={
            "cost": total_costs,                      # 当前成本
            "total_cost": total_costs,                # 总成本
            "research_type": "deep_research"          # 研究类型
        })

        # 返回研究上下文
        return self.context

    async def write_report(self, existing_headers: list = [], relevant_written_contents: list = [], ext_context=None, custom_prompt="") -> str:
        """
        生成研究报告的主要方法

        这个方法负责将研究上下文转换为结构化的报告，支持：
        1. 使用现有标题结构
        2. 整合相关的已写内容
        3. 使用外部上下文或内部研究结果
        4. 应用自定义提示词

        参数:
            existing_headers (list): 现有的报告标题列表
            relevant_written_contents (list): 相关的已写内容列表
            ext_context: 外部上下文数据（如果不提供则使用内部研究结果）
            custom_prompt (str): 自定义提示词

        返回:
            str: 生成的报告内容
        """
        await self._log_event("research", step="writing_report", details={
            "existing_headers": existing_headers,
            "context_source": "external" if ext_context else "internal"
        })

        # 委托给报告生成器进行实际的报告写作
        report = await self.report_generator.write_report(
            existing_headers=existing_headers,                    # 现有标题
            relevant_written_contents=relevant_written_contents, # 相关内容
            ext_context=ext_context or self.context,            # 上下文数据
            custom_prompt=custom_prompt                          # 自定义提示
        )

        await self._log_event("research", step="report_completed", details={
            "report_length": len(report)  # 报告长度
        })
        return report

    async def write_report_conclusion(self, report_body: str) -> str:
        """
        为报告生成结论部分

        参数:
            report_body (str): 报告主体内容

        返回:
            str: 生成的结论内容
        """
        await self._log_event("research", step="writing_conclusion")
        conclusion = await self.report_generator.write_report_conclusion(report_body)
        await self._log_event("research", step="conclusion_completed")
        return conclusion

    async def write_introduction(self):
        """
        为报告生成引言部分

        返回:
            str: 生成的引言内容
        """
        await self._log_event("research", step="writing_introduction")
        intro = await self.report_generator.write_introduction()
        await self._log_event("research", step="introduction_completed")
        return intro

    async def quick_search(self, query: str, query_domains: list[str] = None) -> list[Any]:
        """
        执行快速搜索

        使用第一个可用的检索器进行快速搜索，适用于：
        1. 获取即时信息
        2. 验证特定事实
        3. 补充研究数据

        参数:
            query (str): 搜索查询
            query_domains (list[str], optional): 限制搜索的域名列表

        返回:
            list[Any]: 搜索结果列表
        """
        return await get_search_results(query, self.retrievers[0], query_domains=query_domains)

    async def get_subtopics(self):
        """
        获取研究的子主题列表

        基于当前查询和研究上下文，生成相关的子主题，
        用于构建详细报告的结构。

        返回:
            子主题列表
        """
        return await self.report_generator.get_subtopics()

    async def get_draft_section_titles(self, current_subtopic: str):
        """
        为当前子主题生成草稿章节标题

        参数:
            current_subtopic (str): 当前子主题

        返回:
            章节标题列表
        """
        return await self.report_generator.get_draft_section_titles(current_subtopic)

    async def get_similar_written_contents_by_draft_section_titles(
        self,
        current_subtopic: str,
        draft_section_titles: list[str],
        written_contents: list[dict],
        max_results: int = 10
    ) -> list[str]:
        """
        根据草稿章节标题获取相似的已写内容

        使用语义搜索找到与当前章节标题相关的已有内容，
        避免重复写作并提高内容连贯性。

        参数:
            current_subtopic (str): 当前子主题
            draft_section_titles (list[str]): 草稿章节标题列表
            written_contents (list[dict]): 已写内容列表
            max_results (int): 最大返回结果数

        返回:
            list[str]: 相似内容列表
        """
        return await self.context_manager.get_similar_written_contents_by_draft_section_titles(
            current_subtopic,
            draft_section_titles,
            written_contents,
            max_results
        )

    # === 工具方法集合 ===
    # 这些方法提供了各种实用功能，用于管理研究数据和生成报告

    def get_research_images(self, top_k=10) -> list[dict[str, Any]]:
        """
        获取研究过程中收集的图片

        参数:
            top_k (int): 返回的最大图片数量

        返回:
            list[dict]: 图片信息列表，包含URL、标题、描述等
        """
        return self.research_images[:top_k]

    def add_research_images(self, images: list[dict[str, Any]]) -> None:
        """
        添加研究图片到集合中

        参数:
            images (list[dict]): 要添加的图片信息列表
        """
        self.research_images.extend(images)

    def get_research_sources(self) -> list[dict[str, Any]]:
        """
        获取所有研究来源

        返回:
            list[dict]: 研究来源列表，包含标题、内容、URL等信息
        """
        return self.research_sources

    def add_research_sources(self, sources: list[dict[str, Any]]) -> None:
        """
        添加研究来源到集合中

        参数:
            sources (list[dict]): 要添加的来源信息列表
        """
        self.research_sources.extend(sources)

    def add_references(self, report_markdown: str, visited_urls: set) -> str:
        """
        为报告添加引用信息

        参数:
            report_markdown (str): 报告的Markdown内容
            visited_urls (set): 访问过的URL集合

        返回:
            str: 添加了引用的报告内容
        """
        return add_references(report_markdown, visited_urls)

    def extract_headers(self, markdown_text: str) -> list[dict]:
        """
        从Markdown文本中提取标题

        参数:
            markdown_text (str): Markdown文本

        返回:
            list[dict]: 标题信息列表
        """
        return extract_headers(markdown_text)

    def extract_sections(self, markdown_text: str) -> list[dict]:
        """
        从Markdown文本中提取章节

        参数:
            markdown_text (str): Markdown文本

        返回:
            list[dict]: 章节信息列表
        """
        return extract_sections(markdown_text)

    def table_of_contents(self, markdown_text: str) -> str:
        """
        为Markdown文本生成目录

        参数:
            markdown_text (str): Markdown文本

        返回:
            str: 生成的目录内容
        """
        return table_of_contents(markdown_text)

    def get_source_urls(self) -> list:
        """
        获取所有访问过的源URL列表

        返回:
            list: URL列表
        """
        return list(self.visited_urls)

    def get_research_context(self) -> list:
        """
        获取研究上下文数据

        返回:
            list: 上下文数据列表
        """
        return self.context

    def get_costs(self) -> float:
        """
        获取当前研究的总成本

        返回:
            float: 总成本金额
        """
        return self.research_costs

    def set_verbose(self, verbose: bool):
        """
        设置详细输出模式

        参数:
            verbose (bool): 是否启用详细输出
        """
        self.verbose = verbose

    def add_costs(self, cost: float) -> None:
        """
        添加研究成本到总成本中

        这个方法用于跟踪研究过程中产生的各种成本，包括：
        1. API调用成本（LLM、搜索引擎等）
        2. 数据处理成本
        3. 存储成本

        成本跟踪有助于：
        - 优化研究策略
        - 控制预算
        - 分析成本效益

        参数:
            cost (float): 要添加的成本金额

        异常:
            ValueError: 如果成本不是数字类型
        """
        # 验证成本参数类型
        if not isinstance(cost, (float, int)):
            raise ValueError("成本必须是整数或浮点数")

        # 累加到总成本
        self.research_costs += cost

        # 如果有日志处理器，记录成本更新事件
        if self.log_handler:
            self._log_event("research", step="cost_update", details={
                "cost": cost,                    # 本次添加的成本
                "total_cost": self.research_costs # 累计总成本
            })
