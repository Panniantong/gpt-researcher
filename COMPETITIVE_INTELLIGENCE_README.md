# 竞品情报研究系统使用说明

## 🎯 系统概述

这是一个基于 gpt-researcher 开发的专门用于产品深度商业壁垒调研的智能系统。它能够：

- 自动收集产品的基础信息、创始人背景、市场定位等关键数据
- 分析产品的竞争优势和商业壁垒
- 评估独立开发者的复刻可行性
- 生成结构化的竞品情报报告

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install gpt-researcher python-dotenv

# 设置 API Key（选择一个）
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export GOOGLE_API_KEY="your-google-api-key"
```

### 2. 运行示例

```bash
# 运行简单示例（不会实际调用 API）
python simple_competitive_test.py

# 运行完整测试（会显示系统功能，但不会调用外部 API）
python test_competitive_intelligence.py

# 运行实际研究（会调用 API，产生费用）
python examples/competitive_intelligence_example.py
```

## 📊 输出示例

系统会生成包含以下7大模块的报告：

1. **基础信息 | Facts**
   - Team Size, Name, One-liner, Type, URL, Launch Status, Founded

2. **创始人/团队 | Founder Intelligence**
   - 人物画像、不公平优势、行业专家验证

3. **八维分析 | 8 Questions**
   - Q1 Pitch, Q2 Fixed Broken Spot, Q3 User Urgency...

4. **营销情报 | Growth Intelligence**
   - 增长时间线、营销渠道和策略

5. **复刻评估 | Solo-Dev Feasibility**
   - 难度等级、技术挑战、AI辅助优势

6. **Executive Summary**
   - 核心洞察、增长模式、创始人优势等

7. **信息来源 | Sources**
   - 所有收集到的信息来源URL

## ⚠️ 注意事项

1. **API 费用**：完整研究会进行大量的搜索和 LLM 调用，请注意控制成本
2. **运行时间**：一次完整研究通常需要 3-5 分钟
3. **信息准确性**：虽然系统会标注信息来源，但仍建议人工验证关键数据
4. **产品选择**：英文产品通常能获得更丰富的信息

## 🛠️ 自定义配置

### 使用不同的 LLM

```python
config = Config()
config.llm_provider = "anthropic"  # 或 "openai", "google"
config.fast_llm_model = "claude-3-haiku-20240307"
config.smart_llm_model = "claude-3-opus-20240229"
```

### 调整搜索参数

```python
config.max_search_results_per_query = 10  # 每个查询的最大结果数
config.retriever = "tavily"  # 使用 Tavily 搜索引擎
```

## 📁 文件结构

```
gpt-researcher/
├── gpt_researcher/
│   └── agents/
│       ├── competitive_intelligence_agent.py  # 主代理类
│       └── utils/
│           ├── competitive_query_builder.py   # 查询构建器
│           ├── competitive_report_generator.py # 报告生成器
│           └── competitor_analyzer.py         # 竞品分析器
├── examples/
│   └── competitive_intelligence_example.py    # 完整示例
├── test_competitive_intelligence.py           # 功能测试
├── simple_competitive_test.py                 # 简单示例
└── docs/
    └── competitive_intelligence_guide.md      # 详细文档
```

## 🤝 贡献指南

欢迎贡献代码来改进这个系统！主要改进方向：

1. 增加更多专业信息源的支持
2. 优化信息提取的准确性
3. 添加更多行业特定的分析维度
4. 改进竞品自动识别算法

## 📝 常见问题

**Q: 为什么显示 "⚠️ Info insufficient"？**
A: 表示系统未能从公开渠道找到该信息，你可以手动补充或尝试提供更准确的产品URL。

**Q: 如何降低 API 成本？**
A: 可以使用更便宜的模型（如 gpt-3.5-turbo），或减少搜索查询的数量。

**Q: 支持中文产品吗？**
A: 支持，但中文产品的公开信息通常较少，可能会有更多 "Info insufficient" 标记。

## 📧 联系方式

如有问题或建议，请在 GitHub 上提交 Issue。