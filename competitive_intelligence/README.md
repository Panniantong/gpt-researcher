# 竞品调研 Agent (Competitive Intelligence Agent)

基于 gpt-researcher 的专门用于产品竞品深度调研的智能代理。

## 功能特性

### 📊 八大分析维度

1. **基础信息获取** - 自动提取产品名称、描述、团队规模等
2. **创始人背景调研** - 深入分析创始人经历和不公平优势
3. **八维深度分析** - 从8个维度全面剖析产品特性
4. **营销情报分析** - 研究增长策略和获客渠道
5. **复刻难度评估** - 评估独立开发者复刻的可行性
6. **执行摘要生成** - 提炼核心洞察和可执行建议
7. **竞争定位分析** - 判断 First/Only/Number One
8. **技术架构解析** - 分析应用层API组合方案

## 快速开始

### 安装依赖

```bash
# 确保已安装 gpt-researcher
pip install gpt-researcher

# 设置环境变量
export OPENAI_API_KEY="your-api-key"
# 或其他LLM提供商的API密钥
```

### 基本使用

```python
import asyncio
from competitive_intelligence import CompetitiveIntelligenceAgent

async def analyze():
    # 创建竞品调研Agent
    agent = CompetitiveIntelligenceAgent(
        query="Cursor",  # 产品名称
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    # 运行调研
    report = await agent.run_research()
    print(report)
    
    # 保存结果
    await agent.save_results("cursor_analysis.json")

# 运行
asyncio.run(analyze())
```

### 通过URL分析

```python
agent = CompetitiveIntelligenceAgent(
    query="v0",
    product_url="https://v0.dev",  # 直接提供URL
    llm_provider="openai",
    model="gpt-4o-mini"
)
```

### 使用便捷函数

```python
from competitive_intelligence.agent import analyze_competitor

report = await analyze_competitor(
    query="Notion",
    product_url="https://www.notion.so"
)
```

## 输出格式示例

```markdown
# 竞品调研报告：[产品名称]

## 【基础信息 | Facts】
**Team Size**: 小团队(2-5人)
**Name**: Cursor
**One-liner**: The AI-first code editor
**Type**: AI开发工具
**URL**: https://cursor.sh
**Launch Status**: 正式版
**Founded**: 2022

## 【创始人/团队背景分析 | Founder Intelligence】
### 👤 核心人物画像
- **身份背景**：MIT毕业，前Facebook工程师...
- **技术能力**：深度学习、编译器设计...
- **行业深度**：5年+开发工具经验...

### 🎯 不公平优势识别
- AI/ML技术背景优势
- 深厚的编程语言理论基础
- MIT校友网络资源

## 【八维分析 | 8 Questions】
### Q1 · One-sentence Pitch
AI驱动的代码编辑器，让编程速度提升10倍

### Q2 · Fixed 'Broken' Spot
传统IDE无法理解代码上下文，Cursor通过AI深度理解代码意图...

[... 更多分析内容 ...]

## 【营销情报 | Growth Intelligence】
### G1 · Growth Timeline & Milestones
- **Launch Phase**: 2022年在HN发布MVP，获得500+赞
- **Growth Phase**: 2023年获得种子轮融资，用户破10万

## 【复刻难度评估 | Solo Developer Feasibility】
**难度等级**：🔴 困难

### ⚡ 核心技术挑战
1. 需要深度集成VSCode架构
2. AI模型的上下文管理复杂
3. 实时代码补全的性能优化

## 【Executive Summary】
### 🎯 核心洞察
Cursor抓住了AI编程助手的早期机会，通过深度IDE集成...

### ⭐ AI时代独立开发者策略
建议从VSCode插件切入，专注特定语言或框架...
```

## 高级用法

### 只分析特定模块

```python
from competitive_intelligence.modules.basic_info import BasicInfoExtractor
from competitive_intelligence.modules.founder_analysis import FounderAnalyzer

# 只获取基础信息
extractor = BasicInfoExtractor()
info = await extractor.extract_from_url("https://example.com")

# 只分析创始人背景
analyzer = FounderAnalyzer()
founder_info = await analyzer.analyze_founder_background(
    "Product Name",
    search_results
)
```

### 自定义配置

创建 `config.yaml`:

```yaml
llm_provider: "anthropic"
fast_llm_model: "claude-3-haiku-20240307"
temperature: 0.2
max_tokens: 3000
```

使用配置：

```python
agent = CompetitiveIntelligenceAgent(
    query="Product",
    config_path="config.yaml"
)
```

## 模块说明

### BasicInfoExtractor
- 从网页自动提取产品基础信息
- 智能推断团队规模
- 验证信息完整性

### FounderAnalyzer
- 搜索创始人背景信息
- 识别不公平优势
- 判断是否符合"AI+行业专家"模式

### EightDimensionsAnalyzer
- 8个维度的产品分析
- 自动判断哪些维度需要调研
- 生成针对性搜索查询

### MarketingIntelAnalyzer
- 分析增长时间线
- 识别主要获客渠道
- 提取病毒式传播因素

### ReplicationEvaluator
- 评估技术复刻难度
- 分析行业壁垒
- 生成复刻策略建议

### ExecutiveSummaryGenerator
- 整合所有分析结果
- 提炼核心洞察
- 生成可执行建议

## 注意事项

1. **API限制**：大量搜索和分析会消耗较多API调用
2. **搜索质量**：搜索结果质量影响分析准确性
3. **信息时效**：部分信息可能过时，建议定期更新
4. **隐私考虑**：分析公开信息，不涉及隐私数据

## 常见问题

### Q: 分析一个产品需要多长时间？
A: 通常需要3-5分钟，取决于搜索和分析的深度。

### Q: 支持哪些LLM提供商？
A: 支持 OpenAI、Anthropic、Google 等主流提供商。

### Q: 如何提高分析质量？
A: 1) 提供准确的产品URL 2) 使用更强大的模型 3) 增加搜索深度

### Q: 可以批量分析吗？
A: 可以，参考 `example_usage.py` 中的批量分析示例。

## 开发计划

- [ ] 支持更多语言的产品分析
- [ ] 添加竞品对比矩阵
- [ ] 集成更多数据源（ProductHunt、Crunchbase等）
- [ ] 支持定期监控和更新
- [ ] 添加可视化报告生成

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

与 gpt-researcher 保持一致的开源许可。