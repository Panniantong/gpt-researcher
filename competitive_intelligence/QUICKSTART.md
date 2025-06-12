# 竞品调研 Agent - 快速开始指南

## 🚀 30秒快速开始

```bash
# 1. 设置 API 密钥
export OPENAI_API_KEY="your-api-key"

# 2. 运行演示
python competitive_intelligence/demo.py

# 选择 2 进行快速演示
```

## 📦 安装要求

确保已安装 gpt-researcher 和相关依赖：

```bash
pip install gpt-researcher
pip install python-dotenv
```

## 💡 使用示例

### 1. 最简单的使用方式

```python
import asyncio
from competitive_intelligence import CompetitiveIntelligenceAgent

async def analyze_product():
    agent = CompetitiveIntelligenceAgent(
        query="Notion",
        llm_provider="openai",
        model="gpt-4o-mini"
    )
    
    report = await agent.run_research()
    print(report)

asyncio.run(analyze_product())
```

### 2. 指定产品URL（推荐）

```python
agent = CompetitiveIntelligenceAgent(
    query="v0",
    product_url="https://v0.dev",  # 提供URL可获得更准确的信息
    llm_provider="openai",
    model="gpt-4o-mini"
)
```

### 3. 只分析特定模块

```python
from competitive_intelligence.modules.basic_info import BasicInfoExtractor

extractor = BasicInfoExtractor("openai", "gpt-4o-mini")
info = await extractor.extract_from_content(html_content, url)
```

## 🎯 分析维度说明

1. **基础信息** - 产品名称、描述、团队规模等
2. **创始人背景** - 团队背景和不公平优势分析
3. **八维分析** - 从8个角度深入剖析产品
4. **营销情报** - 增长策略和获客渠道
5. **复刻评估** - AI时代的技术和商业壁垒
6. **执行摘要** - 核心洞察和策略建议

## ⚙️ 配置选项

### 使用不同的 LLM

```python
# OpenAI
agent = CompetitiveIntelligenceAgent(
    query="Product",
    llm_provider="openai",
    model="gpt-4"
)

# Anthropic
agent = CompetitiveIntelligenceAgent(
    query="Product",
    llm_provider="anthropic",
    model="claude-3-haiku-20240307"
)
```

### 自定义搜索深度

默认配置已优化，但可以通过修改查询数量来调整：

- `_perform_searches` 中的 `queries[:5]` - 控制搜索查询数
- `search_results[:3]` - 控制每个查询的结果数

## 🐛 常见问题

### 1. "No retriever available"

**解决方案**：确保设置了搜索 API 密钥（如 TAVILY_API_KEY）

```bash
export TAVILY_API_KEY="your-tavily-api-key"
```

### 2. 分析时间过长

**解决方案**：使用快速模式或只分析特定模块

### 3. API 调用错误

**解决方案**：
- 检查 API 密钥是否正确
- 确认账户有足够的配额
- 使用更小的模型（如 gpt-4o-mini）

## 📊 输出示例

```markdown
# 竞品调研报告：Cursor

## 【基础信息 | Facts】
**Team Size**: 小团队(2-5人)
**Name**: Cursor
**One-liner**: The AI-first code editor
...

## 【创始人/团队背景分析 | Founder Intelligence】
### 👤 核心人物画像
- **身份背景**：MIT毕业，前Facebook工程师...
...

## 【复刻难度评估 | Solo Developer Feasibility】
**难度等级**：🔴 困难
...
```

## 🎨 高级用法

### 批量分析

```python
products = ["Cursor", "v0", "Perplexity"]
for product in products:
    agent = CompetitiveIntelligenceAgent(query=product)
    report = await agent.run_research()
    await agent.save_results(f"{product}_analysis.json")
```

### 集成到应用

```python
# FastAPI 示例
from fastapi import FastAPI

app = FastAPI()

@app.post("/analyze")
async def analyze_product(product_name: str, product_url: str = None):
    agent = CompetitiveIntelligenceAgent(
        query=product_name,
        product_url=product_url
    )
    report = await agent.run_research()
    return {"report": report, "summary": agent.results["executive_summary"]}
```

## 🔗 相关资源

- [完整文档](README.md)
- [示例脚本](example_usage.py)
- [演示程序](demo.py)

## 💬 获取帮助

遇到问题？
1. 查看 [README.md](README.md) 中的详细说明
2. 运行 `python competitive_intelligence/test_minimal.py` 测试基础功能
3. 查看 demo.py 中的示例代码