"""
竞品调研专用提示词模板
"""

# 基础信息获取提示词
BASIC_INFO_PROMPT = """
请从给定的网页内容中提取以下产品基础信息。注意：所有JSON字段名必须使用小写字母和下划线。

要提取的信息：
1. 产品名称 - 字段名: name
2. 官方一句话描述/Tagline - 字段名: one_liner (保留原文)
3. 产品类型/领域 - 字段名: type
4. 官方网址 - 字段名: url
5. 发布状态 - 字段名: launch_status (Beta/正式版/MVP等)
6. 创立时间 - 字段名: founded
7. 团队规模 - 字段名: team_size (独立开发者/小团队(2-5人)/中型团队(6-20人)/大团队(20+人))

网页内容：
{content}

请严格按照以下JSON格式返回，所有字段名必须是小写：
{{
  "name": "产品名称",
  "one_liner": "一句话描述",  
  "type": "产品类型",
  "url": "官方网址",
  "launch_status": "发布状态",
  "founded": "创立时间",
  "team_size": "团队规模"
}}
"""

# 创始人背景调研提示词
FOUNDER_RESEARCH_PROMPT = """
基于以下搜索结果，分析产品 {product_name} 的创始人/团队背景：

搜索结果：
{search_results}

请提取并分析：
1. 创始人身份背景（职业经历、教育背景、行业经验）
2. 技术能力（编程背景、技术栈、开源贡献等）
3. 行业深度（在产品所属行业的从业时间、专业程度、影响力）
4. 不公平优势（基于背景的独特优势）
5. 是否符合"AI + 行业专家"模式

请包含具体的信息来源URL。
"""

# 八维分析 - Q2 固定"缺口"调研
Q2_BROKEN_SPOT_PROMPT = """
产品名称：{product_name}
产品描述：{product_description}

基于以下搜索结果，分析这个产品解决了什么现实问题或填补了什么缺口：
{search_results}

请找出：
1. 现实中哪个环节是"坏掉的"或低效的？
2. 这个产品如何补上这个缺口？
3. 引用具体的场景或数据作为证据
4. 列出信息来源URL
"""

# 八维分析 - Q3 用户紧迫性调研
Q3_USER_URGENCY_PROMPT = """
产品名称：{product_name}
产品描述：{product_description}

基于以下搜索结果，分析目标用户对这个产品的紧迫需求：
{search_results}

请分析：
1. 目标用户是否会立刻付费或留下邮箱？
2. 是什么让他们产生紧迫感？
3. 提供公开证据（用户评论、增长数据、社区讨论等）
4. 列出信息来源URL
"""

# 八维分析 - Q6 竞技场与得分规则
Q6_ARENA_SCORING_PROMPT = """
产品名称：{product_name}
产品所在领域：{product_type}

基于以下搜索结果，分析这个细分赛道的竞争规则：
{search_results}

请分析：
1. 这个细分赛道最窄可行的定义是什么？
2. 业内公认的1-3个胜负指标是什么？（例如：速度、准确率、价格等）
3. 找出这些指标重要性的证据（行业报告、用户讨论、专家观点等）
4. 列出主要竞品及其在这些指标上的表现
5. 分析目标产品的领先逻辑
6. 所有分析必须包含信息来源URL
"""

# 八维分析 - Q7 定位分析
Q7_POSITIONING_PROMPT = """
产品名称：{product_name}
产品描述：{product_description}

基于以下搜索结果，判断产品的独特定位：
{search_results}

请分析这个产品是：
1. First One（开创10倍新赛道）- 是否是该领域第一个？
2. Only One（独占资源/不公平优势）- 是否有独特资源或护城河？
3. Number One（垂直第一）- 是否在某个细分领域做到第一？

提供具体理由和证据，包含信息来源URL。
"""

# 八维分析 - Q8 应用层架构分析
Q8_ARCHITECTURE_PROMPT = """
产品名称：{product_name}
产品功能：{product_features}

基于以下技术相关信息：
{tech_info}

请分析这个AI产品的应用层实现架构：

1. 核心功能拆解：最关键的1-2个功能及其所需的AI能力
2. API组合方案：
   - 使用了哪些第三方AI API（OpenAI、Anthropic、Google AI等）
   - 如何组合这些API实现核心功能
   - 数据在不同服务间如何流转
3. 应用层创新点：
   - Prompt Engineering设计
   - 工作流设计
   - 用户体验层的创新

注意：重点关注应用层的API组合和产品化包装，而非底层算法。
如信息不足，标注"⚠︎ Implementation details insufficient"并说明已找到的线索。
"""

# 营销情报分析提示词
MARKETING_INTEL_PROMPT = """
产品名称：{product_name}

基于以下搜索结果，分析产品的营销和增长策略：
{search_results}

请分析：
1. 增长时间线与里程碑
   - 发布时间和初期获客方式
   - 关键增长节点（融资、病毒传播、媒体曝光等）
   - 当前增长阶段重点
   
2. 增长渠道与策略
   - 主要的2-3个获客渠道
   - 独特的营销手法或病毒传播机制
   - 内容营销策略

请包含具体的信息来源URL。
"""

# 复刻难度评估提示词
REPLICATION_EVAL_PROMPT = """
产品名称：{product_name}
产品功能：{product_features}
技术架构：{tech_architecture}

基于AI辅助开发时代的技术栈（Next.js + Vercel + TypeScript + Cloudflare + supabase + Claude/Cursor），评估独立开发者复刻这个产品的难度：

1. 技术复刻评估
   - 前端实现难度（考虑AI代码生成能力）
   - API集成难度（考虑OpenRouter、Replicate等聚合平台）
   - AI Workflow复现难度
   - 业务逻辑复杂度

2. 核心技术挑战（按优先级列出3-4个即使有AI辅助仍然困难的点）

3. AI辅助开发优势
   - 哪些部分可通过Claude、Cursor等工具快速实现
   - 可参考的开源项目或模板

4. 行业壁垒评估（重点！）
   - 行业knowhow要求
   - 用户获取难度
   - 信任建立成本
   - 网络效应
   - 数据壁垒

给出难度等级：🟢 容易 | 🟡 中等 | 🔴 困难 | ⚫ 极难
"""

# 执行摘要生成提示词
EXECUTIVE_SUMMARY_PROMPT = """
基于以下竞品调研结果，生成执行摘要：

基础信息：{basic_info}
创始人分析：{founder_analysis}
八维分析：{eight_dimensions}
营销情报：{marketing_intel}
复刻评估：{replication_eval}

请生成：
1. 核心洞察（≤100字）- 总结产品的核心价值与市场定位
2. 增长模式（≤80字）- 总结独特的增长策略或获客模式
3. 创始人优势（≤60字）- 总结创始人/团队的核心不公平优势
4. 可迁移要素（3-4条）- 技术、产品、营销、运营方面
5. 趋势判断 - 产品反映的行业趋势或技术发展方向
6. AI时代独立开发者策略（≤100字）- 基于AI辅助开发能力的执行路径建议
"""

# 搜索查询生成提示词
SEARCH_QUERY_GENERATOR = """
为了深入调研产品 {product_name}，请生成相关的搜索查询。

产品信息：
- 名称：{product_name}
- 网址：{product_url}
- 类型：{product_type}

调研目标：{research_goal}

请生成5-8个高质量的搜索查询，应该包括：
1. 直接搜索（产品名 + 关键词）
2. 竞品对比搜索
3. 行业分析搜索
4. 创始人/团队搜索
5. 技术栈搜索（如果适用）

返回格式：每行一个查询
"""