# 竞品情报研究代理使用指南

## 概述

CompetitiveIntelligenceAgent 是基于 gpt-researcher 开发的专门用于产品深度商业壁垒调研的智能代理。它能够自动收集、分析和生成结构化的竞品情报报告。

## 核心特性

### 1. 七大模块研究框架

- **基础信息 | Facts**: 自动收集团队规模、成立时间、产品类型等基础数据
- **创始人/团队 | Founder Intelligence**: 深度挖掘创始人背景和不公平优势
- **八维分析 | 8 Questions**: 全方位分析产品的市场定位和竞争力
- **营销情报 | Growth Intelligence**: 追踪增长时间线和营销策略
- **复刻评估 | Solo-Dev Feasibility**: 评估独立开发者复刻的可行性
- **Executive Summary**: 生成核心洞察和可迁移要素
- **信息来源 | Sources**: 所有信息附带可验证的来源

### 2. 智能查询生成

- 针对每个模块定制化的搜索策略
- 优先搜索特定信息源（如 LinkedIn、Crunchbase、GitHub）
- 支持并行搜索提高效率

### 3. 竞品识别与对比

- 自动从搜索结果中识别主要竞品
- 生成多维度评分矩阵
- 分析竞争优势和市场定位

### 4. 信息验证机制

- 所有关键信息必须附带来源
- 缺失信息自动标记 "⚠️ Info insufficient"
- 提供搜索轨迹便于追溯

## 快速开始

### 安装依赖

```bash
# 确保已安装 gpt-researcher
pip install gpt-researcher

# 设置环境变量
export OPENAI_API_KEY="your-api-key"
# 或使用其他支持的 LLM 提供商
```

### 基本使用

```python
import asyncio
from gpt_researcher.agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from gpt_researcher.config import Config

async def research_product():
    # 创建配置
    config = Config()
    
    # 创建竞品情报代理
    agent = CompetitiveIntelligenceAgent(
        product_name="Notion",
        product_url="https://notion.so",  # 可选
        config=config
    )
    
    # 执行研究
    result = await agent.conduct_research()
    
    # 输出报告
    print(result["report"])
    
    # 查看验证结果
    print("验证结果:", result["validation"])
    
    # 保存报告
    with open("notion_report.md", "w", encoding="utf-8") as f:
        f.write(result["report"])

# 运行研究
asyncio.run(research_product())
```

## 高级配置

### 自定义 LLM 提供商

```python
config = Config()
config.llm_provider = "anthropic"  # 使用 Claude
config.fast_llm_model = "claude-3-haiku-20240307"
config.smart_llm_model = "claude-3-opus-20240229"
```

### 自定义搜索引擎

```python
config.retriever = "tavily"  # 使用 Tavily 搜索
config.max_search_results_per_query = 10  # 每个查询的最大结果数
```

### 批量研究

```python
async def batch_research():
    products = [
        {"name": "ChatGPT", "url": "https://chat.openai.com"},
        {"name": "Claude", "url": "https://claude.ai"},
        {"name": "Gemini", "url": "https://gemini.google.com"}
    ]
    
    tasks = []
    for product in products:
        agent = CompetitiveIntelligenceAgent(
            product_name=product["name"],
            product_url=product["url"]
        )
        tasks.append(agent.conduct_research())
    
    results = await asyncio.gather(*tasks)
    return results
```

## 输出格式示例

```markdown
### 【基础信息 | Facts】

**Team Size**: 100-500
**Name**: Notion
**One-liner**: All-in-one workspace for notes, docs, and collaboration
**Type**: SaaS
**URL**: https://notion.so
**Launch Status**: GA
**Founded**: 2016

### 【创始人/团队 | Founder Intelligence】

**a. 👤 人物画像**
- 身份背景: Ivan Zhao (CEO), 前 Inkling 工程师
- 技术能力: 全栈开发，专注于用户界面设计
- 行业深度: 10+ 年生产力工具开发经验

**b. 🎯 不公平优势**
- 行业洞察: 深刻理解知识工作者的工作流程痛点
- 技术实现: 创新的块编辑器架构，灵活可扩展
- 资源网络: 硅谷顶级投资人背书
- 时机判断: 抓住远程办公趋势

[... 更多模块内容 ...]
```

## 核对表验证

系统会自动验证以下项目：

- ✅ Team Size 已填写
- ✅ Q2/Q3/Q6/Q7 及营销板块均附来源
- ✅ 无猜测词（如"可能/我认为/大概"）
- ✅ 信息缺失处写 ⚠️ Info insufficient + 搜索轨迹
- ✅ Q8 仅讨论应用层，不谈底模
- ✅ 复刻评估含行业壁垒
- ✅ Executive Summary 覆盖创始人优势

## 注意事项

1. **API 消耗**: 深度研究会进行大量搜索和 LLM 调用，请注意 API 费用
2. **运行时间**: 完整研究通常需要 3-5 分钟
3. **信息准确性**: 虽然系统要求所有信息附带来源，但仍需人工验证关键数据
4. **隐私考虑**: 研究结果可能包含公开的个人信息，请谨慎使用和分享

## 扩展开发

### 添加新的研究模块

```python
class CustomCompetitiveAgent(CompetitiveIntelligenceAgent):
    async def _research_custom_module(self):
        """添加自定义研究模块"""
        queries = [
            f"{self.product_name} custom aspect 1",
            f"{self.product_name} custom aspect 2"
        ]
        
        results = await self._parallel_search(queries)
        # 处理结果...
```

### 自定义报告格式

```python
from gpt_researcher.agents.utils import CompetitiveReportGenerator

class CustomReportGenerator(CompetitiveReportGenerator):
    def generate_report(self, data):
        # 自定义报告格式
        pass
```

## 常见问题

**Q: 如何提高信息收集的准确性？**
A: 提供准确的产品 URL，使用更强大的 LLM 模型（如 GPT-4 或 Claude Opus）

**Q: 为什么某些信息显示 "⚠️ Info insufficient"？**
A: 表示系统未能从公开来源找到该信息，可能需要手动补充

**Q: 可以研究非英文产品吗？**
A: 可以，系统会自动处理多语言内容，但英文产品的信息通常更丰富

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个工具。主要改进方向：

1. 增加更多专业信息源
2. 优化信息提取算法
3. 支持更多产品类型的专门化分析
4. 改进竞品识别准确性

## 许可证

本项目基于 gpt-researcher 开发，遵循相同的开源许可证。