# 竞品调研可视化系统 📊

一个现代化的竞品调研工具，能够生成美观的HTML可视化报告，重点突出「3秒扫一眼」的快速信息获取能力。

## ✨ 核心特色

### 🎯 4层信息金字塔设计
- **0-5秒**: Hero Snapshot + 价值曲线插图
- **5-30秒**: 竞争雷达图 + 增长时间轴 + 指标图表  
- **30秒-3分钟**: 6大洞察卡片 + 创始人护城河画布
- **3分钟+**: 折叠面板收纳详细调研数据

### 📊 5个核心可视化组件
1. **Hero Snapshot**: 一句话定位 + 4个关键指标（ARR、客户数、90天增长、复刻难度）
2. **Value Curve**: 问题→解决方案的渐变式流程图
3. **Competitive Radar**: 5维度雷达图（定制化、自动化、开源、生态、价格）
4. **Growth Timeline**: 增长里程碑时间轴 + 证据截图
5. **Founder Moat Canvas**: 创始人护城河4象限分析

### 🎨 现代化UI设计
- **技术栈**: TailwindCSS + Chart.js + Lucide Icons
- **布局**: 12栅格系统，1200px宽度，响应式设计
- **动效**: 滚动渐显 + 雷达图绘制动画
- **主题**: 渐变背景 + 深色模式支持

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 基本使用
```python
import asyncio
from backend.report_type.competitive_intelligence.competitive_intelligence import CompetitiveIntelligenceVisualReport

async def generate_visual_report():
    # 创建可视化报告实例
    visual_report = CompetitiveIntelligenceVisualReport(
        query="notion",  # 产品名称或URL
        report_type="competitive_intelligence_visual",
        report_source="web"
    )
    
    # 生成JSON数据
    json_data = await visual_report.run()
    
    # 生成HTML可视化报告
    html_content = await visual_report.generate_html_report()
    
    # 保存HTML文件
    with open("competitive_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ 可视化报告已生成: competitive_report.html")

# 运行
asyncio.run(generate_visual_report())
```

### 命令行使用
```bash
# 运行演示
python demo_visual_competitive_intelligence.py

# 运行测试
python test_competitive_intelligence_visual.py
```

## 📂 项目结构

```
gpt-researcher/
├── schemas/
│   └── competitive_intelligence_visual_schema.json  # JSON数据结构定义
├── templates/
│   ├── competitive_intelligence_visual.html        # HTML模板
│   └── renderer.py                                 # 模板渲染器
├── backend/report_type/competitive_intelligence/
│   └── competitive_intelligence.py                 # 核心实现
├── gpt_researcher/
│   ├── prompts.py                                  # AI提示词
│   └── utils/enum.py                               # 报告类型枚举
├── test_competitive_intelligence_visual.py         # 集成测试
└── demo_visual_competitive_intelligence.py         # 使用演示
```

## 🏗️ 数据结构

### JSON Schema 概览
```json
{
  "metadata": {
    "product_name": "产品名称",
    "report_date": "2025-06-14", 
    "version": "2.0",
    "report_type": "visual"
  },
  "layer_1_hero": {
    "hero_snapshot": {
      "tagline": "一句话产品定位",
      "key_metrics": {
        "arr": "$1.2M",
        "clients": 39,
        "growth_90d": "+18%",
        "replication_difficulty": "困难"
      }
    },
    "value_curve": {
      "problems": ["痛点1", "痛点2"],
      "solutions": ["解决方案1", "解决方案2"]
    }
  },
  "layer_2_visual": {
    "competitive_radar": {
      "dimensions": ["定制化", "自动化深度", "开源透明", "生态", "价格"],
      "scores": [4.2, 3.8, 4.5, 3.2, 4.0]
    },
    "growth_timeline": [...],
    "metrics_chart": {...}
  },
  "layer_3_cards": {
    "insight_cards": {...},
    "founder_moat_canvas": {...}
  },
  "layer_4_detailed": {
    "detailed_research": {...}
  }
}
```

## 🎛️ 配置选项

### 报告类型
- `competitive_intelligence`: 传统文本报告
- `competitive_intelligence_detailed`: 详细文本报告  
- `competitive_intelligence_visual`: **新增**可视化报告

### UI主题配置
```json
{
  "theme": {
    "primary_color": "#0EA5E9",
    "accent_color": "#06B6D4",
    "background": "gradient",
    "font_family": "Inter, PingFang SC"
  },
  "layout": {
    "grid_columns": 12,
    "max_width": "1200px",
    "margin": "72px",
    "gutter": "24px"
  },
  "animations": {
    "scroll_reveal": true,
    "radar_draw_duration": "0.6s",
    "fade_in_duration": "40ms"
  }
}
```

## 🧪 测试和验证

### 运行测试套件
```bash
python test_competitive_intelligence_visual.py
```

测试包括：
- ✅ 数据验证和补全
- ✅ 模板渲染功能
- ✅ 完整报告生成
- ✅ 错误处理机制

### 测试产品示例
- `notion` - 知识管理平台
- `figma` - 设计协作工具
- `claude.ai` - AI助手
- `https://gadget.dev` - 开发工具

## 📊 输出示例

### JSON数据输出
```bash
outputs/visual_report_notion_20250614_233033.json
```

### HTML可视化报告
```bash
outputs/visual_report_notion_20250614_233033.html
```

## 🔧 技术实现

### 核心组件
1. **数据生成**: AI驱动的结构化数据提取
2. **数据验证**: 自动补全和错误处理
3. **模板渲染**: Handlebars-like语法支持
4. **可视化**: Chart.js图表 + CSS动画

### 优化特性
- **搜索引擎**: Tavily + Google双引擎
- **平台优先级**: 37个关键平台覆盖
- **数据过滤**: 智能筛选高质量信息源
- **容错机制**: 降级渲染确保可用性

## 🚀 部署和扩展

### 生产环境配置
```python
# 设置环境变量
ANTHROPIC_API_KEY=your_key
TAVILY_API_KEY=your_key  
GOOGLE_API_KEY=your_key  # 可选

# 启动服务
python backend/server/app.py
```

### 自定义扩展
```python
# 自定义模板
from templates.renderer import TemplateRenderer

renderer = TemplateRenderer("custom_templates/")
html = renderer.render_competitive_intelligence_visual(data)

# 自定义UI配置
data["ui_config"]["theme"]["primary_color"] = "#FF6B6B"
```

## 📈 性能特点

- **生成速度**: 2-3分钟完整报告
- **数据准确性**: 37个平台信息融合
- **视觉效果**: 现代化响应式设计
- **信息密度**: 4层渐进式信息展示
- **用户体验**: 3秒快速概览 → 深度分析

## 🤝 贡献指南

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目基于MIT许可证开源。

## 🙏 致谢

感谢GPT-Researcher团队提供的强大调研框架，以及所有贡献者的支持！

---

**🎯 一句话总结**: 先让用户3秒认知价值，再用30秒确认关键信息，最后提供3分钟深读——视觉层次就是产品洞察的优先级排序！